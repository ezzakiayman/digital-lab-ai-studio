"""Update the prime lesson using the two reviewed Kore recordings and the original timings."""
import hashlib
import json
import re
import wave
from pathlib import Path

import numpy as np


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def signature(path, narration):
    return hashlib.sha256(path.read_bytes() + narration.encode()).hexdigest()


def tokens(text):
    return re.sub(r"[^\w\sً-ْٰ]", "", text.casefold()).split()


def wav(path):
    with wave.open(str(path), "rb") as source:
        assert (source.getnchannels(), source.getsampwidth(), source.getframerate()) == (1, 2, 24000), path
        return np.frombuffer(source.readframes(source.getnframes()), dtype="<i2")


def words_for(path, scene_id, narration):
    aligned = read(path.parent / "alignment" / (scene_id + ".json"))
    assert aligned["signature"] == signature(path, narration)
    return aligned["words"]


def spoken_level(samples):
    voiced = samples[np.abs(samples.astype(float)) >= 900].astype(float)
    return np.sqrt(np.mean(voiced**2))


timeline = read(Path("src/video/primes-v2-lesson.json"))
intro = timeline["scenes"][0]
original = Path("public") / intro["audio"]
original_pcm = wav(original)
original_words = words_for(original, intro["id"], intro["narration"])
directory = Path("public/primes-review-2026-11-12")
rate = 24000
new_pcm = np.zeros(round(20.64 * rate), dtype="<i2")
new_pcm[:len(original_pcm)] = original_pcm

patches = [
    # Clip name, transcript, old word indices, source interval, placement, replace interval.
    ("verifier", "Vérifier : تَحَقَّق.", (17, 24), (.24, 3.05), 9.88, (9.58, 13.12)),
    ("closing", "Et c’est le sujet de notre séance.", (34, 40), (.235, 2.42), 18.44, (18.42, 20.64)),
]
new_words = []
previous = 0
models = {read(Path(str(original) + ".json"))["model"]}
for name, narration, (first, last), (start, end), placement, (replace_start, replace_end) in patches:
    source = directory / (name + ".wav")
    model = read(Path(str(source) + ".json"))["model"]
    models.add(model)
    aligned = words_for(source, name, narration)
    assert tokens(narration) == [word["word"].casefold() for word in aligned]
    assert start <= aligned[0]["start"] and aligned[-1]["end"] <= end
    samples = wav(source)[round(start * rate):round(end * rate)].astype(float)
    assert replace_start <= placement and placement + len(samples) / rate <= replace_end
    assert original_words[first]["start"] >= replace_start and original_words[last - 1]["end"] <= replace_end
    assert original_words[first - 1]["end"] <= replace_start
    assert last == len(original_words) or original_words[last]["start"] >= replace_end
    reference = original_pcm[round(replace_start * rate):round(replace_end * rate)]
    gain = min(1.22, spoken_level(reference) / spoken_level(samples), 30000 / np.abs(samples).max())
    samples *= gain
    # Only the near-silent edges of the replacement take receive a short fade.
    fade = np.linspace(0, 1, round(.012 * rate))
    samples[:len(fade)] *= fade
    samples[-len(fade):] *= fade[::-1]
    new_pcm[round(replace_start * rate):round(replace_end * rate)] = 0
    index = round(placement * rate)
    new_pcm[index:index + len(samples)] = samples.round().astype("<i2")
    new_words.extend(original_words[previous:first])
    new_words.extend({
        **word,
        **{key: round(word[key] + placement - start, 6) for key in ("start", "end")},
    } for word in aligned)
    previous = last
new_words.extend(original_words[previous:])
assert np.array_equal(new_pcm[:round(9.58 * rate)], original_pcm[:round(9.58 * rate)])
assert np.array_equal(new_pcm[round(13.12 * rate):round(18.42 * rate)], original_pcm[round(13.12 * rate):round(18.42 * rate)])
assert len(new_pcm) / rate < intro["durationInFrames"] / 30

intro["beats"][2]["text"] = patches[0][1]
intro["beats"][2]["from"] = round(new_words[17]["start"] * 30)
intro["beats"][3]["text"] = intro["beats"][3]["text"].replace("C’est le sujet de notre séance.", patches[1][1])
intro["narration"] = " ".join(beat["text"] for beat in intro["beats"])
assert tokens(intro["narration"]) == [word["word"].casefold() for word in new_words]
intro["cues"]["explanation1"] = round(new_words[18]["start"] * 30)
intro["revision"] = "2026-11-12"
intro["audio"] = "primes-review-2026-11-12/objectif.wav"
intro["timingMethod"] = "MMS_FA known-transcript alignment, remapped after PCM cuts"
audio = Path("public") / intro["audio"]
with wave.open(str(audio), "wb") as output:
    output.setparams((1, 2, rate, len(new_pcm), "NONE", "not compressed"))
    output.writeframes(new_pcm.tobytes())
digest = signature(audio, intro["narration"])
write(audio.parent / "alignment/objectif.json", {
    "signature": digest, "method": intro["timingMethod"], "words": new_words,
})
write(Path(str(audio) + ".json"), {
    "provider": "gemini", "voice": "Kore", "model": " + ".join(sorted(models)), "signature": digest,
    "processing": "Two locally spliced Kore phrases; all other retained samples are byte-identical",
    "sourceAudio": original.relative_to("public").as_posix(),
    "patches": [patch[0] + ".wav" for patch in patches],
})

offset = 0
for scene in timeline["scenes"]:
    if scene["kind"] in ("one", "vocabulary"):
        scene["revision"] = "2026-11-12"
    if scene["kind"] == "vocabulary":
        cues = scene["cues"]
        cues.update({key: seconds * 30 - offset for key, seconds in (
            ("eleven", 206), ("divisorPair", 207), ("orangeBand", 215), ("conclusionArrow", 219), ("blinkPair", 223),
        )})
        words = words_for(Path("public") / scene["audio"], scene["id"], scene["narration"])
        phrase = ["onze", "est", "un", "nombre", "premier"]
        speech = [word["word"].casefold() for word in words]
        index, = (i for i in range(len(words)) if speech[i:i + len(phrase)] == phrase)
        cues.update({f"statement{i}": round(words[index + i]["start"] * 30) for i in range(len(phrase))})
    offset += scene["durationInFrames"]

write(Path("src/video/primes-review-lesson.json"), timeline)
print(f"Prime revision with original scene boundaries: {offset / 30:.3f} s")
