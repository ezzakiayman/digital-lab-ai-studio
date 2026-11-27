"""Reviewed 34-slide algebra plan. Main-area content is separate from production strips."""
import json,argparse,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--keep-original-objective',action='store_true');p.add_argument('--gemini',action='store_true');p.add_argument('--elevenlabs',action='store_true');args=p.parse_args()
if args.gemini and args.elevenlabs:p.error('Choose only one narration provider')
args.gemini=not args.elevenlabs
scenes=[]
def s(id,kind,slides,title,beats,**extra):
 # Explicit French letter names avoid ambiguous isolated-variable pronunciation.
 if not args.gemini:
  for letter,spoken in [('x','ix'),('y','i grec'),('z','zède')]:beats=[re.sub(r'\b'+letter+r'\b',spoken,t) for t in beats]
 scenes.append(dict(id=id,type='polynomials',kind=kind,title=title,sourceSlides=slides,audio=('polynomials/' if args.gemini else 'polynomials-elevenlabs/')+id+'.wav',beats=[dict(stage=i,text=t) for i,t in enumerate(beats)],narration=' '.join(beats),**extra))
if args.keep_original_objective:
 s('objectif','intro',[1,2,3],'Déclaration de l’objectif',[
 'Bonjour ! Aujourd’hui, vous serez capables de déterminer le degré d’un polynôme.',
 'Déterminer, c’est trouver une réponse.',
 'Le degré d’un polynôme non nul est un entier positif ou nul, comme zéro, un ou deux.'
 ],objectiveVariant='original')
else:
 s('objectif','intro',[1,2,3],'Déclaration de l’objectif',[
 'Bonjour ! Aujourd’hui, vous serez capables de reconnaître un binôme, un trinôme et un polynôme.',
 'Un binôme comporte deux termes.',
 'Un trinôme comporte trois termes.',
 'Un polynôme comporte un ou plusieurs termes. Nous allons apprendre à les reconnaître.'
 ],objectiveVariant='content-matched')
s('definition-binome','definition',[4,5],'Définition 1',[
 'Je commence par la définition d’un binôme.',
 'Un binôme est une expression algébrique réduite composée de deux termes qui n’ont pas les mêmes variables avec les mêmes exposants.'
],concept='binome')
s('exemple-binome','example',[6,7,8,9],'Exemple',[
 'Par exemple, je prends l’expression algébrique : cinq x plus trois y au cube.',
 'De combien de termes est-elle composée ?',
 'J’observe le premier terme : cinq x.',
 'Puis le second terme : plus trois y au cube.',
 'Elle est composée de deux termes.',
 'Donc, cinq x plus trois y au cube est un binôme.' if args.gemini else 'Donc, cette expression est un binôme.'
],expressionKey='binome',concept='binome',valid=True)
s('contre-exemple-binome','example',[10,11,12,13],'Exemple',[
 'Je prends maintenant l’expression algébrique : x plus deux y plus un.',
 'De combien de termes est-elle composée ?',
 'Le premier terme est x.',
 'Le deuxième terme est plus deux y.',
 'Le troisième terme est plus un.',
 'Elle est composée de trois termes.',
 'Donc, x plus deux y plus un n’est pas un binôme.'
],expressionKey='trois-termes',concept='binome',valid=False)
s('definition-trinome','definition',[14,15],'Définition 2',[
 'Je passe maintenant à la définition d’un trinôme.',
 'Un trinôme est une expression algébrique réduite composée de trois termes qui n’ont pas les mêmes variables avec les mêmes exposants.'
],concept='trinome')
s('exemple-trinome','example',[16,17,18,19],'Exemple',[
 'Par exemple, je prends l’expression algébrique : deux x au carré plus quatre y moins un.',
 'De combien de termes est-elle composée ?',
 'Le premier terme est deux x au carré.',
 'Le deuxième terme est plus quatre y.',
 'Le troisième terme est moins un.',
 'Elle est composée de trois termes.',
 'Donc, deux x au carré plus quatre y moins un est un trinôme.'
],expressionKey='trinome',concept='trinome',valid=True)
s('contre-exemple-trinome','example',[20,21,22,23],'Exemple',[
 'Je prends maintenant l’expression algébrique : x moins trois y.',
 'De combien de termes est-elle composée ?',
 'Le premier terme est x.',
 'Le deuxième terme est moins trois y.',
 'Elle est composée de deux termes.',
 'Donc, x moins trois y n’est pas un trinôme.'
],expressionKey='deux-termes',concept='trinome',valid=False)
s('definition-polynome','definition',[24,25],'Définition 3',[
 'Je passe maintenant à la définition d’un polynôme.',
 'Un polynôme est une expression algébrique réduite composée d’un ou plusieurs termes.'
],concept='polynome')
s('exemple-polynome','example',[26,27],'Exemple',[
 'Par exemple : x au cube fois y au carré, plus x fois y au cube, moins x au cube, plus cinq.',
 'Cette expression est composée de quatre termes.',
 'Donc, c’est un polynôme.'
],expressionKey='quatre-termes',concept='polynome',valid=True)
s('lecture-binome','pronunciation',[28],'Vocabulaire',[
 'Écoutons la lecture du mot binôme.', 'Binôme.', 'Binôme.'
],concept='binome')
s('lecture-polynome','pronunciation',[29],'Vocabulaire',[
 'Écoutons la lecture du mot polynôme.', 'Polynôme.', 'Polynôme.'
],concept='polynome')
s('synthese','synthesis',[30,31,32,33],'Synthèse',[
 'Au cours de cette séance, nous avons enrichi notre vocabulaire avec ces mots.',
 'Binôme : deux termes. Par exemple, cinq x plus trois y au cube est un binôme.',
 'Trinôme : trois termes. Par exemple, deux x plus cinq y moins quatre est un trinôme.',
 'Polynôme : un ou plusieurs termes. Par exemple, x plus y moins deux z plus un est un polynôme.'
],holdSeconds=2)
s('vocabulaire','vocabulary',[34],'À retenir',[
 'Retenez le vocabulaire : binôme, trinôme et polynôme.'
],holdSeconds=2)
assert sorted({i for s in scenes for i in s['sourceSlides']})==list(range(1,35))
plan=dict(version=1,lesson='Binôme, trinôme et polynôme',level='2AC',videoType='VDP',fps=30,scenes=scenes)
Path('src/video/polynomials-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared',len(scenes),'reviewed scenes covering all 34 source slides.')
