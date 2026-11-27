import json
from pathlib import Path
end=1110
def e(target,start,stop=37):return dict(target=target,from_=int(start*30),to=int(stop*30))
events=[e('prompt',2.5),e('signs',4.5,6),e('arrowA',10.5,13.2),e('absoluteA',11.7),e('arrowB',13.2,16),e('absoluteB',13.8),e('redB',17,19),e('redA',19,20.5),e('greater',20),e('focusA',21.7,26),e('given',25.8),e('therefore',31),e('resultA',32),e('less',33.5),e('resultB',34.5)]
for event in events:event['from']=event.pop('from_')
t={'version':1,'lesson':'Comparer −3 et −2','level':'1AC','videoType':'VDP','fps':30,'scenes':[{'id':'negative-example-1','type':'negative-comparison','title':'Propriété 1','durationInFrames':end,'narration':'Comparer moins trois et moins deux. Leurs valeurs absolues sont trois et deux. Trois est supérieur à deux. Donc moins trois est inférieur à moins deux.','audio':'reference/negative-comparison.wav','sourceSlides':list(range(9,15)),'operands':[-3,-2],'events':events}]}
Path('src/video/comparison.json').write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf-8')
