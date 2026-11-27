"""Reviewed Remotion plans for the 1AC SEM2 VDP3 and VDP4 storyboards."""
import argparse
import json
from pathlib import Path
import runpy


VIDEO = Path("src/video")
RUNTIME = runpy.run_path("scripts/prepare-n3-sem3.py")
art, text, mathline, mark = (RUNTIME[name] for name in ("art", "text", "mathline", "mark"))
RED, BLUE, GREEN, PURPLE = (RUNTIME[name] for name in ("RED", "BLUE", "GREEN", "PURPLE"))
TITLES = {3: "Utiliser la commutativité et l’associativité de l’addition",
          4: "Effectuer la soustraction de nombres entiers"}
COUNTS = {3: 30, 4: 19}


def scene(episode, name, slides, title, script, *visuals, kind="teaching", **options):
    beats = script.split(" | ")
    key = f"vdp{episode}-{name}"
    return dict(episode=episode, id=key, type="vdp-sequence", kind=kind, title=title,
                narration=" ".join(beats), speechMode="verbatim", audio=f"n1-sem2/{key}.wav",
                sourceSlides=list(slides), art=list(visuals), cues={},
                beats=[dict(stage=i, text=part, **{"from": 0}) for i, part in enumerate(beats)], **options)


def objective(episode, last, script, *links):
    return scene(episode, "objectif", range(1, last+1), "Déclaration de l’objectif", script, kind="intro",
                 objective=RUNTIME["objective_art"](TITLES[episode], links))


def pronounce(episode, slide, word, printed, spoken):
    phrase = f"Écoutez la prononciation du mot « {word} »."
    script = " | ".join([phrase, *(syllable+"." for syllable in spoken), word+"."])
    return scene(episode, f"prononciation-{slide}", [slide], "Vocabulaire", script, kind="pronunciation",
                 pronunciation=dict(word=word, syllables=printed))


def colored(color, value):
    return rf"\textcolor{{{color}}}{{{value}}}"


def arrow(direction, x, y, at, color, size=82, **options):
    return art("arrow", direction, y, at, size, x, color=color, **options)


