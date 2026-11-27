"""Reviewed Remotion plan for the 23-slide 1AC week 3 VDP1."""
import argparse
import json
import math
import re
from pathlib import Path
import runpy
import shutil
import subprocess
import wave

VIDEO = Path("src/video")
PUBLIC = Path("public")
RAW = "n1-sem3-vdp1"
VOICE = VIDEO / f"{RAW}-voice-plan.json"
ARABIC_PLAN = VIDEO / f"{RAW}-arabic-plan.json"
PLAN = VIDEO / f"{RAW}-plan.json"
PACED = VIDEO / f"{RAW}-paced-plan.json"
REFERENCE = Path("reference") / RAW
RUNTIME = runpy.run_path("scripts/prepare-n3-sem3.py")
art, text, mathline = (RUNTIME[name] for name in ("art", "text", "mathline"))
TITLE = "Additionner et soustraire dans des expressions numériques"
ARABIC = "سَنَتَعَرَّفُ عَلَيْهَا خِلَالَ هَذِهِ الحِصَّةِ."
INK, GREEN, RED, BLUE, ORANGE = "#1D1D1D", "#087746", "#D60019", "#007DBA", "#E78318"
EXAMPLE = "(+7)  +  (−15)  +  (+5)"
SUMMARY = "(−6) + (+4) + (−3)"
PRONOUNCE = f"{RAW}-prononciation"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def scene(name, first, last, title, script, *visuals, kind="teaching", **extras):
    key = f"{RAW}-{name}"
    beats = [line.strip() for line in script.split("|")]
    return dict(episode=1, id=key, type="vdp-sequence", kind=kind, title=title, speechMode="verbatim",
                audio=f"{RAW}/{key}.wav", narration=" ".join(beats),
                beats=[dict(stage=i, text=line, **{"from": 0}) for i,line in enumerate(beats)],
                sourceSlides=list(range(first,last+1)), art=list(visuals), cues={}, **extras)


def algebra(value, y, at=0, size=92, x=960, **extras):
    return art("algebra", value, y, at, size, x, **extras)


def down(y, at, size=64):
    return art("arrow", "down", y, at, size, color=ORANGE, draw=True)


def right(x, y, at, to=None):
    return art("arrow", "right", y, at, 155, x, color=BLUE, draw=True, **({"to":to} if to else {}))


def operators(formula):
    return [match.start()+1 for match in re.finditer(r" \+ ",formula)]


def signed_terms(formula):
    return [(match.start(), match.end()-1) for match in re.finditer(r"\([+−]\d+\)",formula)]


def main_scenes():
    signs = operators(EXAMPLE)
    terms = signed_terms(EXAMPLE)
    final_sign = operators(SUMMARY)[-1]
    assert [EXAMPLE[a:b+1] for a,b in terms]==["(+7)","(−15)","(+5)"]
    result = [
        scene("objectif",1,4,"Déclaration de l’objectif",
              "Bonjour. Aujourd’hui, vous serez capables d’additionner et soustraire dans des expressions numériques. | "
              "Additionner, c’est calculer une somme. Pour indiquer une addition, j’utilise le signe plus. | "
              "Soustraire, c’est calculer une différence. Pour indiquer une soustraction, j’utilise le signe moins. | "
              f"Expression numérique, c’est une nouvelle notion. {ARABIC}",
              kind="intro", objective=RUNTIME["objective_art"](TITLE,(
                  ("Additionner",1,mathline("+",721,size=98,color="#E60012")),
                  ("soustraire",2,mathline("-",721,size=98,color="#0DBBA1")),
                  ("expressions numériques",3),
              ))),
        scene("definition-expression",5,6,"Définition 1",
              "Voici la première définition, celle de l’expression numérique. | "
              "Une suite d’additions de nombres est une expression numérique.",
              text("Une suite d’additions de nombres",479,1,68,weight=700),
              text("est une expression numérique.",655,1,68)),
        scene("signes-operation",7,10,"Exemple",
              "Je prends l’exemple suivant : plus sept, auquel j’ajoute moins quinze, puis plus cinq. | "
              "J’observe les signes d’opération placés entre les nombres. | Ce sont des signes d’addition. | "
              "Cette suite d’additions est donc une expression numérique.",
              algebra(EXAMPLE,482,0,112,tokenMarks=[dict(index=i,at=1,to=3,color=GREEN) for i in signs]),
              text("L’addition",699,2,58,to=3),
              down(657,3,90),
              text("Expression numérique",826,3,68,weight=700,color=RED)),
        scene("definition-termes",11,12,"Définition 2",
              "Voici la deuxième définition, celle d’un terme. | "
              "Les nombres additionnés dans une expression numérique s’appellent des termes.",
              text("Les nombres additionnés dans une expression numérique",468,1,51,weight=700),
              text("s’appellent des termes.",646,1,70)),
        scene("trois-termes",13,18,"Exemple",
              "Je reprends la même expression : plus sept, auquel j’ajoute moins quinze, puis plus cinq. | "
              "Dans cette expression, je repère les nombres additionnés. | Le premier est plus sept. | "
              "Le deuxième est moins quinze. | Et le troisième est plus cinq. | "
              "Je conclus que cette expression contient trois termes : | plus sept, | moins quinze | et plus cinq.",
              algebra(EXAMPLE,451,0,112,
                      tokenColors=[dict(index=i,at=beat,color=ink) for beat,ink in [(1,GREEN),(5,INK)] for i in signs],
                      tokenMarks=[dict(index=a,endIndex=b,at=i+2,to=5,color=RED) for i,(a,b) in enumerate(terms)]),
              down(586,5,61),text("Trois termes",695,5,65,weight=700),down(773,6,55),
              algebra("(+7)",885,6,70,674), text(",",890,7,66,814),
              algebra("(−15)",885,7,70,952), text("et",885,8,58,1128),
              algebra("(+5)",885,8,70,1285)),
        scene("prononciation",19,19,"Vocabulaire","Écoutez la prononciation du mot expression.",
              text("Expression",421,0,96,color=BLUE,weight=700)),
        scene("vocabulaire",20,23,"Vocabulaire",
              "Je retiens deux mots de vocabulaire. | Expression numérique. | "
              "Par exemple : moins six, auquel j’ajoute plus quatre, puis moins trois. | Terme. | "
              "Dans cette expression, | moins six, | plus quatre | et moins trois sont les trois termes de la somme.",
              art("card","Expression numérique",495,1,41,535,to=3,pulse=1),
              right(875,495,2,to=3),
              algebra(SUMMARY,495,2,71,1280,tokenColors=[
                  dict(index=final_sign,at=2,color=INK),dict(index=final_sign,at=5,color=INK)]),
              art("card","Terme",744,3,48,535,pulse=3),
              right(875,744,5),
              algebra("(−6)",744,5,58,1104), text(",",747,6,50,1185),
              algebra("(+4)",744,6,58,1273), text("et",744,7,38,1374),
              algebra("(−3)",744,7,58,1480),
              text("Trois termes",872,7,49,1290,weight=700)),
    ]
    for item in (result[4],result[6]):
        for beat in item["beats"][4 if item is result[6] else 5:-1]:
            beat["pauseAfter"] = .28
    return result


