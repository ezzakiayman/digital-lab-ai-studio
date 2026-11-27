"""Adapted from user's presentation-video kit, using Torchaudio 2.8 MMS_FA.
Aligns the known transcript to the existing audio; it is not speech recognition.
"""
import hashlib,json,re,subprocess,warnings,argparse
from pathlib import Path
import numpy as np
import torch,torchaudio,uroman
warnings.filterwarnings('ignore',category=UserWarning)
p=argparse.ArgumentParser();p.add_argument('plan',nargs='?',default='src/video/n3-plan.json');p.add_argument('--available',action='store_true');args=p.parse_args()
plan=json.loads(Path(args.plan).read_text(encoding='utf-8'))
bundle=torchaudio.pipelines.MMS_FA
device='cuda' if torch.cuda.is_available() else 'cpu'
print('Loading MMS alignment model on',device,flush=True)
model=bundle.get_model(with_star=False).to(device).eval();tokenizer=bundle.get_tokenizer();aligner=bundle.get_aligner();roman=uroman.Uroman();keep=set(bundle.get_dict())
for scene in plan['scenes']:
 audio=Path('public')/scene['audio'];root=audio.parent/'alignment';root.mkdir(parents=True,exist_ok=True);cache=root/(scene['id']+'.json')
 if args.available and not audio.exists():print('Audio pending:',scene['id'],flush=True);continue
 signature=hashlib.sha256(audio.read_bytes()+scene['narration'].encode('utf-8')).hexdigest()
 if cache.exists() and json.loads(cache.read_text(encoding='utf-8')).get('signature')==signature:
  print('Cached alignment:',scene['id'],flush=True);continue
 words=[w for w in (re.sub(r'[^\wً-ْٰ]','',t) for t in scene['narration'].split()) if w]
 pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-f','s16le','-ac','1','-ar','16000','-'])
 waveform=torch.from_numpy(np.frombuffer(pcm,np.int16).copy().astype(np.float32)/32768).unsqueeze(0)
 latin=[''.join(c for c in roman.romanize_string(w).lower() if c in keep and c!='-') for w in words];idx=[i for i,w in enumerate(latin) if w]
 with torch.inference_mode():
  emission,_=model(waveform.to(device));spans=aligner(emission[0].cpu(),tokenizer([latin[i] for i in idx]))
 step=waveform.size(1)/emission.size(1)/16000
 times={i:(s[0].start*step,s[-1].end*step,float(np.mean([t.score for t in s]))) for i,s in zip(idx,spans)}
 out=[]
 for i,w in enumerate(words):
  if i not in times:
   prev=out[-1]['end'] if out else 0.;nxt=next((times[j][0] for j in range(i+1,len(words)) if j in times),prev);times[i]=(prev,max(prev,nxt),0.)
  a,b,score=times[i];out.append(dict(word=w,start=round(a,3),end=round(b,3),score=round(score,3)))
 assert all(a['start']<=a['end'] and (i==0 or a['start']>=out[i-1]['start']) for i,a in enumerate(out))
 cache.write_text(json.dumps(dict(signature=signature,method='MMS_FA known-transcript alignment',words=out),ensure_ascii=False,indent=2),encoding='utf-8')
 print('Aligned',scene['id'],len(out),'words',flush=True)
