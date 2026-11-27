"""Insert the two reviewed Kore explanations into the existing factorisation lesson."""
import hashlib
import json
import math
import re
import wave
from pathlib import Path

import numpy as np

RATE = 24000
DIRECTORY = Path("public/factorization-review-2026-11-12")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tokens(text):
    return re.sub(r"[^\w\s]", "", text.casefold()).split()


def signature(audio, narration):
    return hashlib.sha256(audio.read_bytes() + narration.encode()).hexdigest()


def read_audio(path, name, narration):
    alignment = load(path.parent / "alignment" / (name + ".json"))
    assert alignment["signature"] == signature(path, narration)
    words = alignment["words"]
    assert [word["word"].casefold() for word in words] == tokens(narration)
    with wave.open(str(path), "rb") as wav:
        assert (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) == (1, 2, RATE)
        return np.frombuffer(wav.readframes(wav.getnframes()), dtype="<i2"), words


def shift_words(words, shift):
    return [
        {**word, **{key: round(word[key] + shift, 6) for key in ("start", "end")}}
        for word in words
    ]


def insert_explanation(scene, clip, narration, beat_index, bases, source_span, split_time, lead):
    original = Path("public") / scene["audio"]
    source, words = read_audio(original, scene["id"], scene["narration"])
    patch_file = DIRECTORY / (clip + ".wav")
    patch, patch_words = read_audio(patch_file, clip, narration)
    trim_start, trim_end = source_span
    assert trim_start <= patch_words[0]["start"] and patch_words[-1]["end"] <= trim_end
    split = len(source) if split_time is None else round(split_time * RATE)
    split_time = split / RATE
    offset = sum(len(tokens(beat["text"])) for beat in scene["beats"][:beat_index + 1])
    assert words[offset - 1]["end"] <= split_time
    assert offset == len(words) or split_time <= words[offset]["start"]

    samples = patch[round(trim_start * RATE):round(trim_end * RATE)].astype(float)
    voiced = lambda pcm: pcm[np.abs(pcm.astype(float)) >= 900].astype(float)
    reference = voiced(source[max(0, split - 3 * RATE):split])
    clip_voiced = voiced(samples)
    gain = min(1.18, np.sqrt(np.mean(reference**2) / np.mean(clip_voiced**2)), 30000 / np.abs(samples).max())
    samples *= gain
    fade = np.linspace(0, 1, round(.012 * RATE))
    samples[:len(fade)] *= fade
    samples[-len(fade):] *= fade[::-1]
    inserted = np.concatenate((
        np.zeros(round(lead * RATE), dtype="<i2"),
        samples.round().astype("<i2"),
        np.zeros(round(.08 * RATE), dtype="<i2"),
    ))
    mixed = np.concatenate((source[:split], inserted, source[split:]))
    assert np.array_equal(np.concatenate((mixed[:split], mixed[split + len(inserted):])), source)
    extra = len(inserted) / RATE
    new_words = shift_words(patch_words, split_time + lead - trim_start)
    full_words = words[:offset] + new_words + shift_words(words[offset:], extra)
    scene["beats"][beat_index]["text"] += " " + narration
    scene["narration"] = " ".join(beat["text"] for beat in scene["beats"])
    assert [word["word"].casefold() for word in full_words] == tokens(scene["narration"])
    index = 0
    for beat in scene["beats"]:
        beat["from"] = round(full_words[index]["start"] * 30) if index else 0
        index += len(tokens(beat["text"]))
    for i, base in enumerate(bases):
        word, = [word for word in new_words if word["word"].casefold() == base]
        scene["cues"][f"emphasis{i}"] = round(word["start"] * 30)

    target = DIRECTORY / original.name
    with wave.open(str(target), "wb") as wav:
        wav.setparams((1, 2, RATE, len(mixed), "NONE", "not compressed"))
        wav.writeframes(mixed.tobytes())
    scene["audio"] = target.relative_to("public").as_posix()
    scene["durationInFrames"] = math.ceil((len(mixed) / RATE + scene.get("holdSeconds", .9)) * 30)
    scene["timingMethod"] = "MMS_FA known-transcript alignment, remapped after PCM insertion"
    digest = signature(target, scene["narration"])
    save(DIRECTORY / "alignment" / (scene["id"] + ".json"), {
        "signature": digest, "method": scene["timingMethod"], "words": full_words,
    })
    models = {load(Path(str(file) + ".json"))["model"] for file in (original, patch_file)}
    save(Path(str(target) + ".json"), {
        "provider": "gemini", "voice": "Kore", "model": " + ".join(sorted(models)), "signature": digest,
        "processing": "Aligned explanation inserted; original PCM samples preserved",
        "sourceAudio": original.relative_to("public").as_posix(), "insertedAudio": patch_file.name,
        "insertionAt": split_time, "secondsAdded": extra,
    })


timeline = load(Path("src/video/factorization-v2-lesson.json"))
for scene in timeline["scenes"]:
    scene["revision"] = "2026-11-12"
    kind = scene["kind"]
    if kind == "intro":
        scene["cues"].update(redEnd=300, greenEnd=390)
    elif kind == "theorem":
        insert_explanation(scene, "explanation-360", "Les nombres deux, trois et cinq sont des facteurs premiers.",
                           2, ("deux", "trois", "cinq"), (.24, 5.87), 20.82, .08)
    elif kind == "example":
        insert_explanation(scene, "explanation-72", "Pourquoi ? Car les facteurs deux et trois sont des nombres premiers.",
                           3, ("deux", "trois"), (.21, 5.85), None, .32)
save(Path("src/video/factorization-review-lesson.json"), timeline)
print(f"Factorisation review: {sum(s['durationInFrames'] for s in timeline['scenes']) / 30:.3f} s")