def speech(scene_id, text, **extra):
    return dict(id=scene_id, audio=f"{RAW}/{scene_id}.wav", narration=text, speechMode="verbatim", **extra)


def prepare():
    scenes = main_scenes()
    intro = scenes[0]
    french = [speech(intro["id"]+"-fr",intro["narration"].removesuffix(ARABIC).strip()), *scenes[1:]]
    arabic = speech(intro["id"]+"-ar",ARABIC,languageCode="ar",speed=.94,stability=.45)
    assert [n for item in scenes for n in item["sourceSlides"]]==list(range(1,24))
    RUNTIME["write"](PLAN,dict(scenes=scenes))
    RUNTIME["write"](VOICE,dict(scenes=french))
    RUNTIME["write"](ARABIC_PLAN,dict(scenes=[arabic]))


def pcm(path):
    with wave.open(str(path)) as src:
        assert (src.getnchannels(),src.getsampwidth(),src.getframerate())==(1,2,24000),path
        return src.readframes(src.getnframes())


def save_wave(path, raw):
    with wave.open(str(path),"wb") as dest:
        dest.setparams((1,2,24000,0,"NONE","not compressed"))
        dest.writeframes(raw)


def receipt(path):
    return Path(str(path)+".json")


def assemble():
    path = PUBLIC/RAW/f"{RAW}-objectif.wav"
    before, arabic = [path.with_name(path.stem+f"-{q}.wav") for q in ("fr","ar")]
    fr_data, ar_data = pcm(before), pcm(arabic)
    gap = bytes(round(.28*24000)*2)
    save_wave(path,fr_data+gap+ar_data)
    tag = load(receipt(before))
    ar_tag = load(receipt(arabic))
    tag.update(arabicModel=ar_tag["model"], arabicVoice=ar_tag["voice"],
               arabicStartSample=(len(fr_data)+len(gap))//2, arabicSamples=len(ar_data)//2,
               parts=[str(before.as_posix()),str(arabic.as_posix())])
    RUNTIME["write"](receipt(path),tag)


def timeline():
    plan = load(PACED)
    results = {1:dict(version=1,lesson=TITLE,level="1AC",videoType="VDP",fps=30,scenes=[])}
    RUNTIME["finish_timeline"](plan,results,prefix="n1-sem3-vdp",counts={1:23})
    timeline = results[1]
    item = next(s for s in timeline["scenes"] if s["id"]==PRONOUNCE)
    lead = PUBLIC/item["audio"]
    src = REFERENCE/"prononciation-expression.mp4"
    clip = PUBLIC/RAW/"prononciation-expression.mp4"
    shutil.copyfile(src,clip)
    clip_audio = subprocess.check_output(["ffmpeg","-v","error","-i",str(src),"-ac","1","-ar","24000","-f","s16le","-"])
    before = pcm(lead)
    # Put the source clip on a frame boundary, with a short pause after the spoken lead-in.
    clip_start = math.ceil((len(before)/48000+.25)*30)
    gap = bytes(clip_start*1600-len(before))
    combined = lead.with_name(lead.stem+"-source.wav")
    save_wave(combined,before+gap+clip_audio)
    clip_frames = math.floor(len(clip_audio)/1600)
    tag = load(receipt(lead))
    tag.update(embeddedSource="Slide 19 pronunciation clip", embeddedStartFrame=clip_start,
               embeddedFrames=clip_frames)
    RUNTIME["write"](receipt(combined),tag)
    item.update(audio=combined.relative_to(PUBLIC).as_posix(),
                durationInFrames=clip_start+math.ceil(len(clip_audio)/1600)+21,
                timingMethod="Source pronunciation clip synchronized to its own audio")
    item["art"].append(art("clip",clip.relative_to(PUBLIC).as_posix(),703,0,434,
                           frame=clip_start,clipFrames=clip_frames))
    RUNTIME["write"](VIDEO/f"{RAW}-lesson.json",timeline)
    print("Final",sum(s["durationInFrames"] for s in timeline["scenes"]),"frames")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","assemble","timeline"))
    {"prepare":prepare,"assemble":assemble,"timeline":timeline}[parser.parse_args().action]()
