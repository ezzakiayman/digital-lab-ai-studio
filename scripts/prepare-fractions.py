"""Manually reviewed scene plan; storyboard strips remain production data."""
import json
from pathlib import Path
scenes=[]
def s(id,kind,slides,title,beats,**kw):
 scenes.append(dict(id=id,type='fractions',kind=kind,title=title,sourceSlides=slides,audio='fractions/'+id+'.wav',beats=[dict(stage=i,text=t) for i,t in enumerate(beats)],narration=' '.join(beats),**kw))
s('objectif','intro',[1,2,3],'Déclaration de l’objectif',[
 'Bonjour ! Aujourd’hui, vous serez capables de simplifier une fraction et de réduire deux fractions au même dénominateur.',
 'Simplifier une fraction, c’est اختزال une fraction.',
 'Et réduire deux fractions au même dénominateur, c’est توحيد المقام.'
])
s('fraction-irreductible','irreducible',[4,5,6,7],'Exemple',[
 'Est-ce que je peux réduire la fraction vingt-trois sur quarante et un ?',
 'Non. Pourquoi ? Car vingt-trois et quarante et un ont un seul diviseur commun : un.',
 'Alors, le plus grand commun diviseur de vingt-trois et de quarante et un est un.',
 'Donc, vingt-trois et quarante et un sont premiers entre eux.',
 'Je dis que la fraction vingt-trois sur quarante et un est irréductible.'
])
s('fraction-reductible','reducible',list(range(8,15)),'Exemple',[
 'Est-ce que je peux maintenant réduire la fraction quarante-deux sur trente-six ?',
 'Oui. Par combien ?',
 'Par deux : je divise le numérateur et le dénominateur par deux.',
 'Par trois : je divise les deux par trois.',
 'Et par six : je divise les deux par six.',
 'Le plus grand commun diviseur de quarante-deux et de trente-six est six.',
 'Je dis que la fraction quarante-deux sur trente-six est réductible par six.'
])
s('definition','definition',[15,16],'Définition',[
 'Je retiens cette définition.',
 'Une fraction a sur b, avec a et b entiers positifs et b non nul, est irréductible si et seulement si a et b sont premiers entre eux.'
])
s('propriete','property',[17,18],'Propriété',[
 'Je passe à la propriété du dénominateur commun de deux fractions.',
 'Le plus petit dénominateur commun de deux fractions est le plus petit commun multiple de leurs deux dénominateurs.'
])
s('multiples-communs','common',list(range(19,25)),'Exemple',[
 'Je prends, par exemple, les deux fractions : cinq sur neuf et sept sur quinze.',
 'Je veux mettre ces deux fractions au même dénominateur.',
 'Pour cela, je cherche le plus petit commun multiple de neuf et de quinze.',
 'Les premiers multiples communs strictement positifs de neuf et de quinze sont : quarante-cinq, quatre-vingt-dix, cent trente-cinq et cent quatre-vingts.',
 'Parmi ces multiples communs, le plus petit est quarante-cinq.',
 'Donc, le plus petit commun multiple de neuf et de quinze est quarante-cinq.'
])
s('denominateur-commun','denominator',[25],'Dénominateur commun',[
 'Comme le plus petit commun multiple de quinze et de neuf est quarante-cinq,',
 'je choisis quarante-cinq comme plus petit dénominateur commun des deux fractions.'
])
s('prononciation','pronunciation',[26],'Vocabulaire',[
 'Écoutons la lecture du mot irréductible.', 'Irréductible.', 'Irréductible.'
])
s('vocabulaire','vocabulary',[27,28],'Synthèse',[
 'Au cours de cette séance, nous avons enrichi notre vocabulaire avec ces mots.',
 'Dénominateur : dans la fraction un sur deux, le dénominateur est deux.',
 'Et irréductible : le numérateur et le dénominateur sont premiers entre eux, comme dans la fraction trois sur quatre.'
])
assert sorted({i for s in scenes for i in s['sourceSlides']})==list(range(1,29))
Path('src/video/fractions-plan.json').write_text(json.dumps(dict(version=1,lesson='Simplifier une fraction et réduire au même dénominateur',level='3AC',videoType='VDP',fps=30,scenes=scenes),ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared nine reviewed scenes covering 28 slides.')
