"""Capture actual encoded objective motion, each completed scene and term highlights."""
import json,subprocess,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',nargs='?',default='outputs/n2-sem2-vdp1-google');args=p.parse_args()
root=Path(args.root);timeline=json.loads((root/'timeline.json').read_text(encoding='utf-8'));video=root/'P1_MATHS_N2_SEM2_VDP1.mp4'
def cap(frame,name):subprocess.run(['ffmpeg','-y','-v','error','-ss',str(frame/30),'-i',str(video),'-frames:v','1',str(root/('export-'+name+'.png'))],check=True)
offset=0
for s in timeline['scenes']:
 cap(offset+s['durationInFrames']-15,s['id'])
 revised=s.get('revision')=='2026-11-10'
 if s['kind']=='intro':
  start=max(15,s['beats'][1]['from']-36)
  for name,f in [('objective-center',0),('objective-moving',start+16),('objective-top',s['beats'][1]['from']-2)]:cap(f,name)
  if revised:
   cap(s['beats'][1]['from']+42,'objective-link')
   cap(s['beats'][4]['from']+40,'objective-roadmap')
 if revised and s['kind']=='example':
  term_count={'binome':2,'trois-termes':3,'trinome':3,'deux-termes':2,'quatre-termes':4}[s['expressionKey']]
  for i in range(term_count):
   cap(offset+min(s['beats'][i+2]['from']+20,s['beats'][i+3]['from']-10),s['id']+'-term-'+str(i+1))
  if s['concept']=='polynome':
   cap(offset+s['beats'][6]['from']+20,s['id']+'-variables')
   cap(offset+s['beats'][7]['from']+30,s['id']+'-exponents')
 elif s['kind']=='example' and s['concept']!='polynome':
  for i in range(2,len(s['beats'])-2):cap(offset+s['beats'][i]['from']+24,s['id']+'-term-'+str(i-1))
 if revised and s['kind']=='pronunciation':
  cap(offset+s['beats'][1]['from']+14,s['id']+'-first')
  cap(offset+s['beats'][-2]['from']+14,s['id']+'-syllables')
 if revised and s['id']=='definition-binome':cap(offset+6,'box-entrance')
 offset+=s['durationInFrames']
print(f'Encoded objective motion, all {len(timeline["scenes"])} scenes and meaningful intermediate states captured.')
