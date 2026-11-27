"""Build verified cue frames from actual paced Google speech/alignment."""
import argparse,hashlib,json,re,math,wave
from pathlib import Path
def tokens(t):return [w for w in (re.sub(r'[^\wً-ْٰ]','',s).lower() for s in t.split()) if w]
parser=argparse.ArgumentParser()
parser.add_argument('--revised',action='store_true')
stem='factorization-v2' if parser.parse_args().revised else 'factorization'
plan=json.loads(Path(f'src/video/{stem}-paced-plan.json').read_text(encoding='utf-8'))
for scene in plan['scenes']:
 audio=Path('public')/scene['audio'];data=json.loads((audio.parent/'alignment'/(scene['id']+'.json')).read_text(encoding='utf-8'))
 assert data['signature']==hashlib.sha256(audio.read_bytes()+scene['narration'].encode()).hexdigest(),scene['id']
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
 if scene['kind']=='intro':
  cue('writing','l’écrire',1);cue('multiplication','multiplication',2)
  for i,t in enumerate(['deux','cinq','six']):cue('prime'+str(i),t,3)
 if scene['kind'] in ['theorem','example']:
  beat=2 if scene['kind']=='theorem' else 1
  cue('equals','est égal',beat)
  cue('factor0','deux à la puissance trois',beat);cue('factor1','fois trois à la puissance deux',beat)
  if scene['kind']=='theorem':cue('factor2','fois cinq à la puissance un',beat)
 if scene['kind']=='vocabulary':
  cue('word0','Décomposition',1);cue('word1','facteurs premiers',2);cue('word2','divisions successives',3);cue('word3','l’arbre de factorisation',4)
Path(f'src/video/{stem}-lesson.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Aligned factorisation:',len(plan['scenes']),'scenes,',sum(s['durationInFrames'] for s in plan['scenes'])/30,'seconds')
