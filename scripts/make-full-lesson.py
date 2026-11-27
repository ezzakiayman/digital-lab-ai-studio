import json
from pathlib import Path
scenes=[]
def section(id,kind,start,end,slides,events):
    scenes.append(dict(id=id,type='lesson-section',section=kind,title=id,durationInFrames=round((end-start)*30),audio=None,narration='Narration française originale, intervalle '+str(start)+'–'+str(end)+' s.',sourceSlides=slides,events=[dict(target=k,**{'from':round(a*30),'to':round(b*30)}) for k,a,b in events]))
section('introduction','intro',0,28,[1,2,3,4],[('compare',6,14),('symbols',11.5,14),('sort',15,21),('numbers',22,28)])
section('lecture-du-mot','phonetics',28,42,[5],[('syllables',6,12),('ending',9,12),('whole',12,14)])
section('propriete-1-titre','property-lead',42,48,[6,7],[('expanded',2.5,6)])
p=json.loads(Path('src/video/lesson.json').read_text(encoding='utf-8'))['scenes'][0];p.update(id='propriete-1',durationInFrames=300,audio=None,cues=[dict(target='condition',**{'from':30,'to':135}),dict(target='conclusion',**{'from':165,'to':285})]);scenes.append(p)
e=json.loads(Path('src/video/comparison.json').read_text(encoding='utf-8'))['scenes'][0];e['audio']=None;scenes.append(e)
section('propriete-2-et-exemple','opposite-signs',95,134,[15,16,17,18,19],[('example',13,39),('prompt',15,36),('negative',21,36),('positive',27,36),('result',36,39)])
section('remarque-droite','number-line',134,170,list(range(20,27)),[('line',6,36),('left',9,15),('right',14,16),('comparison',16,36),('place',26,36),('left',24,36),('answer',32,36)])
section('je-retiens','summary',170,180,[27],[('line',0,10),('left',0,10),('right',0,10)])
t=dict(version=1,lesson='Comparer et ranger des nombres',level='1AC',videoType='VDP',fps=30,audio='reference/full-narration.wav',scenes=scenes)
assert sum(s['durationInFrames'] for s in scenes)==5400
Path('src/video/full-lesson.json').write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf-8')

