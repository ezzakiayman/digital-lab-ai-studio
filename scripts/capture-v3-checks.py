from pathlib import Path
import json,subprocess
root=Path('outputs/n3-v3');t=json.loads((root/'timeline.json').read_text(encoding='utf-8'));intro=t['scenes'][0];acronym=t['scenes'][2]
checks=[('export-objective.png',(intro['durationInFrames']-15)/30),('export-acronym.png',(sum(s['durationInFrames'] for s in t['scenes'][:2])+acronym['cues']['word3']+30)/30)]
for name,second in checks:subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(second),'-i',str(root/'Digital-Lab-3AC-PPCM.mp4'),'-frames:v','1',str(root/name)],check=True)
