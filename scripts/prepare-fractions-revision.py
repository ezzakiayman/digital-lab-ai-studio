"""Apply the 2026-11-12 review to the delivered fractions timeline and cached speech."""
import hashlib
import json
import math
import re
import wave
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tokens(text):
    return re.findall(r"\w+", re.sub(r"[^\w\s]", "", text.casefold()))


def match(words, phrase, occurrence=0):
    needle = tokens(phrase)
    spoken = [word["word"].casefold() for word in words]
    hits = [i for i in range(len(words)) if spoken[i:i + len(needle)] == needle]
    if len(hits) <= occurrence:
        raise ValueError(f"Missing speech cue: {phrase!r} ({occurrence + 1})")
    return hits[occurrence]


def frame(seconds):
    return round(seconds * 30)


def edit_voice(scene, audio, words):
    # Cut in the existing gaps around the redundant phrases. Leave about a second
    # between the retained ideas and keep every retained speech sample intact.
    cuts = [(13.82, 15.72), (17.22, 19.52)]
    removed = "je divise les deux par trois", "je divise les deux par six"
    kept = []
    for start, end in cuts:
        assert any(start < w["start"] and w["end"] < end for w in words)
        assert not any(w["start"] < edge < w["end"] for w in words for edge in (start, end))
    for word in words:
        if not any(start <= word["start"] < end for start, end in cuts):
            offset = sum(end - start for start, end in cuts if end <= word["start"])
            kept.append({**word, **{key: round(word[key] - offset, 6) for key in ("start", "end")}})

    target = Path("public/fractions-review-2026-11-12") / audio.name
    (target.parent / "alignment").mkdir(parents=True, exist_ok=True)
    with wave.open(str(audio), "rb") as original:
        rate = original.getframerate()
        params = original.getparams()
        ranges = [(0, cuts[0][0]), (cuts[0][1], cuts[1][0]), (cuts[1][1], original.getnframes() / rate)]
        chunks = []
        for start, end in ranges:
            original.setpos(round(start * rate))
            chunks.append(original.readframes(round(end * rate) - round(start * rate)))
    with wave.open(str(target), "wb") as output:
        output.setparams(params)
        output.writeframes(b"".join(chunks))
    with wave.open(str(target), "rb") as output:
        samples = output.getnframes()
        assert output.readframes(samples) == b"".join(chunks)
    for index, phrase in zip((3, 4), removed):
        scene["beats"][index]["text"] = scene["beats"][index]["text"].removesuffix(": " + phrase + ".").rstrip() + "."
    scene["narration"] = " ".join(beat["text"] for beat in scene["beats"])
    assert tokens(scene["narration"]) == [w["word"].casefold() for w in kept]
    index = 0
    for beat in scene["beats"]:
        beat["from"] = frame(kept[index]["start"]) if index else 0
        index += len(tokens(beat["text"]))
    scene["durationInFrames"] = math.ceil((samples / rate + 0.9) * 30)
    scene["audio"] = target.relative_to("public").as_posix()
    scene["timingMethod"] = "MMS_FA known-transcript alignment, remapped after PCM cuts"
    signature = hashlib.sha256(target.read_bytes() + scene["narration"].encode()).hexdigest()
    receipt = read(Path(str(audio) + ".json"))
    write(Path(str(target) + ".json"), {
        **receipt,
        "signature": signature,
        "processing": "Two redundant phrases cut from the paced Kore recording; retained PCM samples unchanged",
        "sourceAudio": audio.relative_to("public").as_posix(),
        "removedSeconds": cuts,
    })
    write(target.parent / "alignment" / (scene["id"] + ".json"), {
        "signature": signature, "method": scene["timingMethod"], "words": kept,
    })
    return kept


timeline = read(Path("src/video/fractions-v2-lesson.json"))
for scene in timeline["scenes"]:
    audio = Path("public") / scene["audio"]
    alignment = read(audio.parent / "alignment" / (scene["id"] + ".json"))
    assert alignment["signature"] == hashlib.sha256(audio.read_bytes() + scene["narration"].encode()).hexdigest()
    words = alignment["words"]
    scene["revision"] = "2026-11-12"
    kind = scene["kind"]
    if kind == "reducible":
        words = edit_voice(scene, audio, words)

    def cue(name, phrase, occurrence=0):
        scene["cues"][name] = frame(words[match(words, phrase, occurrence)]["start"])

    def line(name, text, phrase, occurrence=0):
        index = match(words, phrase, occurrence)
        pieces = text.split()
        scene.setdefault("reveals", {})[name] = [
            {"text": piece, "from": frame(words[index + i]["start"])}
            for i, piece in enumerate(pieces)
        ]

    if kind in ("irreducible", "reducible"):
        cue("question", "Est-ce que")
        if kind == "irreducible":
            cue("numerator", "vingt-trois", 1)
            cue("denominator", "quarante et un", 1)
            cue("conclusion", "est irréductible")
            line("conclusion", "est irréductible", "est irréductible")
        else:
            cue("division2", "deux", 0)
            cue("division3", "trois")
            cue("division6", "six")
            cue("gcd", "six", 1)
            line("conclusion", "est réductible par 6", "est réductible par six")
    elif kind == "definition":
        line("fractionLabel", "Une fraction", "Une fraction")
        cue("fraction", "a sur b")
        line("irreducible", "est irréductible", "est irréductible")
        line("condition", "si et seulement si a et b", "si et seulement si a et b")
        line("coprime", "sont premiers entre eux.", "sont premiers entre eux")
    elif kind == "property":
        line("first", "Le plus petit dénominateur commun", "Le plus petit dénominateur commun")
        line("second", "de deux fractions est le PPCM", "de deux fractions est le plus petit commun multiple")
        line("third", "de leurs deux dénominateurs.", "de leurs deux dénominateurs")
    elif kind == "denominator":
        cue("formula", "plus petit commun multiple")
        cue("formulaResult", "quarante-cinq")
        cue("chosen", "quarante-cinq", 1)
        # “Comme plus petit…” in the narration corresponds to “est le plus petit…” on screen.
        line("result", "plus petit dénominateur commun", "plus petit dénominateur commun")
        result = scene["reveals"]["result"]
        same = frame(words[match(words, "comme plus petit")]["start"])
        scene["reveals"]["result"] = [
            {"text": "45", "from": scene["cues"]["chosen"]},
            {"text": "est", "from": same}, {"text": "le", "from": same}, *result,
        ]
        cue("fractionLead", "des deux fractions")
        cue("fractionPair", "fractions")
    elif kind == "vocabulary":
        cue("vocabularyOne", "un sur deux")
        cue("vocabularyTwo", "trois sur quatre")
        cue("denominator", "deux", 1)

write(Path("src/video/fractions-review-lesson.json"), timeline)
print(f"Fractions review: {sum(s['durationInFrames'] for s in timeline['scenes']) / 30:.3f} s")
