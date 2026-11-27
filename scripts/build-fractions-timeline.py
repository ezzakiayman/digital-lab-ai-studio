"""Derive scene/word cues from final paced recordings; reject stale alignment."""
import argparse,hashlib,json,math,re,wave
from pathlib import Path
def tokens(s):return [w for w in (re.sub(r'[^\wً-ْٰ]','',t).lower() for t in s.split()) if w]
parser=argparse.ArgumentParser()
parser.add_argument('--revised',action='store_true')
stem='fractions-v2' if parser.parse_args().revised else 'fractions'
plan=json.loads(Path(f'src/video/{stem}-paced-plan.json').read_text(encoding='utf-8'))
for scene in plan['scenes']:
 audio=Path('public')/scene['audio'];data=json.loads((audio.parent/'alignment'/(scene['id']+'.json')).read_text(encoding='utf-8'))
 assert data['signature']==hashlib.sha256(audio.read_bytes()+scene['narration'].encode()).hexdigest()
 words=data['words'];offsets=[];index=0
 for beat in scene['beats']:
  offsets.append(index);beat['from']=0 if not index else round(words[index]['start']*30);index+=len(tokens(beat['text']))
 assert index==len(words)
 with wave.open(str(audio)) as w:seconds=w.getnframes()/w.getframerate()
 scene['durationInFrames']=math.ceil((seconds+scene.get('holdSeconds',.9))*30)
 scene['timingMethod']='MMS_FA known-transcript alignment';scene['cues']={}
 def cue(name,phrase,beat,occurrence=0):
  start=offsets[beat];end=offsets[beat+1] if beat+1<len(offsets) else len(words)
  span=[w['word'].lower() for w in words[start:end]];needle=tokens(phrase)
  hits=[i for i in range(len(span)-len(needle)+1) if span[i:i+len(needle)]==needle]
  if not hits:raise RuntimeError(f'Missing cue: {scene["id"]}/{phrase}')
  scene['cues'][name]=round(words[start+hits[occurrence]]['start']*30)
 if scene['kind']=='intro':cue('arabic0','اختزال',1);cue('arabic1','توحيد المقام',2)
 if scene['kind']=='definition':cue('condition','si et seulement',1);cue('coprime','sont premiers',1)
 if scene['kind']=='property':cue('fractions','de deux fractions',1);cue('denominators','de leurs deux',1)
 if scene['kind']=='common':
  cue('firstFraction','cinq sur neuf',0);cue('secondFraction','sept sur quinze',0)
  for i,t in enumerate(['quarante-cinq','quatre-vingt-dix','cent trente-cinq','cent quatre-vingts']):cue('multiple'+str(i),t,3)
  cue('minimum','quarante-cinq',4)
 if scene['kind']=='vocabulary':cue('denominator','deux',1,1)
Path(f'src/video/{stem}-lesson.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Fractions timeline:',sum(s['durationInFrames'] for s in plan['scenes'])/30,'seconds')
