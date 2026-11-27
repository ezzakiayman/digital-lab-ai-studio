"""Final paced audio determines frames; every alignment receipt must match its audio/text."""
import argparse,json,hashlib,math,re,wave
from pathlib import Path
def tokens(text):return [w for w in (re.sub(r'[^\wً-ْٰ]','',t).lower() for t in text.split()) if w]
p=argparse.ArgumentParser()
p.add_argument('--revised',action='store_true')
args=p.parse_args()
stem='polynomials-v2' if args.revised else 'polynomials'
plan=json.loads(Path(f'src/video/{stem}-paced-plan.json').read_text(encoding='utf-8'))
for scene in plan['scenes']:
 audio=Path('public')/scene['audio'];data=json.loads((audio.parent/'alignment'/(scene['id']+'.json')).read_text(encoding='utf-8'))
 assert data['signature']==hashlib.sha256(audio.read_bytes()+scene['narration'].encode()).hexdigest()
 words=data['words'];offsets=[];index=0
 for b in scene['beats']:
  offsets.append(index);b['from']=0 if b['stage']==0 else round(words[index]['start']*30);index+=len(tokens(b['text']))
 assert index==len(words)
 with wave.open(str(audio)) as w:seconds=w.getnframes()/w.getframerate()
 scene['durationInFrames']=math.ceil((seconds+scene.get('holdSeconds',.9))*30);scene['cues']={};scene['timingMethod']='MMS_FA known-transcript alignment'
 def cue(name,phrase,beat,occurrence=0):
  start=offsets[beat];end=offsets[beat+1] if beat+1<len(offsets) else len(words);span=[w['word'].lower() for w in words[start:end]];needle=tokens(phrase)
  hits=[i for i in range(len(span)-len(needle)+1) if span[i:i+len(needle)]==needle]
  if not hits:raise RuntimeError('Missing cue '+scene['id']+'/'+phrase)
  scene['cues'][name]=round(words[start+hits[occurrence]]['start']*30)
 if scene['kind']=='definition':
  cue('keyword',{'binome':'binôme','trinome':'trinôme','polynome':'polynôme'}[scene['concept']],1)
  cue('count',{'binome':'deux termes','trinome':'trois termes','polynome':'plusieurs termes'}[scene['concept']],1)
  if scene['concept']!='polynome':cue('distinct','qui n’ont pas',1)
 if scene['kind']=='vocabulary':
  for i,t in enumerate(['binôme','trinôme','polynôme']):cue('word'+str(i),t,0)
 if args.revised and scene['kind']=='intro':
  for i,t in enumerate(['binôme','trinôme','polynôme']):cue('concept'+str(i),t,3)
 if args.revised and scene['kind']=='example' and scene['expressionKey']!='deux-termes':
  beat=7 if scene['concept']=='polynome' else len(scene['beats'])-2
  cue('different','différents' if scene['concept']=='polynome' else 'différentes',beat)
 if args.revised and scene['kind']=='inclusion':
  for i,t in enumerate(['binôme','trinôme']):
   cue('inclusionName'+str(i),t,i+1)
   cue('inclusionPolynomial'+str(i),'polynôme',i+1)
 if args.revised and scene['kind']=='synthesis':
  for i,t in enumerate(['deux termes','trois termes','un ou plusieurs termes']):
   cue('summaryCount'+str(i),t,i+1)
   cue('summaryExample'+str(i),'par exemple',i+1)
 if args.revised and scene['kind']=='next':cue('nextTitle','prochaine',0)
Path(f'src/video/{stem}-lesson.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Aligned polynomial lesson:',sum(s['durationInFrames'] for s in plan['scenes'])/30,'seconds')
