"""Reviewed plans for the 3AC fractions revision and the 2AC subtraction model."""
import json
from pathlib import Path

base = Path('src/video')
def write(stem, value):
    (base/f'{stem}-plan.json').write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

fractions = json.loads((base/'fractions-plan.json').read_text(encoding='utf-8'))
for s in fractions['scenes']:
    s['revision']='2026-11-10'
    if s['kind']=='pronunciation':
        phrases=['Écoutons la lecture du mot irréductible.','I.','Ré.','Duc.','Tible.','Irréductible.']
        s.update(audio='fractions-v2/prononciation.wav', beats=[dict(stage=i,text=t) for i,t in enumerate(phrases)],
                 narration=' '.join(phrases), holdSeconds=1.8)
write('fractions-v2',fractions)
scenes=[]
def scene(id,kind,first,last,title,phrases,**fields):
    scenes.append(dict(id=id,type='polynomial-subtraction',kind=kind,title=title,sourceSlides=list(range(first,last+1)),
        audio=f'polynomial-subtraction/{id}.wav',beats=[dict(stage=i,text=t) for i,t in enumerate(phrases)],narration=' '.join(phrases),**fields))
scene('objectif','intro',1,2,'Déclaration de l’objectif',[
    'Bonjour. Aujourd’hui, je vais vous expliquer comment effectuer la soustraction de deux polynômes.',
    'Effectuer la soustraction de deux polynômes, c’est calculer leur différence.',
])
scene('methode-horizontale','task',3,10,'Soustraction horizontale',[
    'Voici notre première tâche : effectuer la soustraction horizontale des deux polynômes huit ix plus sept i grec, et six ix plus quatre i grec.',
    'Les deux polynômes sont huit ix plus sept i grec, et six ix plus quatre i grec.',
    'Le calcul se fait sur la même ligne, avec un signe moins entre les deux polynômes.',
    'Pour cela, je vais suivre quatre étapes.',
    'La première : je transforme la soustraction en addition.',
    'La deuxième : j’enlève les parenthèses.',
    'La troisième : je regroupe les termes semblables.',
    'La quatrième : je calcule.',
],method='horizontal')
scene('opposer-horizontal','opposite',11,15,'1. Transformer en addition',[
    'Première étape : je transforme la soustraction en addition.',
    'Je remplace le signe moins de la soustraction par un signe plus.',
    'Puis j’ajoute l’opposé du second polynôme, six ix plus quatre i grec.',
    'L’opposé de six ix est moins six ix.',
    'L’opposé de quatre i grec est moins quatre i grec.',
],method='horizontal')
scene('calcul-horizontal','horizontal',16,26,'Calcul horizontal',[
    'Deuxième étape : j’enlève les parenthèses.',
    'J’enlève les parenthèses autour de l’opposé.',
    'J’obtiens huit ix plus sept i grec moins six ix moins quatre i grec.',
    'Troisième étape : je regroupe les termes semblables.',
    'Je regroupe d’abord les termes en ix : huit ix et moins six ix.',
    'Puis les termes en i grec : sept i grec et moins quatre i grec.',
    'Quatrième étape : je calcule.',
    'J’additionne les termes semblables.',
    'Huit ix moins six ix est égal à deux ix.',
    'Sept i grec moins quatre i grec est égal à trois i grec.',
    'Le résultat de la soustraction est donc deux ix plus trois i grec.',
])
scene('methode-verticale','task',27,32,'Soustraction verticale',[
    'Deuxième tâche : effectuer la soustraction verticale des mêmes polynômes.',
    'Je place l’opposé du second sous le premier, en alignant les termes semblables.',
    'Pour cela, je vais suivre trois étapes.',
    'La première : je change les signes de tous les termes du polynôme à soustraire.',
    'La deuxième : j’effectue l’addition verticale.',
    'La troisième : j’écris le résultat.',
],method='vertical')
scene('opposer-vertical','opposite',33,34,'1. Changer les signes',[
    'Première étape : je change les signes de tous les termes du polynôme à soustraire, six fois ix plus quatre fois la lettre i grec.',
    'J’obtiens moins six fois ix, moins quatre fois la lettre i grec.',
],method='vertical',speechMode='verbatim')
scenes[-1]['audio']='polynomial-subtraction/opposer-vertical-clair.wav'
scene('calcul-vertical','vertical',35,42,'2. Additionner verticalement',[
    'Deuxième étape : j’effectue l’addition verticale.',
    'J’aligne d’abord les termes semblables dans la même colonne.',
    'Puis j’additionne les termes de la colonne de ix.',
    'Huit ix moins six ix est égal à deux ix.',
    'J’additionne les termes de la colonne de i grec.',
    'Sept i grec moins quatre i grec est égal à trois i grec.',
    'Troisième étape : j’écris le résultat.',
    'La soustraction donne deux ix plus trois i grec.',
])
scene('synthese','synthesis',43,47,'Synthèse',[
    'Voici la synthèse.',
    'Pour effectuer la soustraction de deux polynômes, je peux choisir entre deux méthodes.',
    'Première méthode : la soustraction horizontale.',
    'Deuxième méthode : la soustraction verticale.',
    'Les deux méthodes donnent le même résultat : deux ix plus trois i grec.',
],holdSeconds=2.5)
assert [i for s in scenes for i in s['sourceSlides']]==list(range(1,48))
write('polynomial-subtraction',dict(version=1,lesson='Effectuer la soustraction de deux polynômes',level='2AC',videoType='VM',fps=30,scenes=scenes))

