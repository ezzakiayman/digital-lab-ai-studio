"""Reviewed storyboard plans for 2AC week 1, VDP3 and VDP4."""
import argparse
import json
from pathlib import Path
import runpy
import wave

from PIL import ImageFont

VIDEO = Path("src/video")
PUBLIC = Path("public")
RAW = "n2-sem1"
PLAN = VIDEO / "n2-sem1-plan.json"
VOICE = VIDEO / "n2-sem1-kore-plan.json"
ARABIC = VIDEO / "n2-sem1-arabic-plan.json"
PACED = VIDEO / "n2-sem1-paced-plan.json"
RUNTIME = runpy.run_path("scripts/prepare-n3-sem3.py")
art, text, mathline = (RUNTIME[name] for name in ("art", "text", "mathline"))
BLUE, RED, GREEN, PURPLE, ORANGE = (RUNTIME[name] for name in ("BLUE", "RED", "GREEN", "PURPLE", "ORANGE"))
TITLES = {3: "Résoudre l’équation x² = a, a > 0", 4: "Identifier les éléments d’un monôme"}
SOURCES = {3: 13, 4: 17}
ARABIC_WORD = "يَتَعَرَّف"
ARABIC_BEFORE = "En arabe,"
ARABIC_AFTER = "c’est l’idée de reconnaître."


def scene(episode, name, start, end, label, beats, *visuals, kind="teaching", **options):
    beats = [part.strip() for part in beats.split("|")]
    key = f"n2-sem1-vdp{episode}-{name}"
    return dict(episode=episode, id=key, type="vdp-sequence", kind=kind, title=label, speechMode="verbatim",
                audio=f"{RAW}/{key}.wav", narration=" ".join(beats), art=list(visuals), cues={},
                sourceSlides=list(range(start, end+1)),
                beats=[dict(stage=i, text=part, **{"from": 0}) for i, part in enumerate(beats)], **options)


def algebra(value, y, at=0, size=82, x=960, **options):
    return art("algebra", value, y, at, size, x, **options)


def arrow(direction, x, y, at, size=80, **options):
    return art("arrow", direction, y, at, size, x, color=ORANGE, draw=True, **options)


def color(value, ink):
    return rf"\textcolor{{{ink}}}{{{value}}}"


def math_word(value, y, at, size, x):
    return mathline(value, y, at, size, x)


def pronunciation(episode, slide, word, syllables, spoken, intro, *, retake=None):
    repeat = word.lower() if retake else word
    item = scene(episode, "prononciation-"+str(slide), slide, slide, "Vocabulaire",
                 " | ".join([intro, *(part+"." for part in spoken), word+". Maintenant, répétez : "+repeat+"."]),
                 kind="pronunciation", pronunciation=dict(word=word, syllables=syllables))
    if retake:
        item["audio"] = f"{RAW}/retakes/{retake}.wav"
    return item


def equation_objective():
    title = "Résoudre l’équation"
    expression = "x² = a, a > 0"
    title_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 64)
    math_font = ImageFont.truetype("C:/Windows/Fonts/cambria.ttc", 64, index=1)
    first = round(title_font.getlength(title))
    offset = round(title_font.getlength(title+"  "))
    width = round(math_font.getlength("𝒙² = 𝒂, 𝒂 > 0"))
    return scene(3, "objectif", 1, 3, "Déclaration de l’objectif",
                 "Bonjour. Aujourd’hui, vous serez capables de résoudre l’équation : x au carré est égal à a, avec a supérieur à zéro. | "
                 "Résoudre une équation, c’est trouver les valeurs de x qui rendent l’égalité vraie. | "
                 "Voici quelques exemples d’équations : | x au carré est égal à vingt-cinq, | puis x au carré est égal à dix-neuf.",
                 kind="intro", objective=dict(title=title, mathSuffix=expression, mathOffset=offset, measure=offset+width,
                    size=68, links=[
                      dict(offset=0,width=first,at=1,art=[
                        text("Trouver les valeurs", 694, size=55),
                        text("de", 787, size=53, x=928), algebra("x", 787, size=64, x=991)]),
                      dict(offset=offset,width=width,at=2,art=[
                        algebra("x² = 25", 687, 3, 74),
                        algebra("x² = 19", 814, 4, 74)])
                    ]))


