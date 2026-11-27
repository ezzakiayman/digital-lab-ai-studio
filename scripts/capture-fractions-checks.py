"""Inspect actual encoded video frames, not only Remotion previews."""
import json,subprocess
from pathlib import Path
root=Path('outputs/n3-sem2-vdp3');timeline=json.loads((root/'timeline.json').read_text(encoding='utf-8'));video=root/'Digital-Lab-3AC-Fractions.mp4'
def capture(frame,name):
 subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(frame/30),'-i',str(video),'-frames:v','1',str(root/('export-'+name+'.png'))],check=True)
offset=0
for s in timeline['scenes']:
 capture(offset+s['durationInFrames']-15,s['id'])
 if s['kind']=='reducible':
  for stage in [2,3,4]:capture(offset+s['beats'][stage]['from']+24,'division-'+str(stage))
 if s['kind']=='common':capture(offset+s['cues']['minimum']+32,'minimum-45')
 offset+=s['durationInFrames']
capture(0,'opening')
print('Captured all nine encoded scenes, three reduction factors, minimum 45 and opening.')
