"""Reviewed plans for the 2AC like-terms lesson and the resupplied 3AC factorisation deck."""
import json
from pathlib import Path

base = Path('src/video')
scenes = []

def write(name, plan):
    (base/f'{name}-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def scene(id, kind, first, last, title, phrases, **fields):
    scenes.append(dict(id=id, type='like-terms', kind=kind, title=title,
        sourceSlides=list(range(first,last+1)), audio=f'like-terms/{id}.wav',
        beats=[dict(stage=i,text=t) for i,t in enumerate(phrases)],
        narration=' '.join(phrases), **fields))

scene('objectif','intro',1,4,'Déclaration de l’objectif',[
    'Bonjour ! Aujourd’hui, vous serez capables de réduire un polynôme en regroupant les termes semblables.',
    'Réduire un polynôme, c’est simplifier son écriture. Par exemple, deux ix plus huit ix est égal à dix ix.',
    'Les termes deux ix et huit ix sont semblables.',
    'Mais les termes deux ix au cube et huit ix ne sont pas semblables.',
])
scene('definition','definition',5,6,'Définition 1',[
    'Définition un : des termes semblables.',
    'Les termes semblables d’un polynôme ont les mêmes variables avec les mêmes exposants.',
])
scene('termes-semblables','comparison',7,13,'Exemple',[
    'Par exemple, je prends les deux termes : cinq ix i grec et quatre ix i grec.',
    'Ils ont les mêmes variables : ix,',
    'et i grec.',
    'J’observe que cinq ix i grec s’écrit cinq fois ix à la puissance un fois i grec à la puissance un. De même, quatre ix i grec s’écrit quatre fois ix à la puissance un fois i grec à la puissance un.',
    'Ils ont le même exposant de ix : un.',
    'Et le même exposant de i grec : un.',
    'Donc, les deux termes cinq ix i grec et quatre ix i grec sont semblables.',
], example='like')
scene('termes-non-semblables','comparison',14,20,'Exemple',[
    'Je prends maintenant les deux termes : ix au cube fois i grec et ix au carré fois i grec.',
    'Ils ont les mêmes variables : ix,',
    'et i grec.',
    'L’exposant de ix dans le premier terme est trois.',
    'L’exposant de ix dans le second terme est deux.',
    'Les exposants de ix sont différents : trois n’est pas égal à deux.',
    'Donc, ix au cube fois i grec et ix au carré fois i grec ne sont pas semblables.',
], example='unlike')
scene('lecture-semblables','pronunciation',21,21,'Vocabulaire',[
    'Écoutons la lecture du mot semblables.',
    'San.',
    'Blable.',
    'Semblables.',
], holdSeconds=1.8)
scene('synthese','synthesis',22,26,'Synthèse',[
    'Voici ce qu’il faut retenir.',
    'Terme. Dans l’expression deux ix plus cinq, les termes sont deux ix et cinq.',
    'Variables. Dans l’expression trois ix plus deux i grec, les variables sont ix et i grec.',
    'Exposant. Dans l’expression cinq ix au carré, l’exposant de ix est deux.',
    'Semblables. Mêmes variables avec les mêmes exposants. Par exemple, les deux termes trois ix et sept ix sont semblables.',
], holdSeconds=2)
scene('vocabulaire','vocabulary',27,27,'À retenir',[
    'Retenez le vocabulaire : terme, variables, exposant et semblables.',
], holdSeconds=2)
assert [n for s in scenes for n in s['sourceSlides']] == list(range(1,28))
write('like-terms',dict(version=1,lesson='Réduire un polynôme en regroupant les termes semblables',level='2AC',videoType='VDP',fps=30,scenes=scenes))

factors=json.loads((base/'factorization-plan.json').read_text(encoding='utf-8'))
for s in factors['scenes']:
    s['revision']='2026-11-10'
    if s['kind']=='pronunciation':
        phrases=['Écoutons la lecture du mot décomposition.','Dé.','Con.','Po.','Zi.','Sion.','Décomposition.']
        s.update(audio='factorization-v2/lecture-decomposition.wav', beats=[dict(stage=i,text=t) for i,t in enumerate(phrases)],
                 narration=' '.join(phrases), holdSeconds=1.8)
write('factorization-v2',factors)

# Reuse the verified cached 3AC clips and generate only one new vocabulary clip there.
write('vdp2-voice',dict(scenes=[*scenes,*factors['scenes']]))
print('Prepared 7 scenes for 2AC and 5 scenes for 3AC.')