def equation_worked():
    result = scene(3, "resoudre", 4, 10, "Définition",
        "A est un nombre positif. | Résoudre l’équation x au carré est égal à a, | c’est trouver les nombres qui, élevés au carré, donnent a. | "
        "Je prends un premier exemple : | x au carré est égal à trente-six. Je cherche les nombres qui ont trente-six pour carré. | "
        "À votre avis, quels nombres ont pour carré trente-six ? | Il y a six | et moins six. Ce sont donc deux solutions. | "
        "Je vérifie : six au carré est égal à trente-six, | et le carré de moins six est aussi égal à trente-six. Voilà pourquoi les deux nombres conviennent. | "
        "Je passe au deuxième exemple : x au carré est égal à deux. Cette fois, je cherche les nombres dont le carré est égal à deux. | "
        "Les deux solutions sont racine carrée de deux | et moins racine carrée de deux. Ces deux nombres sont opposés. | "
        "Je peux les vérifier : le carré de racine carrée de deux est égal à deux. | Le carré de moins racine carrée de deux est également égal à deux. Les deux valeurs conviennent donc.",
        mathline(r"a\text{ est un nombre positif.}", 350, 0, 53),
        text("Résoudre l’équation", 424, 1, 53, 760, color="#8A4B0B", weight=700),
        algebra("x² = a", 424, 1, 62, 1190),
        mathline(r"\text{c’est trouver les nombres qui, élevés au carré, }\textcolor{#66539F}{\text{donnent }a}\text{.}", 498, 2, 46, color="#006189"),
        arrow("down", 335, 554, 3, 58),
        text("Exemple :", 615, 3, 44, 335, weight=700),
        algebra("x² = 36", 714, 4, 68, 480, tokenColors=[
            dict(index=5, at=4, color=RED), dict(index=6, at=4, color=RED)
        ]),
        art("question", "", 714, 5, 117, 900, to=6),
        mathline("6", 714, 6, 73, 795),
        text("et", 714, 7, 51, 909),
        mathline("-6", 714, 7, 73, 1024),
        mathline(r"6^2="+color("36",RED), 675, 8, 60, 1400),
        mathline(r"(-6)^2="+color("36",RED), 750, 9, 60, 1400),
        algebra("x² = 2", 897, 10, 68, 480, tokenColors=[dict(index=5, at=10, color=RED)]),
        mathline(r"\sqrt{2}", 897, 11, 68, 795),
        text("et", 897, 12, 51, 909),
        mathline(r"-\sqrt{2}", 897, 12, 68, 1024),
        mathline(r"(\sqrt 2)^2="+color("2",RED), 861, 13, 58, 1400),
        mathline(r"(-\sqrt 2)^2="+color("2",RED), 939, 14, 58, 1400),
    )
    result["beats"][5]["pauseAfter"] = 2.0
    return result


def vdp3():
    return [
        equation_objective(),
        equation_worked(),
        scene(3, "vocabulaire", 11, 12, "Vocabulaire",
              "Pour terminer, je retiens le mot résoudre. Résoudre une équation, c’est chercher les valeurs qui rendent l’égalité vraie. | "
              "Et le deuxième mot, c’est équation. Une équation est une égalité contenant une inconnue. Ce sont les deux mots essentiels de cette séance.",
              art("card", "Résoudre", 605, 0, 56, 610), art("card", "Équation", 605, 1, 56, 1310)),
        pronunciation(3,13,"Résoudre",["ré","soudre"],["Ré","Zoudre"],"Écoutez le mot résoudre. Écoutez les syllabes."),
    ]


def monomial_tokens(at):
    return [dict(index=i, at=at, color=ink) for i,ink in [(0,BLUE),(1,RED),(3,RED)]]


