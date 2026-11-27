"""Review real encoded frames, not only pre-encoding Remotion previews."""
import json,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else 'outputs/n3-sem2-vdp1');timeline=json.loads((root/'timeline.json').read_text(encoding='utf-8'))
revised=timeline['scenes'][0].get('revision') in ('2026-11-10','2026-11-12')
video=root/('P1_MATHS_N3_SEM2_VDP1.mp4' if revised else 'Digital-Lab-3AC-Nombres-premiers.mp4')
start=0
for scene in timeline['scenes']:
    checks=[(('export-' if revised else '')+scene['id']+'.png',start+scene['durationInFrames']-15)]
    if scene['kind']=='intro':checks.append(('export-objective-start.png',0))
    if revised and scene['kind']=='intro':
        checks.append(('export-objective-moving.png',max(15,scene['beats'][1]['from']-36)+16))
        for i,cue in enumerate(['explanation0','explanation1','prime4']):
            checks.append((f'export-objective-link-{i}.png',scene['cues'][cue]+20))
    if revised and scene['kind']=='pronunciation':
        checks.extend((f'export-syllable-{i}.png',start+scene['beats'][i]['from']+14) for i in [1,2])
    if revised and scene['kind']=='definition':checks.append(('export-box-entrance.png',start+6))
    if scene['kind']=='divisors':checks.extend((scene['id']+f'-step-{i}.png',start+b['from']+20) for i,b in enumerate(scene['beats']))
    if scene['kind']=='prime-ranges':
        if revised:
            checks.extend((scene['id']+f'-row-{row}.png',start+max(v for k,v in scene['cues'].items() if k.startswith(f'row{row}number'))+24) for row in range(5))
        else:checks.extend((scene['id']+f'-row-{i}.png',start+b['from']+30) for i,b in enumerate(scene['beats']))
    for name,frame in checks:subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(frame/30),'-i',str(video),'-frames:v','1',str(root/name)],check=True)
    start+=scene['durationInFrames']
if timeline['scenes'][0].get('revision')=='2026-11-12':
    frames=json.loads((root/'review-frames.json').read_text(encoding='utf-8'))
    for item in frames:
        if item['scene'].startswith('review-'):
            subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(item['frame']/30),'-i',str(video),'-frames:v','1',str(root/('export-'+item['scene']+'.png'))],check=True)
print('Extracted encoded final frames and progressive example/list checkpoints for all eleven scenes.')
