"""Remove a detected spoken TTS instruction while keeping every lesson speech sample."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import time
import wave
import numpy as np
from faster_whisper import WhisperModel

p=argparse.ArgumentParser()
p.add_argument('plan')
p.add_argument('archive')
args=p.parse_args()
archive=Path(args.archive)
archive.mkdir(parents=True,exist_ok=True)
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,
    download_root=str(Path.home()/'.cache/digital-lab-whisper'))
for scene in json.loads(Path(args.plan).read_text(encoding='utf-8'))['scenes']:
    wav=Path('public')/scene['audio']
    receipt=Path(str(wav)+'.json')
    data=json.loads(receipt.read_text(encoding='utf-8'))
    if data.get('removedSpokenInstructionSeconds'):
        continue
    audio=subprocess.check_output(['ffmpeg','-v','error','-i',str(wav),'-ac','1','-ar','16000','-f','f32le','-'])
    segments,_=model.transcribe(np.frombuffer(audio,dtype=np.float32).copy(),language='fr',
        beam_size=5,word_timestamps=True,condition_on_previous_text=False,vad_filter=False)
    words=[w for s in segments for w in s.words]
    norm=lambda s:re.sub(r'[^\w]','',s.lower())
    words=[w for w in words if norm(w.word)]
    if [norm(w.word) for w in words[:2]]!=['lis','uniquement']:
        print('No spoken instruction:',scene['id'],flush=True)
        continue
    boundary=next(i for i,w in enumerate(words[:45]) if norm(w.word) in ['instruction','instructions'])
    before,after=words[boundary],words[boundary+1]
    assert norm(after.word)==norm(scene['narration'].split()[0]),(scene['id'],before.word,after.word)
    with wave.open(str(wav)) as w:
        params=w.getparams()
        pcm=w.readframes(w.getnframes())
        assert w.getnchannels()==1 and w.getsampwidth()==2
    samples=np.frombuffer(pcm,dtype=np.int16)
    # The quiet region between the reviewed prefix and the first lesson word is the safe cut.
    lo=max(before.end-.08,after.start-.36,0)
    hi=max(lo,min(after.start-.06,before.end+.25))
    centers=range(round(lo*params.framerate),round(hi*params.framerate)+1,120)
    cut=min(centers,key=lambda i:np.mean(np.abs(samples[max(0,i-96):i+96].astype(np.int32))))
    raw=archive/wav.name
    if raw.exists():
        assert raw.read_bytes()==wav.read_bytes(),'Raw recording conflict'
    else:
        shutil.copyfile(wav,raw)
        shutil.copyfile(receipt,archive/receipt.name)
    tmp=wav.with_suffix('.tmp')
    with wave.open(str(tmp),'wb') as w:
        w.setparams(params)
        w.writeframes(pcm[cut*2:])
    for attempt in range(5):
        try:
            tmp.replace(wav)
            break
        except PermissionError:
            if attempt==4:
                raise
            time.sleep(.5*(attempt+1))
    data.update(removedSpokenInstructionSeconds=cut/params.framerate,
        originalSha256=hashlib.sha256(raw.read_bytes()).hexdigest())
    receipt.write_text(json.dumps(data,indent=2),encoding='utf-8')
    with wave.open(str(wav)) as w:
        assert w.readframes(w.getnframes())==pcm[cut*2:]
    print(scene['id'],round(cut/params.framerate,3),before.word,after.word,flush=True)