def vdp4():
    arabic_phrase = f"{ARABIC_BEFORE} {ARABIC_WORD}, {ARABIC_AFTER}"
    return [
        scene(4, "objectif", 1, 3, "Déclaration de l’objectif",
              "Bonjour. Aujourd’hui, je vais vous expliquer comment identifier les éléments d’un monôme. | "
              f"Identifier, c’est reconnaître ou repérer quelque chose. | {arabic_phrase} | "
              "Et le mot monôme désigne ici une expression comme | quatre fois x au carré fois y. Je vais apprendre à en distinguer les éléments.",
              kind="intro", objective=RUNTIME["objective_art"](TITLES[4], (
                  ("Identifier",1,text("يتعرف",716,2,85,rtl=True)),
                  ("les éléments d’un monôme",3,algebra("4x²y",724,4,100)),
              ))),
        pronunciation(4,4,"Monôme",["mo","nôme"],["Mo","Nôme"],"Écoutez les syllabes du mot monôme.", retake="monome"),
        scene(4, "definition-monome", 5, 9, "Définition 1",
              "Première définition : | un monôme est une expression algébrique à un seul terme. Cela veut dire qu’il s’agit d’un seul terme, et non d’une somme de plusieurs termes. | "
              "Prenons quatre fois x au carré fois y au cube. Il n’y a qu’un seul terme. | C’est donc bien un monôme. | "
              "En revanche, deux fois x plus y contient deux termes, séparés par une addition. | Ce n’est pas un monôme. | "
              "Dans le monôme quatre fois x au carré fois y au cube, | quatre est le coefficient. C’est le nombre qui multiplie les lettres. | "
              "Et x et y sont les variables : ce sont les lettres auxquelles je peux donner différentes valeurs.",
              text("Un monôme est une expression algébrique", 371, 1, 56),
              text("à un seul terme.", 451, 1, 60, weight=700, color=BLUE),
              arrow("down", 960, 525, 2, 60),
              algebra("4x²y³", 622, 2, 84, 575, background="#D9F3FB"),
              mathline(r"\checkmark", 625, 3, 65, 792, color=GREEN),
              algebra("2x + y", 622, 4, 84, 1240, background="#EDE3F7"),
              art("status", "Faux", 622, 5, 38, 1525, color=RED),
              text("Dans le monôme", 740, 6, 49, 748),
              algebra("4x²y³", 740, 6, 67, 1118, tokenColors=monomial_tokens(7)),
              mathline(color("4",BLUE)+r"\text{ est le coefficient.}", 848, 7, 56, 960),
              algebra("x", 940, 8, 63, 682, tokenColors=[dict(index=0,at=8,color=RED)]),
              text("et", 940, 8, 49, 751),
              algebra("y", 940, 8, 63, 811, tokenColors=[dict(index=0,at=8,color=RED)]),
              text("sont les variables.", 940, 8, 54, 1094)),
        scene(4, "degre", 10, 12, "Définition 2",
              "Deuxième définition : le degré du monôme est | la somme des exposants de ses variables. Je dois donc m’intéresser aux exposants des lettres. | "
              "Le degré du monôme quatre fois x au carré fois y au cube est… | Je repère l’exposant deux de x | et l’exposant trois de y. | "
              "J’additionne ces exposants : deux plus trois | est égal à cinq. Le degré de ce monôme est donc cinq.",
              text("Le degré du monôme est", 375, 0, 59, weight=700),
              text("la somme des exposants de ses variables.", 466, 1, 58, color=BLUE),
              arrow("down", 960, 563, 2, 72),
              text("Le degré du monôme", 679, 2, 53, 655),
              algebra("4x²y³", 680, 2, 101, 1116,
                      tokenColors=[*monomial_tokens(2), dict(index=2,at=3,color=BLUE), dict(index=4,at=4,color=BLUE)],
                      tokenMarks=[dict(index=2,at=3),dict(index=4,at=4)]),
              text("est :", 679, 2, 53, 1380),
              mathline(color("2",BLUE)+"+"+color("3",BLUE), 859, 5, 106, 860),
              mathline("="+color("5",GREEN), 859, 6, 106, 1143)),
        pronunciation(4,13,"Degré",["de","gré"],["De","Gré"],"Écoutez les syllabes du mot degré.", retake="degre"),
        scene(4, "vocabulaire", 14, 17, "Vocabulaire",
              "Pour terminer, je retiens du vocabulaire important. D’abord, monôme : une expression algébrique à un seul terme. | "
              "Ensuite, variable : une lettre qui peut prendre différentes valeurs. | "
              "Puis, coefficient : le nombre qui multiplie les variables dans le monôme. | "
              "Enfin, degré : la somme des exposants des variables. Ces quatre mots m’aident à identifier les éléments d’un monôme.",
              art("card", "Monôme", 474, 0, 55, 595), art("card", "Variable", 474, 1, 55, 1325),
              art("card", "Coefficient", 752, 2, 55, 595), art("card", "Degré", 752, 3, 55, 1325)),
    ]


