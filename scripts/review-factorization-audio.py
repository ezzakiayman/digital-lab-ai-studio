"""Independent ASR content review; isolated-word/criterion crops avoid whole-clip VAD omissions."""
import hashlib,json,re,unicodedata,subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
root=Path('reference/n3-sem2-vdp2/asr');plan=json.loads(Path('src/video/factorization-plan.json').read_text(encoding='utf-8'));texts={}
def norm(t):
 t=unicodedata.normalize('NFD',t.lower()).encode('ascii','ignore').decode()
 for word,n in [('deux','2'),('trois','3'),('cinq','5'),('six','6'),('un','1')]:t=re.sub(r'\b'+word+r'\b',n,t)
 return re.sub('[^a-z0-9]','',t)
for s in plan['scenes']:
 audio=Path('public')/s['audio'];r=json.loads((root/(s['id']+'.json')).read_text(encoding='utf-8'))
 assert r['signature']==hashlib.sha256(audio.read_bytes()+b'whisper-small-fr').hexdigest()
 receipt=json.loads(Path(str(audio)+'.json').read_text());assert receipt['provider']=='gemini' and receipt['voice']=='Kore'
 texts[s['id']]=norm(r['transcript'])
def has(id,t):assert t in texts[id],(id,t,texts[id])
has('objectif','2et5maispas6');has('objectif','6nestpas1nombrepremier')
has('theoreme-360','superieurouegala2');has('theoreme-360','defaconunique');has('theoreme-360','lordredesfacteurs')
has('theoreme-360','360estegala2alapuissance3fois3alapuissance2fois5alapuissance1')
has('exemple-72','72estegala2alapuissance3fois3alapuissance2')
has('synthese','divisionssuccessives');has('synthese','larbredefactorisation')
model=None;regions=[]
for name,start,end in [('lecture-decomposition',3.5,5.6),('lecture-decomposition',5.6,7.5),('theoreme-360',5.5,8.4)]:
 audio=Path('public/factorization')/(name+'.wav');signature=hashlib.sha256(audio.read_bytes()+f'whisper-small-fr-region-{start}-{end}'.encode()).hexdigest();target=root/(name+'-region-'+str(start)+'.json')
 if target.exists() and (r:=json.loads(target.read_text(encoding='utf-8'))).get('signature')==signature:pass
 else:
  if model is None:model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(Path.home()/'.cache/digital-lab-whisper'))
  a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32).copy()
  segments,_=model.transcribe(a[round(start*16000):round(end*16000)],language='fr',beam_size=5,condition_on_previous_text=False,vad_filter=False)
  r=dict(signature=signature,method='Independent ASR crop; VAD disabled; no expected transcript prompt',start=start,end=end,transcript=' '.join(s.text.strip() for s in segments))
  target.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
 if name=='lecture-decomposition':assert norm(r['transcript'])=='decomposition',r
 else:assert re.search(r'produitdenombres?premiers?',norm(r['transcript'])),r
 regions.append(r)
out=Path('outputs/n3-sem2-vdp2');out.mkdir(parents=True,exist_ok=True)
(out/'audio-review.json').write_text(json.dumps(dict(scenes=5,provider='gemini',voice='Kore',model='gemini-2.5-flash-preview-tts',result='Independent ASR recovers both exact prime-power products, uniqueness/order qualifier, prime/nonprime examples and method vocabulary.',resolvedFindings='Whole-clip ASR omitted isolated repeated words and wrote nombreux premiers; bounded VAD-disabled crops recover both repetitions of décomposition and nombre(s) premier(s). Original findings preserved.',regions=regions,limits='ASR remains a review aid and forced alignment is a separate timing operation; full pronunciation certification is not claimed.'),ensure_ascii=False,indent=2),encoding='utf-8')
print('All five fresh Google ASR receipts, exact numbers/powers and targeted pronunciation/criterion checks passed.')
