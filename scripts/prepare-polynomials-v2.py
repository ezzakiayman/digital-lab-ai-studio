"""Reviewed revision of the 55-slide 2AC polynomial storyboard."""
import json
from pathlib import Path

base = Path('src/video')
earlier = {s['id']: s for s in json.loads((base/'polynomials-plan.json').read_text(encoding='utf-8'))['scenes']}
scenes = []

def scene(id, kind, slides, title, text=None, **fields):
    data = dict(id=id, type='polynomials', revision='2026-11-10', kind=kind, title=title, sourceSlides=slides)
    if text is None:
        prior = earlier[id]
        data.update(audio=prior['audio'], beats=prior['beats'], narration=prior['narration'])
    else:
        data.update(audio=f'polynomials-v2/{id}.wav', beats=[dict(stage=i,text=t) for i,t in enumerate(text)], narration=' '.join(text))
    scenes.append(dict(data, **fields))

scene('objectif', 'intro', list(range(1,7)), 'Déclaration de l’objectif', [
    'Bonjour. Aujourd’hui, vous serez capables de déterminer le degré d’un polynôme.',
    'Déterminer le degré, c’est trouver sa valeur par un calcul.',
    'Pour y arriver, je vais procéder en deux parties.',
    'La première partie : reconnaître un binôme, un trinôme et un polynôme.',
    'La deuxième partie : déterminer le degré.',
    'Dans cette vidéo, je traite la première partie : reconnaître un binôme, un trinôme et un polynôme.',
])
scene('definition-binome', 'definition', [7,8], 'Définition 1', concept='binome')
scene('exemple-binome', 'example', list(range(9,15)), 'Exemple', [
    'Par exemple, je prends l’expression algébrique : cinq ix plus trois i grec au cube.',
    'De combien de termes est-elle composée ?',
    'Le premier terme est cinq ix.',
    'Le deuxième terme est plus trois i grec au cube.',
    'Elle est composée de deux termes : cinq ix et trois i grec au cube.',
    'Les variables ix et i grec sont différentes.',
    'Donc, cette expression est un binôme.',
], concept='binome', expressionKey='binome', valid=True)
scene('contre-exemple-binome', 'example', list(range(15,21)), 'Exemple', [
    'Je prends maintenant l’expression algébrique : ix plus deux i grec plus un.',
    'De combien de termes est-elle composée ?',
    'Le premier terme est ix.',
    'Le deuxième terme est plus deux i grec.',
    'Le troisième terme est plus un.',
    'Elle est composée de trois termes : ix, deux i grec et un.',
    'Les variables ix et i grec sont différentes.',
    'Donc, cette expression n’est pas un binôme, car elle a trois termes.',
], concept='binome', expressionKey='trois-termes', valid=False)
scene('definition-trinome', 'definition', [21,22], 'Définition 2', concept='trinome')
scene('exemple-trinome', 'example', list(range(23,29)), 'Exemple', [
    'Par exemple, je prends l’expression algébrique : deux ix au carré plus quatre i grec moins un.',
    'De combien de termes est-elle composée ?',
    'Le premier terme est deux ix au carré.',
    'Le deuxième terme est plus quatre i grec.',
    'Le troisième terme est moins un.',
    'Elle est composée de trois termes : deux ix au carré, quatre i grec et moins un.',
    'Les variables ix et i grec sont différentes.',
    'Donc, cette expression est un trinôme.',
], concept='trinome', expressionKey='trinome', valid=True)
scene('contre-exemple-trinome', 'example', [29,30,31,32], 'Exemple', concept='trinome', expressionKey='deux-termes', valid=False)
scene('definition-polynome', 'definition', [33,34], 'Définition 3', concept='polynome')
scene('exemple-polynome', 'example', list(range(35,44)), 'Exemple', [
    'Par exemple, l’expression ix au cube fois i grec au carré, plus ix fois i grec au cube, moins ix au cube, plus cinq.',
    'Elle est composée de quatre termes.',
    'Ix au cube fois i grec au carré.',
    'Plus ix fois i grec au cube.',
    'Moins ix au cube.',
    'Et plus cinq.',
    'Observons les variables ix et i grec.',
    'Elles ont des exposants différents dans les deux premiers termes.',
    'Donc, cette expression est un polynôme.',
], concept='polynome', expressionKey='quatre-termes', valid=True)
scene('polynomes-particuliers', 'inclusion', [44,45,46], 'Propriété', [
    'Le binôme et le trinôme sont des polynômes particuliers.',
    'Cinq ix plus trois i grec au cube est un binôme, mais c’est aussi un polynôme.',
    'Deux ix au carré plus quatre i grec moins un est un trinôme, mais c’est aussi un polynôme.',
])
for n, concept, syllables in [(47,'binome',['Bi','Nôme']), (48,'trinome',['Tri','Nôme']), (49,'polynome',['Po','Ly','Nôme'])]:
    word = {'binome':'binôme','trinome':'trinôme','polynome':'polynôme'}[concept]
    scene(f'lecture-{concept}', 'pronunciation', [n], 'Vocabulaire', [
        f'Écoutons la lecture du mot {word}.', *[p+'.' for p in syllables], word.capitalize()+'.'
    ], concept=concept, holdSeconds=1.8)
scene('synthese', 'synthesis', [50,51,52,53], 'Synthèse', holdSeconds=2)
scene('vocabulaire', 'vocabulary', [54], 'À retenir', holdSeconds=2)
scene('prochaine-video', 'next', [55], 'Dans la prochaine vidéo', [
    'Dans la prochaine vidéo, je traiterai la deuxième partie : déterminer le degré d’un polynôme.'
], holdSeconds=1.8)

assert [n for s in scenes for n in s['sourceSlides']] == list(range(1,56))
plan = dict(version=1, lesson='Reconnaître un binôme, un trinôme et un polynôme', level='2AC', videoType='VDP', fps=30, scenes=scenes)
(base/'polynomials-v2-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('16 reviewed scenes cover all 55 slides.')