def prepare():
    lessons = vdp3()+vdp4()
    for episode, count in SOURCES.items():
        assert [n for item in lessons if item["episode"]==episode for n in item["sourceSlides"]] == list(range(1,count+1))
    RUNTIME["write"](PLAN, dict(scenes=lessons))
    french, arabic = [], []
    for item in lessons:
        def clip(name, script):
            return dict(id=name, narration=script, speechMode="verbatim", audio=f"{RAW}/{name}.wav")
        if ARABIC_WORD not in item["narration"]:
            french.append(dict(clip(item["id"], item["narration"]), audio=item["audio"]))
            continue
        before, after = item["narration"].split(ARABIC_WORD)
        french += [clip(item["id"]+"-avant", before.strip()), clip(item["id"]+"-apres", after.lstrip(", "))]
        arabic.append(dict(clip(item["id"]+"-ar", ARABIC_WORD), languageCode="ar", speed=.94, stability=.45))
    RUNTIME["write"](VOICE,dict(scenes=french))
    RUNTIME["write"](ARABIC,dict(scenes=arabic))
    print(f"{len(lessons)} scènes et {sum(SOURCES.values())} diapositives, {len(french)} prises françaises")


def assemble(before_end=None):
    item = next(s for s in json.loads(PLAN.read_text(encoding="utf-8"))["scenes"] if ARABIC_WORD in s["narration"])
    target = PUBLIC / item["audio"]
    clips = [target.with_name(target.stem+"-"+tag+".wav") for tag in ("avant","ar","apres")]
    pcm = []
    for path in clips:
        with wave.open(str(path)) as source:
            assert (source.getnchannels(),source.getsampwidth(),source.getframerate())==(1,2,24000), path
            pcm.append(source.readframes(source.getnframes()))
    if before_end is not None:
        assert .2 < before_end < len(pcm[0]) / 48000
        pcm[0] = pcm[0][:2*round(before_end*24000)]
    gap = bytes(round(.24*24000)*2)
    with wave.open(str(target),"wb") as combined:
        combined.setparams((1,2,24000,0,"NONE","not compressed"))
        combined.writeframes(gap.join(pcm))
    french, middle = [json.loads(Path(str(p)+".json").read_text(encoding="utf-8")) for p in clips[:2]]
    RUNTIME["write"](Path(str(target)+".json"),dict(provider="gemini",model=french["model"],voice=french["voice"],
                       arabicProvider=middle["provider"],arabicModel=middle["model"],arabicVoice=middle["voice"],
                       arabicStartSample=(len(pcm[0])+len(gap))//2,arabicSamples=len(pcm[1])//2,
                       parts=[p.as_posix() for p in clips], beforeEndSeconds=before_end))
    print("Prise arabe insérée dans l’objectif de la VDP4")


def timeline():
    plan = json.loads(PACED.read_text(encoding="utf-8"))
    results = {i:dict(version=1,lesson=title,level="2AC",videoType="VDP",fps=30,scenes=[]) for i,title in TITLES.items()}
    RUNTIME["finish_timeline"](plan,results,prefix="n2-sem1-vdp",counts=SOURCES)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=("prepare","assemble","timeline"))
    parser.add_argument("--before-end",type=float,help="Reviewed end of the French prefix in seconds")
    args=parser.parse_args()
    if args.step=="assemble":
        assemble(args.before_end)
    else:
        {"prepare":prepare,"timeline":timeline}[args.step]()
