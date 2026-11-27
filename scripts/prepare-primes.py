"""Reviewed editorial plan for the user's 32-slide prime-numbers storyboard."""
import json
from pathlib import Path

scenes=[]
def s(id,kind,slides,title,beats,**data):
    scenes.append(dict(id=id,type='primes',kind=kind,title=title,sourceSlides=slides,audio='primes/'+id+'.wav',beats=[dict(stage=i,text=t) for i,t in enumerate(beats)],narration=' '.join(beats),**data))

s('objectif','intro',[1,2,3,4],'Déclaration de l’objectif',[
    'Bonjour ! Aujourd’hui, vous serez capables de reconnaître et vérifier si un nombre est premier.',
    'Reconnaître, c’est identifier.',
    'Et vérifier se dit en arabe : تحقق.',
    'Un nombre premier, comme deux, trois, cinq, sept ou onze. C’est le sujet de notre séance.'
])
s('definition','definition',[5,6,7],'Définition',[
    'Je commence par la définition.',
    'Un entier positif, noté pé, est un nombre premier si et seulement s’il possède exactement deux diviseurs positifs distincts : un et pé.',
    'Autrement dit, il est divisible uniquement par un et par lui-même.'
])
s('exemple-41','divisors',[8,9,10],'Exemple',[
    'Par exemple, je prends l’entier positif quarante et un.',
    'Quarante et un a uniquement deux diviseurs positifs : un et quarante et un.',
    'Donc, quarante et un est un nombre premier.'
],value=41)
s('exemple-10','divisors',[11,12,13],'Exemple',[
    'Je prends maintenant l’entier positif dix.',
    'Dix a quatre diviseurs positifs : un, deux, cinq et dix.',
    'Donc, dix n’est pas un nombre premier : il possède quatre diviseurs positifs, au lieu de deux.'
],value=10)
s('remarque-1','one',[14,15],'Remarque',[
    'Je passe maintenant à cette remarque.',
    'Attention à ce cas : le nombre un n’est pas premier, car il admet un seul diviseur positif, qui est un.',
    'Pour être premier, il faut exactement deux diviseurs positifs distincts.'
])
s('question','question',[16,17],'À retenir',[
    'À retenir : les nombres premiers inférieurs à cent.',
    'Quels sont donc les nombres premiers inférieurs à cent ?'
],holdSeconds=1.5)
s('premiers-2-47','prime-ranges',list(range(18,23)),'À retenir',[
    'Je commence d’abord par les nombres premiers inférieurs à dix : deux, trois, cinq, sept.',
    'Entre dix et vingt : onze, treize, dix-sept, dix-neuf.',
    'Entre vingt et trente : vingt-trois, vingt-neuf.',
    'Entre trente et quarante : trente et un, trente-sept.',
    'Entre quarante et cinquante : quarante et un, quarante-trois, quarante-sept.'
],rangeStart=0)
s('premiers-53-97','prime-ranges',list(range(23,28)),'À retenir',[
    'Entre cinquante et soixante : cinquante-trois, cinquante-neuf.',
    'Entre soixante et soixante-dix : soixante et un, soixante-sept.',
    'Entre soixante-dix et quatre-vingts : soixante et onze, soixante-treize, soixante-dix-neuf.',
    'Entre quatre-vingts et quatre-vingt-dix : quatre-vingt-trois, quatre-vingt-neuf.',
    'Entre quatre-vingt-dix et cent : quatre-vingt-dix-sept.'
],rangeStart=5)
s('tous-les-premiers','all-primes',[28],'À retenir',[
    'Voici tous les nombres premiers inférieurs à cent.',
    'Il y en a vingt-cinq. Ce sont les nombres à apprendre par cœur.',
    'Prenez un instant pour les relire.'
],holdSeconds=4)
s('prononciation','pronunciation',[29],'Vocabulaire',[
    'Écoutons la lecture du mot premier.',
    'Premier.',
    'Premier.'
])
s('vocabulaire','vocabulary',[30,31,32],'Synthèse',[
    'Au cours de cette séance, nous avons enrichi notre vocabulaire avec ces mots.',
    'Diviseur : par exemple, onze a deux diviseurs positifs, un et onze.',
    'Divisible : onze est divisible uniquement par un et par onze.',
    'Premier : onze est un nombre premier, car il a exactement deux diviseurs positifs distincts.'
])

assert sorted({i for scene in scenes for i in scene['sourceSlides']})==list(range(1,33))
out=Path('src/video/primes-plan.json')
out.write_text(json.dumps(dict(version=1,lesson='Reconnaître les nombres premiers',level='3AC',videoType='VDP',fps=30,scenes=scenes),ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared',len(scenes),'reviewed scenes covering all 32 storyboard slides.')
