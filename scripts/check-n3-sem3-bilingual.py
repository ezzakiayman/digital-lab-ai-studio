"""Verify the 3AC week 3 voice revision against the source timelines and encoded MP4s."""

import argparse
import json
from pathlib import Path
import subprocess
import wave

import numpy as np


RATE = 24000
TIMING_FIELDS = {"audio", "durationInFrames", "holdSeconds", "timingMethod", "beats"}
SOURCE = Path("src/video")
PUBLIC = Path("public")
OUTPUT = Path("outputs/n3-sem3-v3")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def samples(path, start=0, count=-1):
    with wave.open(str(path), "rb") as audio:
        assert (audio.getframerate(), audio.getsampwidth(), audio.getnchannels()) == (RATE, 2, 1)
        audio.setpos(start)
        return np.frombuffer(audio.readframes(count), dtype="<i2")


def match_audio(track, source, start):
    expected = source.astype(np.float32)
    tolerance = RATE // 15
    view = track[max(0, start - tolerance):start + expected.size + tolerance]
    correlation = np.correlate(view, expected, mode="valid")
    index = int(correlation.argmax())
    actual = view[index:index + expected.size]
    score = float(np.dot(actual, expected) / (np.linalg.norm(actual) * np.linalg.norm(expected)))
    assert score >= .97, (start / RATE, score)
    return round(score, 4)


def verify(episode):
    stem = f"n3-sem3-vdp{episode}"
    folder = OUTPUT / f"vdp{episode}"
    before = load(SOURCE / f"{stem}-v2-lesson.json")
    after = load(folder / "timeline.json")
    assert len(before["scenes"]) == len(after["scenes"])
    movie = folder / f"P1_MATHS_N3_SEM3_VDP{episode}_V3.mp4"
    pcm = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(movie), "-map", "0:a:0",
                                   "-ac", "1", "-ar", str(RATE), "-f", "f32le", "-"])
    track = np.frombuffer(pcm, dtype="<f4")
    report = []
    offset = 0
    for prior, scene in zip(before["scenes"], after["scenes"]):
        assert {k: v for k, v in prior.items() if k not in TIMING_FIELDS} == {
            k: v for k, v in scene.items() if k not in TIMING_FIELDS
        }, scene["id"]
        assert [b["text"] for b in prior["beats"]] == [b["text"] for b in scene["beats"]], scene["id"]
        audio = PUBLIC / scene["audio"]
        receipt = load(Path(f"{audio}.json"))
        assert receipt["model"] == "eleven_v4" and receipt["languageCode"] == "fr", scene["id"]
        entry = {"scene": scene["id"], "encodedAudioMatch": match_audio(track, samples(audio, count=RATE), offset)}
        if receipt.get("arabicModel"):
            assert receipt["arabicModel"] == "eleven_flash_v2_5" and receipt["arabicLanguageCode"] == "ar"
            original = samples(Path(receipt["parts"][1]))
            start = receipt["arabicStartSample"]
            aligned = load(audio.parent / "alignment" / f"{scene['id']}.json")
            paced = start + sum(gap["frames"] for gap in aligned["pauseEdits"] if gap["sample"] <= start)
            assert np.array_equal(samples(audio, paced, original.size), original), scene["id"]
            entry["approvedArabicClipMatch"] = match_audio(track, original, offset + paced)
            entry["arabicStartSeconds"] = (offset + paced) / RATE
            entry["arabicDurationSeconds"] = original.size / RATE
        report.append(entry)
        offset += scene["durationInFrames"] * (RATE // 30)
    (folder / "voice-verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"VDP{episode}: {len(report)} séquences vérifiées, contenu et voix encodée", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episodes", type=int, choices=range(1, 5), nargs="*")
    for selected in parser.parse_args().episodes or range(1, 5):
        verify(selected)
