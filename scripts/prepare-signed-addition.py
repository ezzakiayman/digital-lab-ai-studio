"""Prepare and align the reviewed 1AC signed-addition storyboard."""
import argparse
import hashlib
import json
import math
import re
import wave
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--timeline", action="store_true")
args = parser.parse_args()
VIDEO = Path("src/video")


def tokens(text):
    return re.sub(r"[^\w\s]", "", text.casefold()).split()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


scene_data = [
    ("objectif", "intro", "Déclaration de l’objectif", 1, [
        "Bonjour ! Aujourd’hui, vous serez capables d’additionner avec la valeur absolue.",
        "Additionner, c’est calculer la somme. Le signe de l’addition est le signe plus.",
        "La valeur absolue d’un nombre est sa distance à zéro. Par exemple, la valeur absolue de moins cinq est cinq.",
    ]),
    ("regle-meme-signe", "same", "Règle 1", 4, [
        "Je commence par la première règle.",
        "Pour additionner deux nombres entiers de même signe,",
        "c’est-à-dire lorsque les deux nombres sont positifs,",
        "ou bien lorsque les deux nombres sont négatifs.",
        "Je garde le signe commun des deux nombres.",
        "C’est-à-dire le signe plus si les deux nombres sont positifs,",
        "et le signe moins s’ils sont négatifs.",
        "Ensuite, j’additionne leurs valeurs absolues.",
        "J’additionne les valeurs absolues : le carré et le triangle.",
    ]),
    ("regle-signes-contraires", "different", "Règle 2", 13, [
        "Je passe à la deuxième règle.",
        "Pour additionner deux nombres entiers de signes contraires,",
        "c’est-à-dire lorsque l’un est positif et l’autre négatif.",
        "Si leurs valeurs absolues sont différentes, je garde le signe du nombre ayant la plus grande valeur absolue.",
        "Le grand carré représente la plus grande valeur absolue.",
        "Je garde donc son signe : le signe plus.",
        "Ici aussi, le grand carré représente la plus grande valeur absolue.",
        "Je garde donc son signe : le signe moins.",
        "Je soustrais la plus petite valeur absolue de la plus grande.",
        "Je soustrais la petite valeur absolue de la plus grande : le grand carré moins le petit carré.",
    ]),
    ("regle-nombres-opposes", "opposites", "Règle 3", 23, [
        "Je termine par la troisième règle.",
        "La somme de deux entiers opposés est toujours égale à zéro.",
        "J’observe plus un carré bleu, puis moins un carré bleu. Ces deux entiers sont opposés.",
        "La somme est donc égale à zéro.",
    ]),
]

if not args.timeline:
    plan = dict(version=1, lesson="Additionner avec la valeur absolue", level="1AC", videoType="VDP", fps=30, scenes=[])
    for name, kind, title, first, phrases in scene_data:
        plan["scenes"].append(dict(
            id=name, type="signed-addition", kind=kind, title=title,
            sourceSlides=list(range(first, first + len(phrases))),
            narration=" ".join(phrases), audio=f"signed-addition/{name}.wav",
            beats=[{"stage": i, "text": phrase, "from": 0} for i, phrase in enumerate(phrases)],
        ))
    write(VIDEO / "signed-addition-plan.json", plan)
else:
    plan = json.loads((VIDEO / "signed-addition-paced-plan.json").read_text(encoding="utf-8"))
    for scene in plan["scenes"]:
        audio = Path("public") / scene["audio"]
        data = json.loads((audio.parent / "alignment" / (scene["id"] + ".json")).read_text(encoding="utf-8"))
        assert data["signature"] == hashlib.sha256(audio.read_bytes() + scene["narration"].encode()).hexdigest()
        words = data["words"]
        offsets = []
        index = 0
        for beat in scene["beats"]:
            offsets.append(index)
            beat["from"] = round(words[index]["start"] * 30) if index else 0
            index += len(tokens(beat["text"]))
        assert index == len(words)
        with wave.open(str(audio)) as wav:
            scene["durationInFrames"] = math.ceil((wav.getnframes() / wav.getframerate() + .9) * 30)
        scene["cues"] = {}
        scene["timingMethod"] = "MMS_FA known-transcript alignment"

        def cue(name, phrase, stage, offset=0):
            start = offsets[stage]
            end = offsets[stage + 1] if stage + 1 < len(offsets) else len(words)
            needle = tokens(phrase)
            span = [w["word"].casefold() for w in words[start:end]]
            hit, = (i for i in range(len(span)) if span[i:i + len(needle)] == needle)
            scene["cues"][name] = round(words[start + hit + offset]["start"] * 30)

        if scene["kind"] == "intro":
            cue("plus", "signe plus", 1, 1)
            cue("negative", "moins cinq", 2)
            cue("absolute", "est cinq", 2, 1)
        if scene["kind"] == "same":
            cue("positive", "positifs", 2)
            cue("negative", "négatifs", 3)
            cue("commonPlus", "signe plus", 5, 1)
            cue("commonMinus", "signe moins", 6, 1)
            cue("square", "le carré", 8, 1)
            cue("triangle", "le triangle", 8, 1)
        if scene["kind"] == "different":
            cue("casePositive", "positif", 2)
            cue("caseNegative", "négatif", 2)
            cue("keepLarger", "je garde le signe", 3)
            cue("largePlus", "grand carré", 4)
            cue("keepPlus", "signe plus", 5, 1)
            cue("largeMinus", "grand carré", 6)
            cue("keepMinus", "signe moins", 7, 1)
            cue("difference", "grand carré moins le petit carré", 9, 2)
        if scene["kind"] == "opposites":
            cue("positive", "plus un carré", 2)
            cue("negative", "moins un carré", 2)
            cue("zero", "zéro", 3)
    write(VIDEO / "signed-addition-lesson.json", plan)
    print(f"Aligned signed addition: {sum(s['durationInFrames'] for s in plan['scenes']) / 30:.3f} seconds")
