"""Check that paced voice is exactly original speech plus zero-valued inter-idea samples."""
import json,wave,sys
from pathlib import Path
timeline=json.loads(Path(sys.argv[1] if len(sys.argv)>1 else 'src/video/n3-lesson.json').read_text(encoding='utf-8'))
added=0
for scene in timeline['scenes']:
 target=Path('public')/scene['audio'];receipt=json.loads(Path(str(target)+'.json').read_text());source=Path('public')/receipt['sourceAudio']
 with wave.open(str(source)) as w:original=w.readframes(w.getnframes());width=w.getnchannels()*w.getsampwidth();rate=w.getframerate()
 with wave.open(str(target)) as w:paced=w.readframes(w.getnframes());duration=w.getnframes()/w.getframerate()
 data=json.loads((target.parent/'alignment'/(scene['id']+'.json')).read_text(encoding='utf-8'));cuts=data['pauseEdits'];expected=[];last=0
 for cut in cuts:expected.extend([original[last*width:cut['sample']*width],b'\0'*(cut['frames']*width)]);last=cut['sample'];added+=cut['frames']/rate
 expected.append(original[last*width:]);assert b''.join(expected)==paced,scene['id']
 assert all(0<=w['start']<=w['end']<=duration for w in data['words']),scene['id']
 hold=scene.get('holdSeconds',0.9)
 assert hold-0.01<=scene['durationInFrames']/30-duration<=hold+0.04
print(f"All {len(timeline['scenes'])} paced recordings preserve speech samples exactly; {added:.2f}s added inside idea gaps, plus scene holds.")
