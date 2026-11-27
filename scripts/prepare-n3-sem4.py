"""Reviewed plans for the two available 3AC week 4 VDPs."""
import argparse
import json
import math
from pathlib import Path
import re
import runpy

RUNTIME = runpy.run_path("scripts/prepare-n3-sem3.py")
art, text, mathline = (RUNTIME[name] for name in ("art", "text", "mathline"))
VIDEO = Path("src/video")
PLAN = VIDEO / "n3-sem4-plan.json"
PACED = VIDEO / "n3-sem4-paced-plan.json"
VOICE_PLAN = VIDEO / "n3-sem4-voice-plan.json"
INK = "#1D1D1D"
RED, BLUE, GREEN = "#D60019", "#007DBA", "#087746"
TITLES = {
    1: "Reconnaître et appliquer le produit de deux racines carrées",
    2: "Reconnaître et appliquer le quotient de deux racines carrées",
}
FORMULAS = {
    1: r"\sqrt{a}\times\sqrt{b}=\sqrt{a\times b}",
    2: r"\frac{\sqrt{a}}{\sqrt{b}}=\sqrt{\frac{a}{b}}",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    RUNTIME["write"](path, data)


def scene(ep, name, first, last, title, speech, *visuals, kind="teaching", **extra):
    parts = [p.strip() for p in speech.split("|")]
    assert all(parts)
    key = f"n3-sem4-vdp{ep}-{name}"
    return dict(episode=ep,id=key,type="vdp-sequence",kind=kind,title=title,speechMode="verbatim",
                audio=f"n3-sem4/{key}.wav",narration=" ".join(parts),sourceSlides=list(range(first,last+1)),
                art=list(visuals),cues={},beats=[dict(stage=i,text=p,**{"from":0}) for i,p in enumerate(parts)],
                **extra)


def arrow(y, beat):
    return art("arrow","down",y,beat,64,color="#E78318",draw=True)


def objective(ep):
    title = "Reconnaître et appliquer la relation"
    obj = RUNTIME["objective_art"](title,[
        ("Reconnaître",1,text("Savoir",717,size=64)),
        ("appliquer la relation",2,text("Utiliser la règle",717,size=59)),
    ])
    prefix_width = obj["measure"]
    width = 570 if ep==1 else 425
    obj.update(measure=prefix_width+36+width,
               size=min(64,math.floor(1600*64/(prefix_width+36+width))),
               formula=dict(value=FORMULAS[ep],offset=prefix_width+36,width=width,size=59))
    spoken = ("racine carrée de a multipliée par racine carrée de b est égale à la racine carrée du produit de a et b."
              if ep==1 else
              "racine carrée de a sur racine carrée de b est égale à la racine carrée du quotient a sur b.")
    return scene(ep,"objectif",1,3,"Déclaration de l’objectif",
                 f"Bonjour ! Aujourd’hui, vous serez capables de reconnaître et appliquer la relation : {spoken} | "
                 + ("Reconnaître, c’est savoir. | Et appliquer la relation, c’est utiliser la règle pour effectuer un calcul."
                    if ep==1 else
                    "Reconnaître cette relation, c’est savoir la repérer. | L’appliquer, c’est utiliser la règle dans un calcul."),
                 kind="intro",objective=obj)


def equation(left,right,y,at,reveal,size):
    # Phantom preserves the full equation's geometry before its right side is spoken.
    return (
        mathline(left+r"\phantom{="+right+"}",y,at,size,to=reveal),
        mathline(left+"="+right,y,reveal,size),
    )


def examples(ep):
    if ep==1:
        first = r"\sqrt{2}\times\sqrt{8}"
        right = r"\sqrt{2\times 8}"
        reverse = r"\sqrt{16\times25}"
        expanded = r"\sqrt{16}\times\sqrt{25}"
        a = "Par exemple, | la racine carrée de deux multipliée par la racine carrée de huit | est égale à la racine carrée de deux fois huit."
        b = "Je peux aussi utiliser la propriété dans l’autre sens : | la racine carrée de seize fois vingt-cinq | est égale au produit de la racine carrée de seize et la racine carrée de vingt-cinq."
        sizes=(112,99)
    else:
        first = r"\frac{\sqrt{8}}{\sqrt{2}}"
        right = r"\sqrt{\frac{8}{2}}"
        reverse = r"\sqrt{\frac{25}{16}}"
        expanded = r"\frac{\sqrt{25}}{\sqrt{16}}"
        a = "Par exemple, | racine carrée de huit sur racine carrée de deux | est égale à la racine carrée du quotient huit sur deux."
        b = "Je peux aussi utiliser la propriété dans l’autre sens : | la racine carrée du quotient vingt-cinq sur seize | est égale à racine carrée de vingt-cinq sur racine carrée de seize."
        sizes=(125,125)
    # One equals sign, with the second member entering when the voice states the relation.
    return [
        scene(ep,"exemple-1",7,7,"Exemple 1",a,
              *equation(first,right,612,1,2,sizes[0])),
        scene(ep,"exemple-2",8,8,"Exemple 2",b,
              *equation(reverse,expanded,612,1,2,sizes[1])),
    ]


def property_scene(ep):
    if ep==1:
        speech = (
            "Je commence par la propriété du produit de deux racines carrées. | "
            "A et b sont deux nombres positifs ou nuls. | "
            "Le produit de la racine carrée de a et de la racine carrée de b | "
            "est égal à la racine carrée du produit de a et b.")
        left,right = r"\sqrt{a}\times\sqrt{b}",r"\sqrt{a\times b}"
        content = [
            mathline(r"a\text{ et }b\text{ sont deux nombres positifs ou nuls.}",425,1,53),
            mathline(r"a\geq0\qquad b\geq0",520,1,57),
        ]
    else:
        speech = (
            "Voici la propriété du quotient de deux racines carrées. | "
            "Je prends a positif ou nul | et b strictement positif. | "
            "C’est important : le dénominateur ne peut pas être zéro. | "
            "Alors, racine carrée de a sur racine carrée de b | "
            "est égale à la racine carrée du quotient a sur b.")
        left,right = r"\frac{\sqrt{a}}{\sqrt{b}}",r"\sqrt{\frac{a}{b}}"
        content = [
            mathline(r"a\text{ est positif ou nul.}",402,1,55),
            mathline(r"b\text{ est strictement positif.}",480,2,55),
            mathline(r"a\geq0\qquad b>0",568,2,58),
        ]
    base=2 if ep==1 else 4
    return scene(ep,"propriete",4,6,"Propriété",speech,
                 *content,
                 *equation(left,right,770,base,base+1,100))


def remark(ep):
    noun="produit" if ep==1 else "quotient"
    left,right = ((r"\sqrt{a}\times\sqrt{b}",r"\sqrt{a\times b}") if ep==1 else
                  (r"\frac{\sqrt{a}}{\sqrt{b}}",r"\sqrt{\frac{a}{b}}"))
    introduction = ("Voici une remarque pour mieux comprendre cette propriété." if ep==1 else
                    "Je peux retenir la même propriété sous la forme d’une remarque.")
    read = ("L’égalité : racine carrée de a multipliée par racine carrée de b "
            "est égale à la racine carrée de a fois b, signifie que :"
            if ep==1 else "Cette égalité signifie que :")
    return scene(ep,"remarque",9,11,"Remarque",
                 introduction+" | "+read+" | "
                 f"Le {noun} de deux racines carrées | est égal à la racine carrée du {noun}.",
                 text("L’égalité",372,1,56),
                 mathline(FORMULAS[ep],540,1,95),
                 text("signifie que",709,1,48),
                 text(f"Le {noun} de deux racines carrées",805,2,58,weight=700),
                 text(f"est égal à la racine carrée du {noun}.",898,3,58,weight=700))


def pronunciation(ep):
    if ep==1:
        return scene(ep,"prononciation",12,12,"Vocabulaire",
                     "Écoutez la lecture du mot radical. | Ra. | Di. | Cal. | Radical.",
                     kind="pronunciation",pronunciation=dict(word="Radical",syllables=["ra","di","cal"]))
    # Slide 12 requests a whole-word reading unless a source pronunciation video is supplied.
    return scene(ep,"prononciation",12,12,"Vocabulaire",
                 "Écoutez la lecture du mot quotient. | Quotient.",
                 text("Quotient",560,0,116,color=BLUE,weight=700,pulse=1))


def vocabulary(ep):
    is_product=ep==1
    word="Produit" if is_product else "Quotient"
    speech = (
        "Au cours de cette séance, nous avons enrichi notre vocabulaire avec ces mots. | "
        + ("Produit, | comme trois fois cinq, | qui donne quinze. | " if is_product else
           "Je retiens le mot quotient : | par exemple, douze sur trois | égale quatre. | ")
        + "Puis racine carrée : | par exemple, la racine carrée de neuf | vaut trois. | "
        + "Enfin, le radical : | c’est le symbole de la racine carrée, | comme dans racine carrée de seize.")
    first = "3\\times5" if is_product else r"\frac{12}{3}"
    visuals = [
        art("card",word,398,0,53,582,pulse=1),
        art("card","Racine carrée",398,0,53,1338,pulse=4),
        art("card","Radical",746,0,53,960,pulse=7),
        mathline(first,570,2,75,550),
        mathline("=15" if is_product else "=4",570,3,75,760),
        mathline(r"\sqrt{9}",546,5,78,1260),
        mathline("=3",546,6,78,1462),
        mathline(r"\sqrt{\textcolor{#1D1D1D}{16}}",897,9,97,color=RED),
    ]
    return scene(ep,"vocabulaire",13,16,"Vocabulaire",speech,*visuals)


def prepare():
    scenes=[]
    for ep in (1,2):
        scenes += [objective(ep),property_scene(ep),*examples(ep),remark(ep),pronunciation(ep),vocabulary(ep)]
    for ep in (1,2):
        assert [i for s in scenes if s["episode"]==ep for i in s["sourceSlides"]]==list(range(1,17))
    write(PLAN,dict(scenes=scenes))
    write(VOICE_PLAN,dict(scenes=[
        dict(id=s["id"],audio=s["audio"],narration=s["narration"],languageCode="fr",speed=.94,stability=.45)
        for s in scenes]))
    print(len(scenes),"scènes,",sum(len(s["narration"]) for s in scenes),"caractères")


def words(text):
    return RUNTIME["words"](text)


def cue(s,phrase,beat):
    path=Path("public")/s["audio"]
    alignment=load(path.parent/"alignment"/(s["id"]+".json"))["words"]
    before=sum(len(words(b["text"])) for b in s["beats"][:beat])
    source=[w.casefold() for w in words(s["beats"][beat]["text"])]
    needle=[w.casefold() for w in words(phrase)]
    index=next(i for i in range(len(source)) if source[i:i+len(needle)]==needle)
    return round(alignment[before+index]["start"]*30)


def finish():
    results={ep:dict(version=1,lesson=title,level="3AC",videoType="VDP",fps=30,scenes=[]) for ep,title in TITLES.items()}
    RUNTIME["finish_timeline"](load(PACED),results,prefix="n3-sem4-vdp",counts={1:16,2:16})
    for ep,timeline in results.items():
        for s in timeline["scenes"]:
            if s["id"].endswith("vocabulaire"):
                phrases = ["trois fois cinq" if ep==1 else "douze sur trois", "quinze" if ep==1 else "quatre",
                           "racine carrée de neuf","trois","racine carrée de seize"]
                for art_index,beat,phrase in zip([3,4,5,6,7],[2,3,5,6,9],phrases):
                    s["art"][art_index]["frame"]=cue(s,phrase,beat)
        write(VIDEO/f"n3-sem4-vdp{ep}-lesson.json",timeline)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step",choices=("prepare","timeline"))
    (prepare if parser.parse_args().step=="prepare" else finish)()
