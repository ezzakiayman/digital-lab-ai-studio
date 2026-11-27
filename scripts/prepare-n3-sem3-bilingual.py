"""Prepare the validated French and standard Arabic narration for the four VDPs."""

import argparse
import json
from pathlib import Path
import re
import runpy
import wave


VIDEO = Path("src/video")
PUBLIC = Path("public")
SOURCE = VIDEO / "n3-sem3-elevenlabs-plan.json"
PLAN = VIDEO / "n3-sem3-bilingual-plan.json"
PACED = VIDEO / "n3-sem3-bilingual-paced-plan.json"
AUDIO = "n3-sem3-elevenlabs-bilingual"
FR_PLAN = PUBLIC / AUDIO / "french-plan.json"
AUDITION = PUBLIC / "n3-sem3-elevenlabs/voice-audition"
ARABIC = {"أَتَعَرَّفْ.": "ar-reconnaitre", "قَارِنْ.": "ar-comparer"}
ARABIC_TEXT = re.compile(r"[\u0600-\u06ff]+\.")
RUNTIME = runpy.run_path("scripts/prepare-n3-sem3.py")
VOICE = "05Y5uLueU3x8LrkGHu0H"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def prepare():
    plan = load(SOURCE)
    french = []
    for scene in plan["scenes"]:
        scene_id = scene["id"]
        scene["audio"] = f"{AUDIO}/{scene_id}.wav"
        narration = scene["narration"]
        arabic = ARABIC_TEXT.search(narration)
        if arabic:
            assert arabic[0] in ARABIC and not ARABIC_TEXT.search(narration, arabic.end()), scene_id
            parts = (("before", narration[:arabic.start()].strip()), ("after", narration[arabic.end():].strip()))
        else:
            parts = (("", narration),)
        for tag, text in parts:
            assert text
            name = f"{scene_id}-{tag}" if tag else scene_id
            french.append(dict(id=name, narration=text, audio=f"{AUDIO}/{name}.wav",
                               languageCode="fr", speed=.94, stability=.45))

    FR_PLAN.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME["write"](PLAN, plan)
    RUNTIME["write"](FR_PLAN, {"scenes": french})
    print(f"{len(french)} prises françaises · {sum(len(clip['narration']) for clip in french)} caractères")


def read_audio(path, model, language):
    receipt = load(Path(f"{path}.json"))
    assert (receipt["voice"], receipt["model"], receipt["languageCode"]) == (VOICE, model, language), path
    with wave.open(str(path)) as audio:
        assert (audio.getnchannels(), audio.getsampwidth(), audio.getframerate()) == (1, 2, 24000), path
        return audio.readframes(audio.getnframes())


def assemble():
    for scene in load(PLAN)["scenes"]:
        arabic = ARABIC_TEXT.search(scene["narration"])
        if not arabic:
            continue
        scene_id = scene["id"]
        output = PUBLIC / scene["audio"]
        before = output.with_name(f"{scene_id}-before.wav")
        after = output.with_name(f"{scene_id}-after.wav")
        sample = AUDITION / f"{ARABIC[arabic[0]]}.wav"
        gap = bytes(round(.30 * 24000) * 2)
        clips = (read_audio(before, "eleven_v4", "fr"), read_audio(sample, "eleven_flash_v2_5", "ar"),
                 read_audio(after, "eleven_v4", "fr"))
        with wave.open(str(output), "wb") as audio:
            audio.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
            audio.writeframes(gap.join(clips))
        RUNTIME["write"](Path(f"{output}.json"), {
            "provider": "elevenlabs", "voice": VOICE, "model": "eleven_v4", "languageCode": "fr",
            "parts": [str(clip.as_posix()) for clip in (before, sample, after)],
            "arabicModel": "eleven_flash_v2_5", "arabicLanguageCode": "ar",
            "arabicStartSample": (len(clips[0]) + len(gap)) // 2,
            "arabicSamples": len(clips[1]) // 2,
            "gapSeconds": .30,
        })
        print(f"{scene_id} : passage arabe repris de l’essai validé")


def build_timelines():
    timelines = {i: dict(version=1, lesson=lesson, level="3AC", videoType="VDP", fps=30, scenes=[])
                 for i, lesson in RUNTIME["episodes"].items()}
    RUNTIME["finish_timeline"](load(PACED), timelines, suffix="-v3")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=("prepare", "assemble", "timeline"))
    action = parser.parse_args().step
    {"prepare": prepare, "assemble": assemble, "timeline": build_timelines}[action]()
