"""Generate small batches of verbatim speech and split at aligned scene boundaries."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import wave

MANIFEST = Path("src/video/n3-sem3-plan.json")
BATCHES = Path("reference/n3-sem3/tts-batches.json")
PUBLIC = Path("public")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def word_count(phrase):
    return sum(bool(re.sub(r"[^\wً-ْٰ]", "", part)) for part in phrase.split())


def prepare(scenes, batches_path, audio_dir):
    groups = []
    buffer = []
    length = 0
    for scene in scenes:
        if (PUBLIC / scene["audio"]).exists():
            if buffer:
                groups.append(buffer)
                buffer = []
                length = 0
            continue
        count = word_count(scene["narration"])
        if buffer and (buffer[-1]["episode"] != scene["episode"] or length + count > 122):
            groups.append(buffer)
            buffer = []
            length = 0
        buffer.append(scene)
        length += count
    if buffer:
        groups.append(buffer)
    batches = []
    for group in groups:
        narration = " ".join(item["narration"] for item in group)
        key = "part-" + hashlib.sha256(narration.encode()).hexdigest()[:12]
        batches.append(dict(id=key, kind="teaching", speechMode="verbatim", narration=narration, audio=f"{audio_dir}/{key}.wav",
                            members=[item["id"] for item in group]))
    write(batches_path, dict(scenes=batches))
    print("TTS batches:", len(batches), flush=True)


def split(scenes, batches_path):
    lookup = {scene["id"]: scene for scene in scenes}
    for batch in read(batches_path)["scenes"]:
        audio = PUBLIC / batch["audio"]
        alignment_file = audio.parent / "alignment" / (batch["id"] + ".json")
        if not alignment_file.exists():
            continue
        alignment = read(alignment_file)
        assert alignment["signature"] == hashlib.sha256(audio.read_bytes() + batch["narration"].encode()).hexdigest()
        words = alignment["words"]
        receipt = read(Path(str(audio) + ".json"))
        with wave.open(str(audio)) as clip:
            params = clip.getparams()
            rate = clip.getframerate()
            width = clip.getsampwidth() * clip.getnchannels()
            pcm = clip.readframes(clip.getnframes())
        start = 0
        word = 0
        for idx, member in enumerate(batch["members"]):
            scene = lookup[member]
            word += word_count(scene["narration"])
            if idx == len(batch["members"]) - 1:
                assert word == len(words), (batch["id"], word, len(words))
                stop = len(pcm) // width
            else:
                left, right = words[word-1]["end"], words[word]["start"]
                assert left <= right, (member, left, right)
                stop = round((left + right) / 2 * rate)
            output = PUBLIC / scene["audio"]
            if not output.exists():
                output.parent.mkdir(parents=True, exist_ok=True)
                with wave.open(str(output), "wb") as clip:
                    clip.setparams(params)
                    clip.writeframes(pcm[start*width:stop*width])
                signature = hashlib.sha256((scene["narration"] + "|" + receipt["model"] + "|Kore|verbatim").encode()).hexdigest()
                write(Path(str(output) + ".json"), {**receipt, "signature": signature, "sourceBatch": batch["id"],
                                                     "sourceStartSample": start, "sourceEndSample": stop})
                print("Split:", member, f"{(stop-start)/rate:.2f}s", flush=True)
            start = stop


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare","split"])
    parser.add_argument("--plan", type=Path, default=MANIFEST)
    parser.add_argument("--batches", type=Path, default=BATCHES)
    parser.add_argument("--audio-dir", default="n3-sem3-batches")
    args = parser.parse_args()
    scenes = read(args.plan)["scenes"]
    if args.mode == "prepare":
        prepare(scenes, args.batches, args.audio_dir)
    else:
        split(scenes, args.batches)

