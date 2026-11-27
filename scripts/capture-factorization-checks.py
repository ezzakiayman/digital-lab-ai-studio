"""Review actual encoded objective movement and each spoken prime power."""
import json,subprocess
from pathlib import Path
root=Path('outputs/n3-sem2-vdp2');t=json.loads((root/'timeline.json').read_text(encoding='utf-8'));video=root/'P1_MATHS_N3_SEM2_VDP2.mp4'
def cap(f,name):subprocess.run(['ffmpeg','-y','-v','error','-ss',str(f/30),'-i',str(video),'-frames:v','1',str(root/('export-'+name+'.png'))],check=True)
offset=0
for s in t['scenes']:
 cap(offset+s['durationInFrames']-15,s['id'])
 if s['kind']=='intro':
  for label,f in [('center',0),('moving',max(15,s['beats'][1]['from']-36)+16),('top',s['beats'][1]['from']-2)]:cap(f,'objective-'+label)
 if s['kind'] in ['theorem','example']:
  for name,f in s['cues'].items():
   if name.startswith('factor'):cap(offset+f+24,s['id']+'-'+name)
  for i in range(len(s['beats'])-2,len(s['beats'])):cap(offset+s['beats'][i]['from']+35,s['id']+'-name-'+str(i))
 offset+=s['durationInFrames']
print('Five encoded final scenes, objective movement, all powers and naming stages captured.')
