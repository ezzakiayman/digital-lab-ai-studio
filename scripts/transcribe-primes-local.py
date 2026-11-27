"""Separate local ASR review, without the expected narration as a decoding prompt.
ASR is a review aid and can itself misrecognize numbers or Arabic vocabulary.
"""
import hashlib,json,os,subprocess,argparse
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel

p=argparse.ArgumentParser();p.add_argument('--plan',default='src/video/primes-plan.json');p.add_argument('--out',default='reference/n3-sem2-vdp1/asr');args=p.parse_args()
root=Path(args.out);root.mkdir(parents=True,exist_ok=True)
cache=Path.home()/'.cache/digital-lab-whisper'
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(cache))
plan=json.loads(Path(args.plan).read_text(encoding='utf-8'))
ordered=sorted(plan['scenes'],key=lambda s:0 if s['kind']=='prime-ranges' else 1)
for scene in ordered:
    audio=Path('public')/scene['audio'];signature=hashlib.sha256(audio.read_bytes()+b'whisper-small-fr').hexdigest();target=root/(scene['id']+'.json')
    if target.exists() and json.loads(target.read_text(encoding='utf-8')).get('signature')==signature:print('Cached ASR:',scene['id'],flush=True);continue
    # FFmpeg avoids the installed PyAV/faster-whisper decoder-version mismatch.
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-ac','1','-ar','16000','-f','f32le','-'])
    waveform=np.frombuffer(pcm,dtype=np.float32).copy()
    segments,info=model.transcribe(waveform,language='fr',beam_size=5,condition_on_previous_text=False,vad_filter=True)
    records=[dict(start=round(s.start,3),end=round(s.end,3),text=s.text.strip(),avgLogProbability=s.avg_logprob) for s in segments]
    text=' '.join(s['text'] for s in records)
    target.write_text(json.dumps(dict(signature=signature,model='faster-whisper small, CPU int8',method='ASR without supplied expected transcript',language=info.language,transcript=text,segments=records),ensure_ascii=False,indent=2),encoding='utf-8')
    print(scene['id']+': '+text,flush=True)
