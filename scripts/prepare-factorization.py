"""Reviewed learner content / narration plan for the13-slide prime-factorisation deck."""
import json
from pathlib import Path
scenes=[]
def s(id,kind,slides,title,beats,**extra):
 scenes.append(dict(id=id,type='factorization',kind=kind,title=title,sourceSlides=slides,audio='factorization/'+id+'.wav',beats=[dict(stage=i,text=t) for i,t in enumerate(beats)],narration=' '.join(beats),**extra))
s('objectif','intro',[1,2,3,4],'Déclaration de l’objectif',[
 'Bonjour ! Aujourd’hui, vous serez capables de décomposer un nombre en produit de nombres premiers.',
 'Décomposer un nombre, c’est l’écrire sous forme d’un produit.',
 'C’est-à-dire que je le transforme en multiplication.',
 'De nombres premiers, comme deux et cinq, mais pas six. Six n’est pas un nombre premier.'
])
s('theoreme-360','theorem',[5,6,7,8],'Théorème',[
 'On a le théorème suivant.',
 'Tout entier positif supérieur ou égal à deux peut s’écrire comme un produit de nombres premiers, de façon unique, à l’ordre des facteurs près.',
 'Par exemple, trois cent soixante est égal à deux à la puissance trois, fois trois à la puissance deux, fois cinq à la puissance un.',
 'Cette décomposition s’appelle la décomposition en produit de facteurs premiers.',
 'Ou une factorisation première.'
],value=360)
s('exemple-72','example',[9,10,11],'Exemple',[
 'La même chose pour la décomposition de soixante-douze.',
 'Soixante-douze est égal à deux à la puissance trois, fois trois à la puissance deux.',
 'On dit que c’est une décomposition en produit de facteurs premiers.',
 'Ou une factorisation première.'
],value=72)
s('lecture-decomposition','pronunciation',[12],'Vocabulaire',[
 'Écoutons la lecture du mot décomposition.', 'Décomposition.', 'Décomposition.'
])
s('synthese','vocabulary',[13],'Synthèse',[
 'Au cours de cette séance, nous avons enrichi notre vocabulaire avec ces expressions.',
 'Décomposition signifie écrire un nombre sous forme de produit de facteurs premiers.',
 'Nous retenons aussi l’expression facteurs premiers.',
 'Et deux méthodes de décomposition : les divisions successives,',
 'et l’arbre de factorisation.'
],holdSeconds=2)
assert sorted({n for scene in scenes for n in scene['sourceSlides']})==list(range(1,14))
Path('src/video/factorization-plan.json').write_text(json.dumps(dict(version=1,lesson='Décomposer un nombre en produit de nombres premiers',level='3AC',videoType='VDP',fps=30,scenes=scenes),ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared five reviewed scenes covering all13 source slides.')
