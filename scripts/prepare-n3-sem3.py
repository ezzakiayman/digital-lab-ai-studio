"""Reviewed narration and Remotion timeline for the four 3AC week-three VDPs."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import wave

from PIL import ImageFont

ROOT = Path("src/video")
ASSETS = "n3-sem3"
RED, BLUE, GREEN, PURPLE, ORANGE = "#D60019", "#007DBA", "#087746", "#66539F", "#E78318"
FONT = Path("C:/Windows/Fonts/arialbd.ttf")
TITLE_SIZE = 64
scenes = []
episodes = {
    1: "Reconnaître la racine carrée d’un nombre positif",
    2: "Comparer les racines carrées des nombres positifs",
    3: "Distinguer l’écriture décimale illimitée périodique et non périodique",
    4: "Distinguer nombres rationnels, nombres irrationnels et nombres réels",
}
slide_counts = {1: 30, 2: 18, 3: 31, 4: 47}


def art(kind, text, y, at=0, size=52, x=960, **options):
    return dict(kind=kind, value=text, x=x, y=y, size=size, at=at, **options)


def text(value, y, at=0, size=52, x=960, **options):
    return art("text", value, y, at, size, x, **options)


def mathline(value, y, at=0, size=85, x=960, **options):
    return art("math", value, y, at, size, x, **options)


def mark(kind, y, at=0, size=92, x=960, **options):
    return art(kind, "", y, at, size, x, **options)


def down(y, at, color=ORANGE, **options):
    return art("arrow", "down", y, at, 65, 960, color=color, **options)


def seq(episode, id, source, title, narration, *visuals, kind="teaching", **extra):
    if isinstance(source, int):
        source = (source, source)
    words = [line.strip() for line in narration.split("|")]
    assert all(words)
    key = f"vdp{episode}-{id}"
    scenes.append(dict(episode=episode, id=key, type="vdp-sequence", kind=kind, title=title,
                       speechMode="verbatim", cues={}, narration=" ".join(words), audio=f"{ASSETS}/{key}.wav",
                       sourceSlides=list(range(source[0], source[1] + 1)), art=list(visuals),
                       beats=[{"stage": i, "text": line, "from": 0} for i, line in enumerate(words)], **extra))


def objective_art(title, links):
    font = ImageFont.truetype(str(FONT), TITLE_SIZE)
    measure = round(font.getlength(title))
    links_data = []
    for term, at, *visuals in links:
        start = title.index(term)
        width = round(font.getlength(title[:start + len(term)]) - font.getlength(title[:start]))
        links_data.append(dict(offset=round(font.getlength(title[:start])), width=width, at=at, art=list(visuals)))
    return dict(title=title, measure=measure, size=min(68, math.floor(1600 * TITLE_SIZE / measure)), links=links_data)


def objective(episode, last, speech, *links):
    title = episodes[episode]
    seq(episode, "objectif", (1, last), "Déclaration de l’objectif",
        f"Bonjour ! Aujourd’hui, vous serez capables de {title[0].lower() + title[1:]}. | {speech}", kind="intro",
        objective=objective_art(title, links))


def pronounce(episode, n, word, syllables, spoken, prefix=None):
    prefix = prefix or f"Écoutons la lecture du mot « {word} »."
    seq(episode, f"prononciation-{n}", n, "Vocabulaire",
        " | ".join([prefix, *(s + "." for s in spoken), word.capitalize() + "."]), kind="pronunciation",
        pronunciation=dict(word=word, syllables=syllables))


def vocabulary(episode, source, speech, labels, *visuals):
    items = [art("card", label, 437 if len(labels) == 2 or i < 2 else 664, 0, 52,
                 [590, 1330, 960][i], pulse=min(i+1, len(speech.split("|"))-1))
             for i, label in enumerate(labels)]
    seq(episode, "vocabulaire", source, "Vocabulaire", speech, *items, *visuals)


def positives():
    return (mathline(r"\textcolor{#087746}{\checkmark}\quad 12", 680, size=60),
            mathline(r"\textcolor{#087746}{\checkmark}\quad \frac{5}{7}", 810, size=58),
            mathline(r"\textcolor{#D60019}{\times}\quad -0{,}25", 929, size=60))


def root_diagram(at, reverse, y):
    return (mathline(r"\sqrt{a}", y, at, 89, 565), mathline("a", y, at, 89, 1355),
            art("arrow", "right", y - 23, at, 488, 960, color=RED),
            text("Mise au carré", y - 87, at, 39, color=RED),
            art("arrow", "left", y + 49, reverse, 488, 960, color=BLUE),
            text("Racine carrée", y + 108, reverse, 39, color=BLUE))


def root_one():
    objective(1, 4,
              "Reconnaître. Ataâraf. | La racine carrée est le sujet de notre séance. | D’un nombre positif, comme douze, cinq sur sept, et non pas moins zéro virgule vingt-cinq.",
              ("Reconnaître", 1, text("أتعرف", 716, size=84, rtl=True)),
              ("racine carrée", 2, mathline(r"\left(\textcolor{#D60019}{?}\right)^2=7", 735, size=83)),
              ("nombre positif", 3, *positives()))
    seq(1, "question", 5, "Question", "Alors, qu’est-ce qu’une racine carrée d’un nombre positif ?",
        mark("question", 544, size=295), kind="open")
    seq(1, "definition", (6, 10), "Définition",
        "La racine carrée d’un nombre positif a est le nombre positif ou nul dont le carré est égal à a. | Elle se note racine carrée de a et se lit « racine carrée de a ». | Si je mets la racine carrée de a au carré, j’obtiens a. | Dans l’autre sens, si je prends la racine carrée de a, j’obtiens racine carrée de a. | Voici quelques exemples.",
        text("La racine carrée d’un nombre positif a est le nombre", 388),
        text("positif ou nul dont le carré est égal à a.", 465),
        mathline(r"\sqrt{a}\quad\text{se lit racine carrée de }a", 579, 1, 59),
        *root_diagram(2, 3, 775))
    seq(1, "carres-parfaits", (11, 15), "Exemple",
        "Le carré de quatre est égal à seize. | Alors la racine carrée de seize est égale à quatre. | Le carré de trois est égal à neuf. | Alors la racine carrée de neuf est égale à trois. | Pour trouver la racine carrée de a, je cherche le nombre positif ou nul qui, mis au carré, donne a.",
        mathline(r"4^{\textcolor{#D60019}{2}}=\textcolor{#D60019}{16}", 475, 0, 92, 590, to=4),
        art("arrow", "right", 475, 1, 178, 960, color=GREEN, to=4),
        mathline(r"\textcolor{#007DBA}{\sqrt{16}}=\textcolor{#007DBA}{4}", 475, 1, 92, 1330, to=4),
        mathline(r"3^{\textcolor{#D60019}{2}}=\textcolor{#D60019}{9}", 742, 2, 92, 590, to=4),
        art("arrow", "right", 742, 3, 178, 960, color=GREEN, to=4),
        mathline(r"\textcolor{#007DBA}{\sqrt{9}}=\textcolor{#007DBA}{3}", 742, 3, 92, 1330, to=4),
        mathline(r"\sqrt{a}=\textcolor{#D60019}{?}\qquad\Longrightarrow\qquad \bigl(\textcolor{#D60019}{?}\bigr)^2=a", 615, 4, 96))
    seq(1, "propriete-1", (16, 18), "Propriété 1",
        "Je passe à la première propriété. | Pour tout nombre positif ou nul a, la racine carrée de a, le tout au carré, et son opposé au carré sont tous deux égaux à a. | Par exemple, la racine carrée de onze au carré et son opposé au carré valent tous deux onze.",
        mathline(r"\text{Pour }a\geq 0\text{ :}\quad(\sqrt{a})^2=(-\sqrt{a})^2=a", 445, 1, 69),
        down(611, 2), mathline(r"(\sqrt{11})^2=(-\sqrt{11})^2=11", 798, 2, 92), transition=True)
    seq(1, "propriete-2", (19, 24), "Propriété 2",
        "Voici la deuxième propriété. | Pour tout nombre positif ou nul a, la racine carrée de a au carré est égale à la racine carrée du carré de son opposé. Elles valent a. | Pour calculer la racine carrée de vingt-cinq, je remarque que vingt-cinq est un carré parfait. | C’est le carré de cinq. | C’est également le carré de moins cinq. | On obtient donc cinq.",
        mathline(r"\text{Pour }a\geq 0\text{ :}\quad\sqrt{a^2}=\sqrt{(-a)^2}=a", 445, 1, 69),
        down(600, 2),
        mathline(r"\sqrt{\textcolor{#D60019}{25}}", 793, 2, 88, to=3),
        mathline(r"\sqrt{25}=\sqrt{5^2}", 793, 3, 88, to=4),
        mathline(r"\sqrt{25}=\sqrt{5^2}=\sqrt{(-5)^2}", 793, 4, 88, to=5),
        mathline(r"\sqrt{25}=\sqrt{5^2}=\sqrt{(-5)^2}=\textcolor{#007DBA}{5}", 793, 5, 88))
    seq(1, "verification", (25, 27), "Vérification",
        "Attention à cette erreur : dire que la racine carrée du carré de moins cinq vaut moins cinq. | C’est faux. Une racine carrée est toujours positive ou nulle. | La racine carrée du carré de moins cinq est égale à cinq.",
        mark("alert", 444, size=103),
        mathline(r"\sqrt{(-5)^2}=\textcolor{#D60019}{-5}\quad\textcolor{#D60019}{\times}", 679, 0, 102, to=2, pulse=1),
        mathline(r"\sqrt{(-5)^2}=\textcolor{#087746}{5}\quad\textcolor{#087746}{\checkmark}", 679, 2, 102))
    pronounce(1, 28, "racine", ["ra","cine"], ["ra","cine"])
    vocabulary(1, (29, 30),
               "Les expressions de cette séance sont « racine carrée » et « nombre positif ». | Le carré de la racine carrée de a est égal à a. Dans l’autre sens, on prend la racine carrée de a.",
               ["Nombre positif","Racine carrée"], *root_diagram(1, 1, 728))


def root_two():
    objective(2, 5,
              "Comparer. Qaren. | En utilisant les symboles supérieur à et inférieur à. | Les racines carrées, comme la racine carrée de sept et la racine carrée de dix. | Des nombres positifs, comme douze, cinq sur sept, et non pas moins zéro virgule vingt-cinq.",
              ("Comparer", 1, text("قارن", 715, size=84, rtl=True, to=2),
               mathline(r"\textcolor{#D60019}{>}\quad\text{ou}\quad\textcolor{#D60019}{<}", 714, 2, 78, pulse=2)),
              ("racines carrées", 3, mathline(r"\sqrt{7}\ ;\ \sqrt{10}\ ;\ \ldots", 730, size=77)),
              ("nombres positifs", 4, *positives()))
    pronounce(2, 6, "comparer", ["com","pa","rer"], ["con","pa","ré"])
    seq(2, "propriete", (7, 8), "Propriété",
        "Je passe à la propriété. | Pour deux nombres positifs ou nuls a et b, si a est strictement inférieur à b, alors la racine carrée de a est strictement inférieure à la racine carrée de b.",
        text("Pour deux nombres positifs ou nuls a et b", 453, 1, 57),
        mathline(r"\text{Si }a<b,\quad\text{alors}\quad\textcolor{#007DBA}{\sqrt{a}<\sqrt{b}}", 677, 1, 88), transition=True)
    seq(2, "exemple", (9, 10), "Exemple",
        "Cinq est strictement inférieur à onze. | Alors la racine carrée de cinq est strictement inférieure à la racine carrée de onze.",
        mathline("5<11", 439, 0, 107, pulse=0), down(603, 1, RED),
        mathline(r"\textcolor{#D60019}{\sqrt{\textcolor{#1D1D1D}{5}}}<\textcolor{#D60019}{\sqrt{\textcolor{#1D1D1D}{11}}}", 790, 1, 112))
    seq(2, "attention", (11, 14), "Vérification",
        "Attention : cette propriété ne s’applique pas aux nombres strictement négatifs. | Par exemple, moins huit est inférieur à moins un. | On ne peut pas comparer les racines carrées de moins huit et de moins un. | Pourquoi ? Parce qu’en nombres réels, le nombre sous le radical doit être positif ou nul.",
        mark("alert", 449, 0, 112, pulse=0, to=1),
        mark("alert", 454, 1, 92, 573),
        mathline("-8<-1", 454, 1, 104),
        down(607, 2, RED),
        mathline(r"\sqrt{\textcolor{#D60019}{-8}}<\sqrt{\textcolor{#D60019}{-1}}\quad\textcolor{#D60019}{\times}", 783, 2, 105, pulse=3))
    vocabulary(2, (15, 18),
               "Voici les expressions de cette séance. | Comparer, avec les symboles supérieur à et inférieur à. | Dans cette séance, je compare des racines carrées. | Je peux m’aider de la propriété ou passer par le carré.",
               ["Comparer", "Racine carrée", "Carré"])


def decimal():
    objective(3, 5,
              "Distinguer, c’est faire la différence. | Voici une écriture décimale : trente et un virgule cinquante-six. | Dans cet exemple d’écriture illimitée périodique, les chiffres deux et six se répètent indéfiniment. | Dans cet exemple d’écriture illimitée non périodique, aucune suite de chiffres ne se répète indéfiniment à partir d’un certain rang.",
              ("Distinguer", 1, text("Faire la différence", 730, size=44)),
              ("écriture décimale", 2, mathline("31{,}56", 731, size=86)),
              ("illimitée périodique", 3, mathline(r"5{,}\textcolor{#66539F}{26}26\textcolor{#66539F}{26}\ldots", 731, size=70)),
              ("non périodique", 4, mathline(r"1{,}73205080756\ldots", 731, size=50)))
    pronounce(3, 6, "illimité", ["il","li","mi","té"], ["il","li","mi","té"])
    pronounce(3, 7, "périodique", ["pé","rio","dique"], ["pé","rio","dique"], "Écoutons maintenant le mot « périodique ».")
    seq(3, "definition", (8, 9), "Définition",
        "Je passe à la définition d’une fraction décimale. | Une fraction décimale est une fraction dont le dénominateur est une puissance de dix.",
        text("Une fraction décimale", 472, 0, 68, color=BLUE, weight=700),
        text("est une fraction dont le dénominateur", 621, 1, 59),
        text("est une puissance de 10.", 720, 1, 59, color=RED, weight=700), transition=True)
    seq(3, "fraction-225", (10, 15), "Exemple",
        "Deux cent vingt-cinq sur dix au carré est une fraction décimale. | Pourquoi ? Son dénominateur est une puissance de dix. | Transformons cette fraction en écriture décimale. | Je pars du numérateur, deux cent vingt-cinq. | L’exposant deux indique que je déplace la virgule de deux rangs vers la gauche. | J’obtiens deux virgule vingt-cinq.",
        mathline(r"\frac{225}{10^{\textcolor{#D60019}{2}}}", 560, 0, 110, 620),
        text("Une fraction décimale", 556, 0, 56, 1240, to=2),
        mark("ring", 626, 1, 112, 620, to=2, color=RED),
        mathline("225", 560, 3, 100, 1240, to=5),
        art("arrow", "left", 434, 4, 210, 1240, color=RED, to=5),
        mathline(r"\textcolor{#D60019}{2}", 698, 4, 58, 1240, to=5),
        mark("ring", 626, 4, 112, 620, to=5, color=RED),
        mathline(r"=\quad 2{,}\textcolor{#D60019}{25}", 560, 5, 110, 1140))
    seq(3, "fraction-1", (16, 17), "Exemple",
        "De la même façon, un sur dix à la puissance trois est une fraction décimale. | Son écriture décimale est zéro virgule zéro zéro un.",
        mathline(r"\frac{1}{10^{\textcolor{#D60019}{3}}}", 600, 0, 115, 620),
        text("Une fraction décimale", 594, 0, 56, 1240, to=1),
        mathline(r"=\quad 0{,}\textcolor{#D60019}{001}", 600, 1, 112, 1140))
    seq(3, "fraction-moins-5", (18, 19), "Exemple",
        "Moins cinq sur dix à la puissance zéro est aussi une fraction décimale. | Dix à la puissance zéro vaut un. La fraction est donc égale à moins cinq.",
        mathline(r"\frac{-5}{10^{\textcolor{#D60019}{0}}}", 600, 0, 115, 620),
        text("Une fraction décimale", 594, 0, 56, 1240, to=1),
        mathline(r"=\quad\textcolor{#D60019}{-5}", 600, 1, 112, 1120))
    seq(3, "propriete", (20, 21), "Propriété",
        "Je passe à la propriété. | Tout nombre qui possède une écriture décimale finie s’écrit sous la forme d’une fraction décimale.",
        text("Tout nombre qui possède une écriture décimale finie", 504, 1, 57),
        text("s’écrit sous la forme d’une fraction décimale.", 609, 1, 58,
             color=BLUE, weight=700), transition=True)
    seq(3, "decimale-en-fraction", (22, 27), "Exemple",
        "Observons deux virgule neuf, huit, cinq. Son écriture décimale est finie. Pourquoi ? | Il a trois chiffres après la virgule. | Je vais l’écrire sous la forme d’une fraction. | J’obtiens deux mille neuf cent quatre-vingt-cinq sur mille. | Pourquoi mille ? Parce qu’il y a trois chiffres après la virgule. | Mille est dix à la puissance trois. J’obtiens donc deux mille neuf cent quatre-vingt-cinq sur dix à la puissance trois.",
        mathline("2{,}985", 625, 0, 108, to=1),
        mathline(r"2{,}\underbrace{\textcolor{#D60019}{985}}", 625, 1, 98, to=2),
        mathline(r"2{,}\underbrace{\textcolor{#D60019}{985}}", 625, 2, 92, 520,
                 moveFrom=960),
        mathline(r"=\ \frac{2985}{1000}", 625, 3, 91, 953, to=4),
        mathline(r"=\ \frac{2985}{\textcolor{#D60019}{1000}}", 625, 4, 91, 953),
        mathline(r"=\ \frac{2985}{10^{\textcolor{#D60019}{3}}}", 625, 5, 91, 1362))
    vocabulary(3, (28, 31),
               "Reprenons les mots de cette séance. | Décimale, avec par exemple une partie entière et une partie après la virgule. | Illimitée signifie qu’il y a une infinité de chiffres après la virgule. | Périodique signifie qu’un même groupe de chiffres se répète indéfiniment à partir d’un certain rang.",
               ["Décimale", "Illimitée", "Périodique"])


def real_numbers():
    objective(4, 4,
              "Distinguer, c’est faire la différence. | Voici quelques nombres : sept, zéro virgule vingt-cinq, moins trois quarts, la racine carrée de deux et pi. | Voyons ce que signifient ces expressions.",
              ("Distinguer", 1, text("Faire la différence", 728, size=45)),
              ("nombres rationnels, nombres irrationnels et nombres réels", 2,
               mathline(r"7\ ;\ 0{,}25\ ;\ -\frac{3}{4}", 714, size=70),
               mathline(r"\sqrt{2}\ ;\ \pi", 850, size=72)))
    pronounce(4, 5, "irrationnel", ["ir","ra","tion","nel"], ["ir","ra","sion","nèle"])
    pronounce(4, 6, "réel", ["ré","el"], ["ré","elle"], "Écoutons maintenant le mot « réel ».")
    seq(4, "rationnels", (7, 10), "Définition 1",
        "Je commence par la première définition. | Les nombres qui ont une écriture décimale finie ou illimitée et périodique peuvent s’écrire sous forme d’une fraction a sur b. | A et b sont des entiers, et b est différent de zéro. | On les appelle des nombres rationnels.",
        text("Écriture décimale finie ou illimitée et périodique", 403, 1, 54, weight=700),
        mathline(r"\frac{a}{b}", 570, 1, 104, 960),
        mathline(r"a,b\in\mathbb{Z}\qquad b\ne 0", 743, 2, 73),
        text("Nombres rationnels", 887, 3, 59, color=RED, weight=700), transition=True)
    seq(4, "rationnel-decimal", (11, 13), "Exemple",
        "Le nombre deux virgule vingt-cinq a une écriture décimale finie. Il peut donc s’écrire sous forme de fraction. | Deux virgule vingt-cinq est égal à deux cent vingt-cinq sur cent. | C’est un nombre rationnel.",
        mathline("2{,}25", 495, 0, 112, 700),
        text("Une écriture décimale finie", 666, 0, 53, to=1),
        mathline(r"=\quad\frac{225}{100}", 495, 1, 105, 1090),
        text("2,25 est un nombre rationnel.", 783, 2, 61, color=RED, weight=700))
    seq(4, "rationnel-periodique", (14, 18), "Exemple",
        "Observons ce nombre. Les six chiffres sept, un, quatre, deux, huit, cinq se répètent. | C’est une écriture décimale illimitée périodique. | Je peux donc écrire ce nombre sous forme d’une fraction. | Ce nombre est égal à quarante-cinq sur soixante-trois. | C’est un nombre rationnel.",
        mathline(r"0{,}\overbrace{\textcolor{#66539F}{714285}}\overbrace{\textcolor{#66539F}{714285}}7\ldots", 501, 0, 71, 960, to=3),
        text("Écriture décimale illimitée périodique", 701, 1, 53, color=PURPLE, to=4),
        mathline(r"0{,}7142857142857\ldots=\frac{45}{63}", 501, 3, 83),
        text("C’est un nombre rationnel.", 789, 4, 59, color=RED, weight=700))
    seq(4, "irrationnels", (19, 21), "Définition 2",
        "Je passe à la deuxième définition. | Les nombres dont l’écriture décimale est illimitée et non périodique ne s’écrivent pas sous la forme d’une fraction d’entiers. | Ils s’appellent des nombres irrationnels.",
        text("Les nombres dont l’écriture décimale est illimitée", 459, 1, 55),
        text("et non périodique ne s’écrivent pas en fraction d’entiers.", 553, 1, 53),
        text("Nombres irrationnels", 790, 2, 62, weight=700, color=RED), transition=True)
    seq(4, "irrationnel-racine", (22, 25), "Exemple",
        "Je prends la racine carrée de sept. Voici le début de son écriture décimale. Qu’est-ce que je remarque ? | Son écriture décimale est illimitée et non périodique. | Je ne peux donc pas l’écrire sous forme d’une fraction d’entiers. | La racine carrée de sept est un nombre irrationnel.",
        mathline(r"\sqrt{7}=2{,}\underbrace{645751311064\ldots}_{\text{Partie décimale}}", 470, 0, 78, to=1),
        mathline(r"\sqrt{7}=2{,}645751311064\ldots", 470, 1, 87),
        text("Écriture décimale illimitée et non périodique", 642, 1, 54, color=RED),
        down(740, 3, RED),
        mathline(r"\sqrt{7}\quad\text{est un nombre }\textcolor{#D60019}{\text{irrationnel}}", 875, 3, 60))
    seq(4, "irrationnel-pi", (26, 28), "Exemple",
        "De la même façon, voici le début de l’écriture décimale de pi. Sa partie décimale ne s’arrête jamais. | L’écriture décimale de pi est illimitée et non périodique. | Pi est un nombre irrationnel.",
        mathline(r"\pi=3{,}\underbrace{141592653589\ldots}_{\text{Partie décimale}}", 470, 0, 78, to=1),
        mathline(r"\pi=3{,}141592653589\ldots", 470, 1, 86),
        text("Écriture décimale illimitée et non périodique", 642, 1, 54, color=RED),
        down(740, 2, RED),
        mathline(r"\pi\quad\text{est un nombre }\textcolor{#D60019}{\text{irrationnel}}", 875, 2, 60))
    seq(4, "entiers", (29, 34), "Propriété 1",
        "Je passe à la première propriété. | Tout entier est un nombre rationnel. | Deux cent trente-quatre s’écrit sous forme de fraction : deux cent trente-quatre sur un. | Deux cent trente-quatre est donc rationnel. | De même, moins quatre-vingt-sept s’écrit moins quatre-vingt-sept sur un. | Moins quatre-vingt-sept est donc rationnel.",
        text("Tout entier est un nombre rationnel.", 417, 1, 60, color=BLUE, weight=700),
        mathline(r"234=\frac{234}{1}", 680, 2, 91, 570),
        text("234 est rationnel", 847, 3, 49, 570, color=RED),
        mathline(r"-87=\frac{-87}{1}", 680, 4, 91, 1350),
        text("−87 est rationnel", 847, 5, 49, 1350, color=RED), transition=True)
    seq(4, "reels", (35, 37), "Propriété 2",
        "Voici la deuxième propriété. | Les nombres rationnels et les nombres irrationnels forment l’ensemble des nombres réels. | Un nombre réel est soit rationnel, soit irrationnel.",
        text("Les rationnels et les irrationnels forment les nombres réels.", 431, 1, 53),
        mark("sets", 700, 2, pulse=2), transition=True)
    seq(4, "droite-propriete", (38, 40), "Propriété 3",
        "Je passe à la troisième propriété. | À chaque nombre réel correspond un unique point de la droite graduée. Ce nombre est l’abscisse du point. | Réciproquement, à chaque point de la droite graduée correspond une unique abscisse réelle.",
        text("À chaque nombre réel correspond un unique point", 439, 1, 53),
        text("de la droite graduée. Ce nombre est l’abscisse du point.", 536, 1, 53),
        text("Réciproquement, chaque point de la droite graduée", 737, 2, 53),
        text("a une unique abscisse réelle.", 834, 2, 56, color=BLUE, weight=700), transition=True)
    seq(4, "droite-exemple", (41, 43), "Exemple",
        "Je prends une droite graduée. | Je veux y placer la racine carrée de deux. | Ce nombre est l’abscisse d’un point M situé entre A d’abscisse un et B d’abscisse deux.",
        mark("axis", 674),
        mathline(r"\sqrt{2}=1{,}4142135623\ldots", 442, 1, 85),
        mark("axis-root", 674, 2),
        mathline(r"1<\sqrt{2}<2", 887, 2, 71))
    vocabulary(4, (44, 47),
               "Reprenons le vocabulaire. | Un nombre rationnel peut s’écrire sous forme d’une fraction d’entiers. | Un nombre irrationnel a une écriture décimale illimitée et non périodique. | Les nombres réels comprennent deux familles : les rationnels et les irrationnels.",
               ["Rationnel", "Irrationnel", "Réel"])


def words(text):
    return [token for chunk in text.split() if (token := re.sub(r"[^\wً-ْٰ]", "", chunk))]


def finish_timeline(plan, result, suffix="", *, prefix="n3-sem3-vdp", counts=None):
    counts = counts if counts is not None else slide_counts
    for scene in plan["scenes"]:
        if scene["episode"] not in result:
            continue
        audio = Path("public") / scene["audio"]
        alignment = json.loads((audio.parent / "alignment" / (scene["id"] + ".json")).read_text(encoding="utf-8"))
        assert alignment["signature"] == hashlib.sha256(audio.read_bytes() + scene["narration"].encode()).hexdigest()
        cursor = 0
        for beat in scene["beats"]:
            beat["from"] = round(alignment["words"][cursor]["start"] * 30) if cursor else 0
            cursor += len(words(beat["text"]))
        assert cursor == len(alignment["words"]), scene["id"]
        assert all(a["from"] < b["from"] for a,b in zip(scene["beats"],scene["beats"][1:])), scene["id"]
        scene["timingMethod"] = "MMS_FA known-transcript alignment"
        scene["holdSeconds"] = 1.2 if scene["kind"] == "pronunciation" else .9
        with wave.open(str(audio)) as clip:
            scene["durationInFrames"] = math.ceil((clip.getnframes() / clip.getframerate() + scene["holdSeconds"]) * 30)
        episode = scene.pop("episode")
        result[episode]["scenes"].append(scene)
    for episode, timeline in result.items():
        assert [n for scene in timeline["scenes"] for n in scene["sourceSlides"]] == list(range(1, counts[episode] + 1))
        write(ROOT / f"{prefix}{episode}{suffix}-lesson.json", timeline)
        print(f"VDP{episode}: {len(timeline['scenes'])} scènes, {counts[episode]} diapositives, {sum(s['durationInFrames'] for s in timeline['scenes']) / 30:.2f} s")


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", action="store_true")
    parser.add_argument("--episode", type=int, choices=episodes)
    parser.add_argument("--paced-plan", type=Path, default=ROOT / "n3-sem3-paced-plan.json")
    args = parser.parse_args()
    result = {i: dict(version=1, lesson=lesson, level="3AC", videoType="VDP", fps=30, scenes=[])
              for i, lesson in episodes.items() if args.episode is None or args.episode == i}
    if args.timeline:
        finish_timeline(json.loads(args.paced_plan.read_text(encoding="utf-8")), result)
    else:
        for make in (root_one, root_two, decimal, real_numbers):
            make()
        for episode, count in slide_counts.items():
            assert [n for s in scenes if s["episode"] == episode for n in s["sourceSlides"]] == list(range(1, count + 1))
        write(ROOT / "n3-sem3-plan.json", dict(scenes=scenes))


