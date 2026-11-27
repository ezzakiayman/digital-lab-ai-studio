"""Build the four teacher-reviewed 3AC week 3 timelines from the delivered V3."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import wave

VIDEO = Path("src/video")
PUBLIC = Path("public")
RAW = "n3-sem3-elevenlabs-v4-raw"
PACED = "n3-sem3-elevenlabs-v4-paced"
VOICE_PLAN = VIDEO / "n3-sem3-v4-voice-plan.json"
PACED_PLAN = VIDEO / "n3-sem3-v4-paced-plan.json"
RED = "#D60019"
SKY = "#007DAF"
BLACK = "#1D1D1D"

# Only scenes with revised speech are regenerated with the approved French voice.
VOICE_EDITS = {
    "vdp1-objectif": {1: "Reconnaître, c’est savoir."},
    "vdp2-objectif": {
        1: "Comparer, c’est utiliser l’un des symboles, supérieur à ou inférieur à.",
        2: None,
    },
    "vdp2-attention": {
        3: "Pourquoi ? Parce que le nombre sous la racine carrée doit être positif ou nul.",
    },
    "vdp2-vocabulaire": {2: "Je compare des racines carrées."},
    "vdp3-fraction-1": {
        1: "Son écriture décimale est zéro virgule zéro zéro un.",
        2: "Et dans le premier exemple, deux cent vingt-cinq sur dix au carré donne deux virgule vingt-cinq.",
    },
    "vdp3-decimale-en-fraction": {
        0: "Observons deux virgule neuf cent quatre-vingt-cinq. Son écriture décimale est finie. Pourquoi ?",
    },
    "vdp4-objectif": {
        2: "Voici quelques nombres : sept, zéro virgule vingt-cinq, moins trois sur quatre, la racine carrée de deux et pi.",
    },
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def base(number):
    return load(VIDEO / f"n3-sem3-vdp{number}-v3-lesson.json")


def words(text):
    return [word for token in text.split() if (word := re.sub(r"[^\wً-ْٰ]", "", token))]


def prepare_voice():
    targets = {scene["id"]: scene for i in range(1, 5) for scene in base(i)["scenes"]}
    for scene_id, changes in VOICE_EDITS.items():
        scene = targets[scene_id]
        phrases = [beat["text"] for beat in scene["beats"]]
        for index, value in changes.items():
            if index == len(phrases):
                phrases.append(value)
            else:
                phrases[index] = value
        phrases = [text for text in phrases if text is not None]
        yield dict(id=scene_id, kind=scene["kind"], narration=" ".join(phrases),
                   beats=[dict(text=text) for text in phrases], audio=f"{RAW}/{scene_id}.wav",
                   languageCode="fr", speed=.94, stability=.45)


def apply_voice(scene, plan):
    scene.update(narration=plan["narration"], audio=plan["audio"])
    audio = PUBLIC / scene["audio"]
    alignment = load(audio.parent / "alignment" / (scene["id"] + ".json"))
    assert alignment["signature"] == hashlib.sha256(audio.read_bytes() + scene["narration"].encode()).hexdigest()
    cursor = 0
    scene["beats"] = []
    for beat in plan["beats"]:
        scene["beats"].append(dict(stage=len(scene["beats"]), text=beat["text"], **{"from": round(alignment["words"][cursor]["start"] * 30) if cursor else 0}))
        cursor += len(words(beat["text"]))
    assert cursor == len(alignment["words"])
    with wave.open(str(audio)) as clip:
        scene["durationInFrames"] = math.ceil((clip.getnframes() / clip.getframerate() + scene["holdSeconds"]) * 30)



def word_frames(scene):
    path = PUBLIC / Path(scene["audio"]).parent / "alignment" / (scene["id"] + ".json")
    return load(path)["words"]


def cue(scene, beat, phrase, last=False, occurrence=1):
    start = sum(len(words(b["text"])) for b in scene["beats"][:beat])
    tokens = [word.lower() for word in words(scene["beats"][beat]["text"])]
    wanted = [word.lower() for word in words(phrase)]
    matches = [i for i in range(len(tokens)) if tokens[i:i + len(wanted)] == wanted]
    assert len(matches) >= occurrence, (scene["id"], phrase, tokens)
    index = start + matches[occurrence - 1] + (len(wanted) - 1 if last else 0)
    return round(word_frames(scene)[index]["start"] * 30)


def visual(kind, value, x, y, size, at=0, **extra):
    return dict(kind=kind, value=value, x=x, y=y, size=size, at=at, **extra)


def formula(value, x, y, size=90, at=0, **extra):
    return visual("math", value, x, y, size, at, **extra)


def label(value, x, y, size=56, at=0, **extra):
    return visual("text", value, x, y, size, at, **extra)


def root_diagram(y, at, timings):
    root, square, result, reverse = timings
    return [
        visual("number-node", r"\sqrt{a}", 565, y, 76, at, frame=root),
        visual("arrow", "right", 960, y-24, 598, at, frame=square, color=RED, draw=True),
        label("Mise au carré", 960, y-68, 41, at, frame=square, color=RED),
        visual("number-node", "a", 1355, y, 76, at, frame=result),
        visual("arrow", "left", 960, y+24, 598, at, frame=reverse, color="#007DBA", draw=True),
        label("Racine carrée", 960, y+71, 41, at, frame=reverse, color="#007DBA"),
    ]


def false_marker(formula_item):
    formula_item["value"] = formula_item["value"].removesuffix(r"\quad\textcolor{#D60019}{\times}")
    formula_item["x"] = 875
    options = {"to": formula_item["to"]} if "to" in formula_item else {}
    if "pulse" in formula_item:
        options["pulse"] = formula_item.pop("pulse")
    return visual("status", "Faux", 1395, formula_item["y"], 44, formula_item["at"], color=RED, **options)


def root_one(scenes):
    objective = scenes["objectif"]["objective"]
    item = objective["links"][0]["art"][0]
    item.update(value="Savoir", size=54)
    item.pop("rtl", None)

    s = scenes["definition"]
    s["art"] = s["art"][:2] + [
        formula(r"\sqrt{a}", 522, 584, 73, 1, frame=cue(s, 1, "Elle se note")),
        label("se lit « racine carrée de a »", 1024, 584, 53, 1, frame=cue(s, 1, "se lit")),
        *root_diagram(808, 2, (
            cue(s, 2, "Si je mets"),
            cue(s, 2, "au carré"),
            cue(s, 2, "j’obtiens a", last=True),
            cue(s, 3, "Dans l’autre sens"),
        )),
    ]
    s = scenes["carres-parfaits"]
    s["art"] = s["art"][:-1] + [
        formula(r"\sqrt{a}=\textcolor{#D60019}{?}", 518, 615, 96, 4, frame=cue(s, 4, "la racine carrée")),
        formula(r"\textcolor{#087746}{\Longrightarrow}", 929, 615, 96, 4, frame=cue(s, 4, "je cherche")),
        formula(r"\bigl(\textcolor{#D60019}{?}\bigr)^2=a", 1313, 615, 96, 4, frame=cue(s, 4, "mis au carré")),
    ]
    s = scenes["verification"]
    s["art"].append(false_marker(s["art"][1]))

    s = scenes["vocabulaire"]
    s["art"] = s["art"][:2] + root_diagram(749, 1, (
        cue(s, 1, "Le carré"),
        cue(s, 1, "de la racine carrée"),
        cue(s, 1, "égal à a", last=True),
        cue(s, 1, "Dans l’autre sens"),
    ))


def root_two(scenes):
    s = scenes["objectif"]
    links = s["objective"]["links"]
    links[0]["art"] = [links[0]["art"][1]]
    links[0]["art"][0].update(at=0)
    links[0]["art"][0].pop("pulse", None)
    links[1]["at"] = 2
    links[2]["at"] = 3

    s = scenes["propriete"]
    s["art"] = [
        label("Pour deux nombres positifs ou nuls a et b", 960, 416, 59, 1),
        formula(rf"\text{{Si }}\textcolor{{{SKY}}}{{a<b}}", 960, 590, 95, 1, frame=cue(s, 1, "si a")),
        formula(rf"\text{{Alors }}\textcolor{{{SKY}}}{{\sqrt{{a}}<\sqrt{{b}}}}", 960, 793, 95, 1, frame=cue(s, 1, "alors")),
    ]
    s = scenes["attention"]
    s["art"].append(false_marker(s["art"][-1]))

    s = scenes["vocabulaire"]
    # Keep each emphasis on the spoken expression itself.
    for art, beat, phrase in zip(s["art"], (1, 2, 3), ("Comparer", "racines carrées", "carré")):
        art.update(pulseFrame=cue(s, beat, phrase))
        art.pop("pulse")


def ring(target, start, stop):
    return dict(target=target, start=start, end=stop)


def fraction_example(numerator, power, y=558, **extra):
    return formula(rf"\frac{{{numerator}}}{{10^{power}}}", 588, y, 108, **extra)


def fraction_name(scene, fragment, y, to):
    return label("Une fraction décimale", 1110, y, 59, frame=cue(scene, 0, fragment), to=to)


def decimals(scenes):
    s = scenes["definition"]
    for item, phrase in zip(s["art"], ("Une fraction décimale", "est une fraction", "est une puissance")):
        item.update(at=1, frame=cue(s, 1, phrase), size=56, color=BLACK, weight=400)

    s = scenes["fraction-225"]
    annotated = r"\frac{225}{\htmlClass{vdp-math-denominator}{10^{\htmlClass{vdp-math-exponent}{2}}}}"
    s["art"] = [
        formula(annotated, 588, 558, 108, focus=[
            ring("denominator", cue(s, 1, "dénominateur"), s["beats"][2]["from"]),
            ring("exponent", cue(s, 4, "L’exposant deux"), s["beats"][5]["from"]),
        ]),
        fraction_name(s, "une fraction décimale", 558, 2),
        formula("225", 1110, 558, 100, 3, to=5, frame=cue(s, 3, "deux cent vingt-cinq")),
        visual("arrow", "left", 1110, 424, 215, 4, color=RED, to=5, draw=True,
               frame=cue(s, 4, "je déplace")),
        formula(r"=\;2{,}\textcolor{#D60019}{25}", 918, 558, 106, 5,
                frame=cue(s, 5, "deux virgule")),
    ]

    s = scenes["fraction-1"]
    first_result = cue(s, 1, "zéro virgule")
    second_result = cue(s, 2, "deux virgule vingt-cinq")
    s["art"] = [
        fraction_example(1, 3, 466),
        fraction_name(s, "une fraction décimale", 466, 1),
        formula("=", 766, 466, 106, 1, frame=first_result),
        formula(r"0{,}\textcolor{#D60019}{001}", 988, 466, 106, 1, frame=first_result),
        fraction_example(225, 2, 775, at=2, frame=cue(s, 2, "deux cent vingt-cinq")),
        formula("=", 766, 775, 106, 2, frame=second_result),
        formula(r"2{,}\textcolor{#D60019}{25}", 955, 775, 106, 2, frame=second_result),
    ]

    s = scenes["fraction-moins-5"]
    s["art"] = [
        fraction_example(-5, 0),
        fraction_name(s, "une fraction décimale", 558, 1),
        formula(r"=\;\textcolor{#D60019}{-5}", 918, 558, 106, 1,
                frame=cue(s, 1, "moins cinq")),
    ]

    s = scenes["propriete"]
    s["art"][0].update(size=58, color=BLACK)
    s["art"][1].update(size=58, color=BLACK, weight=400, frame=cue(s, 1, "s’écrit"))


def stable_decimal(scene, expression, digits, label_size=62):
    whole, fraction = digits.split("{,}", 1)
    formula_text = rf"{expression}={whole}{{,}}\htmlClass{{vdp-math-decimal}}{{{fraction}\ldots}}"
    scene["art"] = [
        formula(formula_text, 960, 453, 87, focus=[ring("decimal", 0, scene["beats"][1]["from"])]),
        *scene["art"][2:],
    ]
    scene["art"][1].update(size=label_size, y=642)
    scene["art"][-1].update(size=label_size)


def rationals(scenes):
    s = scenes["rationnels"]
    s["art"][2].update(value=r"a\text{ et }b\text{ des entiers}\qquad b\ne 0", size=68)
    s = scenes["rationnel-decimal"]
    s["art"] = [
        formula("2{,}25", 544, 505, 112),
        label("Une écriture décimale finie", 1120, 505, 61, frame=cue(s, 0, "une écriture décimale finie"), to=1),
        formula(r"=\;\frac{225}{100}", 1000, 505, 105, 1, frame=cue(s, 1, "égal")),
        s["art"][-1],
    ]
    stable_decimal(scenes["irrationnel-racine"], r"\sqrt{7}", "2{,}645751311064")
    stable_decimal(scenes["irrationnel-pi"], r"\pi", "3{,}141592653589")

    s = scenes["entiers"]
    s["art"][0].update(color=BLACK, size=59)
    for item in s["art"]:
        if item["kind"] == "text":
            item.update(size=59)
    scenes["droite-propriete"]["art"][-1].update(color=BLACK, size=53, weight=400)


def build_timelines():
    revised = {s["id"]: s for s in load(PACED_PLAN)["scenes"]}
    for number, update in enumerate((root_one, root_two, decimals, rationals), 1):
        timeline = base(number)
        scenes = {scene["id"].split("-", 1)[1]: scene for scene in timeline["scenes"]}
        for scene in scenes.values():
            if scene["id"] in revised:
                apply_voice(scene, revised[scene["id"]])
        update(scenes)
        write(VIDEO / f"n3-sem3-vdp{number}-v4-lesson.json", timeline)
        print(f"VDP{number}: {sum(s['durationInFrames'] for s in scenes.values()) / 30:.2f} s")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=("prepare", "timeline"))
    if parser.parse_args().step == "prepare":
        write(VOICE_PLAN, dict(scenes=list(prepare_voice())))
    else:
        build_timelines()


if __name__ == "__main__":
    main()
