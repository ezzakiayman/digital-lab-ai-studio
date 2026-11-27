"""Independent local ASR review, including short pronunciation regions omitted by VAD."""
import hashlib,json,os,re,subprocess,unicodedata
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
root=Path('reference/n3-sem2-vdp3/asr');plan=json.loads(Path('src/video/fractions-plan.json').read_text(encoding='utf-8'))
texts={}
for s in plan['scenes']:
 audio=Path('public')/s['audio'];review=json.loads((root/(s['id']+'.json')).read_text(encoding='utf-8'))
 assert review['signature']==hashlib.sha256(audio.read_bytes()+b'whisper-small-fr').hexdigest()
 texts[s['id']]=review['transcript'].lower()
def has(id,pattern):assert re.search(pattern,texts[id]),(id,pattern,texts[id])
has('fraction-irreductible',r'23 sur 41');has('fraction-irreductible',r'23 et (?:de )?41 est un');has('fraction-irreductible',r'premiers entre eux')
has('fraction-reductible',r'42 sur 36')
for n in [2,3,6]:has('fraction-reductible',fr'par {n}')
has('fraction-reductible',r'42 et de 36 est 6')
has('definition',r'si et seulement si');has('definition',r'entiers positifs');has('definition',r'b non nul')
has('multiples-communs',r'5 sur 9 et 7 sur 15');has('multiples-communs',r'45, 90, 135 et 180')
has('denominateur-commun',r'45 comme plus petit');has('vocabulaire',r'1 sur 2');has('vocabulaire',r'3 sur 4')
audio=Path('public/fractions/prononciation.wav');signature=hashlib.sha256(audio.read_bytes()+b'whisper-small-fr-regions-v1').hexdigest();target=root/'prononciation-regions.json'
if target.exists() and (cached:=json.loads(target.read_text(encoding='utf-8'))).get('signature')==signature:regions=cached['regions']
else:
 model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(Path.home()/'.cache/digital-lab-whisper'))
 waveform=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32).copy()
 regions=[]
 for start,end in [(4.,10.3),(10.3,len(waveform)/16000)]:
  segments,_=model.transcribe(waveform[int(start*16000):int(end*16000)],language='fr',beam_size=5,condition_on_previous_text=False,vad_filter=False)
  regions.append(dict(start=start,end=end,transcript=' '.join(s.text.strip() for s in segments)))
 target.write_text(json.dumps(dict(signature=signature,method='Independent ASR; no expected transcript prompt; VAD disabled for isolated syllables',regions=regions),ensure_ascii=False,indent=2),encoding='utf-8')
normalize=lambda s:re.sub('[^a-z]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
assert normalize(regions[0]['transcript'])=='ireductible',regions
assert normalize(regions[1]['transcript'])=='irreductible',regions
out=Path('outputs/n3-sem2-vdp3');out.mkdir(parents=True,exist_ok=True)
(out/'audio-review.json').write_text(json.dumps(dict(scenes=9,method='Independent faster-whisper small French ASR, CPU int8',mathematicalValues='Reviewed source fractions, reduction factors, PGCD results, exact four common multiples and minimum 45 recovered',pronunciation='Targeted independent regions recover i / ré / duc / tible, then irréductible; full-clip VAD omitted isolated repetitions',limits='ASR review is not complete pronunciation certification. Arabic transliteration not certified. MMS aligns a whole expected word across a syllabified performance in the pronunciation scene.'),ensure_ascii=False,indent=2),encoding='utf-8')
print('Nine fresh ASR recordings reviewed; mathematical values and pronunciation regions passed.')
