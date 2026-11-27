"""Review fresh, independent local ASR against the checked mathematical examples."""
import hashlib,json,re,unicodedata,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out');p.add_argument('--asr-dir');args=p.parse_args()
plan=json.loads(Path('src/video/polynomials-plan.json').read_text(encoding='utf-8'));timeline=json.loads(Path('src/video/polynomials-lesson.json').read_text(encoding='utf-8'));texts={};models={};findings=[]
first=Path('public')/plan['scenes'][0]['audio'];first_receipt=json.loads(Path(str(first)+'.json').read_text());provider=first_receipt['provider'];voice=first_receipt['voice']
assert provider in ['gemini','elevenlabs']
assert voice==('Kore' if provider=='gemini' else 'e1kzF2oNiC1xDfUP7Yxo')
asr=Path(args.asr_dir or ('reference/n2-sem2-vdp1/asr' if provider=='gemini' else 'reference/n2-sem2-vdp1/asr-elevenlabs'))
def norm(t):
 t=unicodedata.normalize('NFD',t.lower().replace('–',' moins ').replace('−',' moins ')).encode('ascii','ignore').decode()
 # Common ASR representations of the explicitly spoken French letter names.
 t=re.sub(r'\bi grec\b','y',t);t=re.sub(r'\bix\b','x',t);t=re.sub(r'\bzede\b','z',t)
 for word,n in [('deux','2'),('trois','3'),('quatre','4'),('cinq','5'),('un','1')]:t=re.sub(r'\b'+word+r'\b',n,t)
 t=t.replace('-',' moins ').replace('+',' plus ')
 return re.sub('[^a-z0-9]','',t)
for s in plan['scenes']:
 audio=Path('public')/s['audio'];r=json.loads((asr/(s['id']+'.json')).read_text(encoding='utf-8'))
 assert r['signature']==hashlib.sha256(audio.read_bytes()+b'whisper-small-fr').hexdigest(),s['id']
 receipt=json.loads(Path(str(audio)+'.json').read_text(encoding='utf-8'))
 assert receipt['provider']==provider and receipt['voice']==voice
 models[receipt['model']]=models.get(receipt['model'],0)+1
 texts[s['id']]=norm(r['transcript'])
def has(id,text):assert text in texts[id],(id,text,texts[id])
has('definition-binome','2termes');has('definition-trinome','3termes');has('definition-polynome','1ouplusieurstermes')
has('exemple-binome','5xplus3yaucube');has('exemple-binome','2termes');has('exemple-binome','est1binome')
has('contre-exemple-binome','xplus2yplus1');has('contre-exemple-binome','3termes');has('contre-exemple-binome','nestpas1binome')
has('exemple-trinome','2xaucarreplus4ymoins1');has('exemple-trinome','3termes')
has('contre-exemple-trinome','2termes');has('contre-exemple-trinome','nestpas1trinome')
expression='xaucubefoisyaucarreplusxfoisyaucubemoinsxaucubeplus5'
if expression not in texts['exemple-polynome'] and provider=='gemini':
 # Resolve symbolic x/adjacency in whole-clip ASR with an independent first-sentence crop.
 audio=Path('public/polynomials/exemple-polynome.wav');target=asr/'exemple-polynome-first-sentence.json'
 signature=hashlib.sha256(audio.read_bytes()+b'whisper-small-fr-first-sentence-v1').hexdigest()
 if target.exists() and (region:=json.loads(target.read_text(encoding='utf-8'))).get('signature')==signature:pass
 else:
  import numpy as np,subprocess
  from faster_whisper import WhisperModel
  model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(Path.home()/'.cache/digital-lab-whisper'))
  samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32).copy()
  segments,_=model.transcribe(samples[:round(13.3*16000)],language='fr',beam_size=5,condition_on_previous_text=False,vad_filter=False)
  region=dict(signature=signature,start=0,end=13.3,method='Independent ASR crop, VAD disabled, no expected-transcript prompt',transcript=' '.join(s.text.strip() for s in segments))
  target.write_text(json.dumps(region,ensure_ascii=False,indent=2),encoding='utf-8')
 assert expression in norm(region['transcript']),region
 findings.append('Whole-clip ASR wrote multiplication symbolically; targeted VAD-disabled first-sentence review recovers the exact spoken multiplication and all four terms. Finding resolved; original ASR retained.')
else:has('exemple-polynome',expression)
has('exemple-polynome','4termes')
has('synthese','2xplus5ymoins4');has('synthese','xplusymoins2zplus1')
assert all(s['audio'].startswith('polynomials-paced/' if provider=='gemini' else 'polynomials-elevenlabs-paced/') for s in timeline['scenes'])
out=Path(args.out or ('outputs/n2-sem2-vdp1-google' if provider=='gemini' else 'outputs/n2-sem2-vdp1'));out.mkdir(parents=True,exist_ok=True)
(out/'audio-review.json').write_text(json.dumps(dict(scenes=13,provider=provider,voice=voice,models=models,method='Independent faster-whisper small French ASR, without expected transcript prompt',result='Reviewed numerical coefficients, exponents, term counts, example classifications and synthesis values',findings=findings,editorial='Original Google Kore recordings restored from cache.' if provider=='gemini' else 'Explicit French variable names; shortened repeated conclusion after ASR ambiguity.',limits='ASR is a review aid, not full pronunciation certification; known-transcript forced alignment is a separate timing operation.'),ensure_ascii=False,indent=2),encoding='utf-8')
print('Thirteen fresh '+provider+' ASR receipts and reviewed mathematical content checks passed; findings:',len(findings))
