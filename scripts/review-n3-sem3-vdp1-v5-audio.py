"""Independent recognition without expected-transcript prompts; findings need review."""
import json,argparse,hashlib
from pathlib import Path
import subprocess
import numpy as np
from faster_whisper import WhisperModel

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--plan',type=Path,default=Path('src/video/n3-sem3-vdp1-v5-voice-plan.json'))
p.add_argument('--output',type=Path,default=Path('outputs/n3-sem3-v5/vdp1'))
p.add_argument('--available',action='store_true')
args=p.parse_args();OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
plan=json.loads(args.plan.read_text(encoding='utf8'))
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,
                  download_root=Path.home()/'.cache/digital-lab-whisper',local_files_only=True)
rows=[]
prior_path=OUT/'independent-asr.json'
prior={r['id']:r for r in json.loads(prior_path.read_text(encoding='utf8'))} if prior_path.exists() else {}
for s in plan['scenes']:
    audio=Path('public')/s['audio']
    if args.available and not audio.exists():continue
    signature=hashlib.sha256(audio.read_bytes()).hexdigest()
    if prior.get(s['id'],{}).get('audioSha256')==signature:
        rows.append(prior[s['id']]);print('Cached independent recognition:',s['id'],flush=True);continue
    pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-ac','1','-ar','16000','-f','f32le','-']),dtype='<f4')
    segments,info=model.transcribe(pcm,beam_size=5,vad_filter=False)
    parts=[dict(start=x.start,end=x.end,text=x.text) for x in segments]
    text=' '.join(x['text'].strip() for x in parts)
    rows.append(dict(id=s['id'],audioSha256=signature,language=info.language,languageProbability=info.language_probability,text=text,segments=parts))
    print(s['id'],info.language,':',text,flush=True)
    (OUT/'independent-asr.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'independent-asr.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
