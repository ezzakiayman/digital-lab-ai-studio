"""Prepare the ElevenLabs revision while retaining the original visual sequences."""
import argparse
import json
from pathlib import Path
import runpy

ROOT = Path("src/video")
SOURCE = ROOT / "n3-sem3-plan.json"
OUTPUT = ROOT / "n3-sem3-elevenlabs-plan.json"
PACED = ROOT / "n3-sem3-elevenlabs-paced-plan.json"
ORIGINAL = runpy.run_path("scripts/prepare-n3-sem3.py")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--timeline", action="store_true")
parser.add_argument("--episode", type=int, choices=ORIGINAL["episodes"])
parser.add_argument("--paced-plan", type=Path, default=PACED)
args = parser.parse_args()
if args.timeline:
    result = {
        i: dict(version=1, lesson=lesson, level="3AC", videoType="VDP", fps=30, scenes=[])
        for i, lesson in ORIGINAL["episodes"].items() if args.episode in (None, i)
    }
    ORIGINAL["finish_timeline"](json.loads(args.paced_plan.read_text(encoding="utf-8")), result, suffix="-v2")
else:
    plan = json.loads(SOURCE.read_text(encoding="utf-8"))
    count = 0
    for scene in plan["scenes"]:
        scene["audio"] = f"n3-sem3-elevenlabs/{scene['id']}.wav"
        # Use fully vocalized Arabic for the same two words shown in the storyboard.
        if scene["id"] == "vdp1-objectif":
            scene["beats"][1]["text"] = scene["beats"][1]["text"].replace("Ataâraf", "أَتَعَرَّفْ")
        if scene["id"] == "vdp2-objectif":
            scene["beats"][1]["text"] = scene["beats"][1]["text"].replace("Qaren", "قَارِنْ")
        scene["narration"] = " ".join(beat["text"] for beat in scene["beats"])
        count += len(scene["narration"])
    ORIGINAL["write"](OUTPUT, plan)
    print(f"Prepared {len(plan['scenes'])} scenes and {count} characters for the voice revision.")