def addition():
    left = colored(BLUE, "(-2)") + "+" + colored(PURPLE, "(+5)")
    right = colored(PURPLE, "(+5)") + "+" + colored(BLUE, "(-2)")
    grouping_left, grouping_right = r"[(-4)+(+3)]+(-2)", r"(-4)+[(+3)+(-2)]"
    bracket_left = rf"\underbrace{{[(-4)+(+3)]}}_{{{colored(RED, '-1')}}}+(-2)"
    bracket_right = rf"(-4)+\underbrace{{[(+3)+(-2)]}}_{{{colored(RED, '+1')}}}"
    return [
        objective(3, 3, "Bonjour ! Aujourd’hui, vous allez apprendre à utiliser la commutativité et l’associativité de l’addition pour faciliter les calculs. | Ici, utiliser signifie appliquer une propriété pour faciliter un calcul. | La commutativité et l’associativité sont deux propriétés de l’addition que nous allons découvrir au cours de cette séance.",
                  ("Utiliser", 1, text("Appliquer une propriété", 671, size=38),
                   text("pour faciliter un calcul", 723, size=38)),
                  ("la commutativité et l’associativité", 2)),
        scene(3, "commutativite", range(4, 6), "Propriété 1",
              "Je commence par la première propriété : la commutativité. | Si je change l’ordre des termes dans une addition, la somme ne change pas. | Je dis que l’addition est commutative.",
              text("La commutativité", 387, size=53, weight=700, color=BLUE),
              text("Si je change l’ordre des termes dans une addition,", 550, 1, 50),
              text("la somme ne change pas.", 626, 1, 55, weight=700),
              text("Je dis que l’addition est commutative.", 807, 2, 49)),
        scene(3, "ordre-des-termes", range(6, 14), "Exemple",
              "Je prends l’exemple suivant : moins deux auquel j’ajoute plus cinq. | Je change l’ordre des deux termes. J’obtiens : plus cinq auquel j’ajoute moins deux. | Est-ce que le résultat change ? | Je calcule les deux sommes pour vérifier. | Moins deux plus cinq est égal à trois. | Plus cinq auquel j’ajoute moins deux est également égal à trois. | Les deux sommes sont donc égales. | Même si je change l’ordre des termes, la somme ne change pas. C’est la commutativité de l’addition.",
              mathline(left, 510, x=550, to=3), mathline(right, 510, 1, x=1370, to=3),
              mark("question", 752, 2, 190, to=3),
              mathline(left + r"\;=\;?", 510, 3, 76, 550, to=4),
              mathline(right + r"\;=\;?", 510, 3, 76, 1370, to=5),
              mathline(rf"\underbrace{{{left}}}_{{{colored(RED, '3')}}}", 568, 4, 77, 550, to=6, pulse=5),
              mathline(rf"\underbrace{{{right}}}_{{{colored(RED, '3')}}}", 568, 5, 77, 1370, to=6, pulse=5),
              mathline(left + "=" + right, 572, 6, 85),
              arrow("right", 960, 412, 7, BLUE, 440), arrow("left", 960, 729, 7, PURPLE, 440)),
        scene(3, "associativite", range(14, 16), "Propriété 2",
              "Je passe maintenant à la deuxième propriété : l’associativité. | La somme de plusieurs nombres ne change pas si je change le groupement de ces nombres. | Je dis que l’addition est associative.",
              text("L’associativité", 387, size=53, weight=700, color=BLUE),
              text("La somme de plusieurs nombres ne change pas", 550, 1, 51),
              text("si je change le groupement de ces nombres.", 626, 1, 51, weight=700),
              text("Je dis que l’addition est associative.", 807, 2, 49)),
        scene(3, "groupement-des-termes", range(16, 26), "Exemple",
              "Je prends moins quatre, plus trois, puis j’ajoute moins deux. | Je change le regroupement des termes en gardant leur ordre. | Est-ce que le résultat change ? | Je calcule les deux sommes pour vérifier. | Dans la première expression, moins quatre plus trois est égal à moins un. | J’additionne ensuite moins un et moins deux. J’obtiens moins trois. | Dans la deuxième expression, plus trois et moins deux donnent plus un. | J’additionne ensuite moins quatre et plus un. J’obtiens moins trois. | Les deux expressions sont donc égales. | Même si je change le regroupement des termes, la somme ne change pas. C’est l’associativité de l’addition.",
              mathline(grouping_left, 449, size=70, to=3), mathline(grouping_right, 661, 1, 70, to=3),
              mark("question", 832, 2, 130, to=3),
              mathline(grouping_left + r"\;=\;?", 449, 3, 68, to=4),
              mathline(grouping_right + r"\;=\;?", 724, 3, 68, to=6),
              mathline(bracket_left, 475, 4, 64, to=5),
              mathline(grouping_left + rf"={colored(RED, '(-1)')}+(-2)={colored(RED, '-3')}", 449, 5, 65, to=8),
              mathline(bracket_right, 739, 6, 64, to=7),
              mathline(grouping_right + rf"=(-4)+{colored(RED, '(+1)')}={colored(RED, '-3')}", 724, 7, 65, to=8),
              mathline(grouping_left + "=" + grouping_right, 554, 8, 77, to=9),
              mathline(colored(GREEN, r"[(-4)+(+3)]")+"+(-2)=(-4)+"+colored(GREEN, r"[(+3)+(-2)]"), 554, 9, 77)),
        pronounce(3, 26, "Commutativité", ["com", "mu", "ta", "ti", "vi", "té"], ["Comme", "Mu", "Ta", "Ti", "Vi", "Té"]),
        pronounce(3, 27, "Associativité", ["as", "so", "cia", "ti", "vi", "té"], ["A", "So", "Sia", "Ti", "Vi", "Té"]),
        scene(3, "synthese", range(28, 31), "Synthèse",
              "Nous avons découvert deux mots importants : commutativité et associativité. Rappelons leur signification. | La commutativité permet de changer l’ordre des termes d’une addition sans changer la somme. | L’associativité permet de changer le regroupement des termes d’une addition sans changer la somme.",
              art("card", "Commutativité", 448, size=47, x=514, pulse=1),
              art("card", "Associativité", 448, size=47, x=1406, pulse=2),
              arrow("down", 514, 569, 1, GREEN), arrow("down", 1406, 569, 2, GREEN),
              mathline("3+4=4+3", 684, 1, 64, 514),
              mathline(r"[(-2)+(+5)]+(+3)", 668, 2, 50, 1406),
              mathline(r"=(-2)+[(+5)+(+3)]", 754, 2, 50, 1406)),
    ]


