import json
from pathlib import Path
scenes=[]
def s(id,kind,slides,beats):
 scenes.append(dict(id=id,type='ppcm',kind=kind,title={'intro':'Déclaration de l’objectif','definition':'Définition','acronym':'Définition','multiples':'Exemple','lcm-result':'Exemple','property1':'Propriété 1','divisible-example':'Exemple','property2':'Propriété 2','product-example':'Exemple','verification':'Vérification','pronunciation':'Vocabulaire','summary':'Synthèse','summary1':'Synthèse','summary2':'Synthèse','vocabulary':'À retenir'}[kind],sourceSlides=slides,audio='n3/'+id+'.wav',beats=[dict(stage=i,text=t) for i,t in enumerate(beats)],narration=' '.join(beats)))
s('objectif','intro',[1,2,3,4,5],["Bonjour ! Aujourd’hui, vous serez capables de déterminer le plus petit multiple commun de deux entiers positifs non nuls.","Déterminer, c’est trouver.","Le plus petit multiple commun se dit en arabe : المضاعف المشترك الأصغر.","Deux entiers positifs non nuls, comme cinquante-huit et douze. Mais pas zéro, ni moins trois."])
s('definition','definition',[6,7,8],["Je commence par la définition. X et y sont deux entiers positifs non nuls.","Le plus petit multiple commun non nul de x et de y est noté : P P C M de x et de y."])
s('sigle','acronym',[9,10,11,12],["Le premier P signifie : plus.","Le deuxième P signifie : petit.","C signifie : commun.","Et M signifie : multiple."])
s('multiples','multiples',[13,14,15],["Je prends les deux entiers positifs six et quatre.","Les premiers multiples communs non nuls de six et de quatre sont douze, vingt-quatre et trente-six.","Parmi ces multiples communs, le plus petit est douze."])
s('resultat-douze','lcm-result',[16],["Donc, le P P C M de six et de quatre est égal à douze."])
s('propriete-un','property1',[17,18,19],["Je passe maintenant à la première propriété du P P C M.","X et y sont deux entiers positifs non nuls.","Si x est un multiple de y, alors le P P C M de x et de y est égal à x."])
s('exemple-soixante-douze','divisible-example',[20,21,22,23],["J’applique cette propriété aux nombres soixante-douze et huit.","Je remarque que soixante-douze est égal à huit fois neuf.","Donc, soixante-douze est un multiple de huit.","D’après la première propriété, le P P C M de soixante-douze et de huit est égal à soixante-douze."])
s('propriete-deux','property2',[24,25,26],["Maintenant, la deuxième propriété du P P C M. X et y sont deux entiers positifs non nuls.","Le P P C M de x et de y, multiplié par le P G C D de x et de y, est égal au produit de x par y."])
s('exemple-produit','product-example',[27,28,29],["J’applique cette propriété aux nombres six et quatre.","Je sais que le P P C M de six et de quatre est égal à douze.","Et le P G C D de six et de quatre est égal à deux."])
s('verification','verification',[30,31,32],["Je multiplie le P P C M par le P G C D : douze fois deux, j’obtiens vingt-quatre.","Et six fois quatre est aussi égal à vingt-quatre.","Les deux produits sont égaux. La propriété est donc vérifiée pour six et quatre."])
s('lecture-multiple','pronunciation',[33],["Écoutons la lecture du mot multiple.","Multiple. Multiple."])
s('synthese-definition','summary',[34,35,36],["Retenez maintenant l’essentiel.","Au cours de cette séance, j’ai appris à déterminer le P P C M de deux entiers positifs non nuls.","Par exemple : le P P C M de six et de quatre est égal à douze."])
s('synthese-un','summary1',[37],["J’ai appris à appliquer la première propriété : si x est un multiple de y, alors le P P C M de x et de y est égal à x."])
s('synthese-deux','summary2',[38],["J’ai aussi appris à appliquer la deuxième propriété : le P P C M de x et de y, multiplié par leur P G C D, est égal à x fois y."])
s('vocabulaire','vocabulary',[39],["Enfin, je retiens le vocabulaire : multiple, commun, et P P C M."])
intro=scenes[0]
if len(intro['beats'])==4:
    positive,negative=intro['beats'][3]['text'].split(' Mais ')
    intro['beats'][3]['text']=positive
    intro['beats'].append(dict(stage=4,text='Mais '+negative))
Path('src/video/n3-plan.json').write_text(json.dumps(dict(version=1,lesson='Déterminer le PPCM',level='3AC',videoType='VDP',fps=30,scenes=scenes),ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared',len(scenes),'narration segments, all 39 slides covered.')