def subtraction():
    first = r"(+7)\mathbin{-}(+10)"
    marked = r"(+7)\mathbin{\textcolor{#087746}{-}}(+10)"
    rewrite = marked + r"=(+7)\mathbin{\textcolor{#087746}{+}}"
    result = rewrite + colored(RED, "(-10)")
    return [
        objective(4, 2, "Bonjour ! Aujourd’hui, vous serez capables d’effectuer une soustraction de nombres entiers. | C’est calculer la différence entre deux nombres qui peuvent être positifs ou négatifs.",
                  ("Effectuer la soustraction de nombres entiers", 1, mathline(r"\ldots\;-\;\ldots\;=\;?", 703, size=80))),
        scene(4, "definition", range(3, 5), "Définition",
              "Je rappelle d’abord la définition de deux nombres opposés. | Deux nombres non nuls sont opposés s’ils ont la même valeur absolue | et des signes contraires.",
              text("Deux nombres opposés non nuls ont", 417, 1, 52, weight=700),
              text("la même valeur absolue", 588, 1, 62, color=BLUE),
              text("des signes contraires", 753, 2, 62, color=RED)),
        scene(4, "opposes", range(5, 11), "Exemple",
              "Je prends les nombres moins cinq et plus cinq. | Moins cinq est un nombre négatif. | Plus cinq est un nombre positif. | Ils ont donc des signes contraires. | Ils ont aussi la même valeur absolue : cinq. | L’opposé de moins cinq est plus cinq.",
              mathline("-5", 462, size=100, x=680, color=RED, to=5),
              text("et", 462, size=55, to=5), mathline("5", 462, size=100, x=1240, color=GREEN, to=5),
              arrow("down", 680, 566, 1, BLUE, to=3), arrow("down", 1240, 566, 2, BLUE, to=3),
              text("Négatif", 668, 1, 52, 680, color=RED, to=3),
              text("Positif", 668, 2, 52, 1240, color=GREEN, to=3),
              text("De signes contraires", 673, 3, 58, color=BLUE, to=4),
              arrow("down", 680, 581, 4, BLUE, to=5), arrow("down", 1240, 581, 4, BLUE, to=5),
              mathline("5", 714, 4, 78, 680, color=BLUE, to=5),
              mathline("5", 714, 4, 78, 1240, color=BLUE, to=5),
              mathline(r"\text{L’opposé de }" + colored(RED, "-5") + r"\text{ est }" + colored(GREEN, "5"), 621, 5, 83)),
        scene(4, "regle", range(11, 13), "Règle",
              "Je passe maintenant à la règle : soustraire un nombre. | Soustraire un nombre, c’est ajouter son opposé.",
              text("Soustraire un nombre", 416, size=54, color=BLUE, weight=700),
              text("Soustraire un nombre, c’est ajouter son opposé.", 630, 1, 51, weight=700)),
        scene(4, "soustraire-dix", range(13, 19), "Exemple",
              "Je prends comme exemple : plus sept moins plus dix. | Je regarde le signe de l’opération entre les deux nombres : c’est le signe moins. | Il s’agit donc d’une soustraction. | Je garde le premier nombre, plus sept, et je remplace la soustraction par une addition. | Je remplace ensuite plus dix par son opposé, moins dix. | J’obtiens : plus sept plus moins dix.",
              mathline(first, 521, size=96, to=1), mathline(marked, 521, 1, 96, to=3),
              mark("ring", 521, 1, 65, to=2, color=GREEN),
              text("Soustraction", 709, 2, 57, color=RED, to=3),
              mathline(rewrite + r"\;\ldots", 555, 3, 84, to=4), arrow("right", 967, 681, 3, BLUE, 280, to=4),
              mathline(result, 555, 4, 84, pulse=5), arrow("right", 1150, 681, 4, BLUE, 345, to=5)),
        pronounce(4, 19, "Soustraction", ["sous", "trac", "tion"], ["Sous", "Trac", "Sion"]),
    ]


def prepare():
    plan = addition() + subtraction()
    for episode, count in COUNTS.items():
        assert [n for item in plan if item["episode"] == episode for n in item["sourceSlides"]] == list(range(1, count+1))
    RUNTIME["write"](VIDEO / "n1-sem2-plan.json", dict(scenes=plan))
    print(f"Prepared {len(plan)} scenes from {sum(COUNTS.values())} slides")


def finish():
    plan = json.loads((VIDEO / "n1-sem2-paced-plan.json").read_text(encoding="utf-8"))
    timelines = {i: dict(version=1, lesson=title, level="1AC", videoType="VDP", fps=30, scenes=[])
                 for i, title in TITLES.items()}
    RUNTIME["finish_timeline"](plan, timelines, prefix="n1-sem2-vdp", counts=COUNTS)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", action="store_true")
    (finish if parser.parse_args().timeline else prepare)()
