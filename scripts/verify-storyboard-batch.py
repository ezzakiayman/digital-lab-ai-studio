"""Decode each finished export and capture its encoded review checkpoints."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

week_three = [f'n3-sem3-vdp{i}' for i in range(1,5)]
week_three_v2 = [stem+'-v2' for stem in week_three]
week_three_v3 = [stem+'-v3' for stem in week_three]
week_three_v4 = [stem+'-v4' for stem in week_three]
lessons={
 'n1-sem2-vdp4-v2':('n1-sem2-vdp4-v2','P1_MATHS_N1_SEM2_VDP4_V2',19),
 'n3-sem3-vdp4-v7':('n3-sem3-v7/vdp4','P1_MATHS_N3_SEM3_VDP4_V7',47),
 'n3-sem3-vdp4-v6':('n3-sem3-v6/vdp4','P1_MATHS_N3_SEM3_VDP4_V6',47),
 'n3-sem3-vdp4-v5':('n3-sem3-v5/vdp4','P1_MATHS_N3_SEM3_VDP4_V5',47),
 'n3-sem3-vdp3-v6':('n3-sem3-v6/vdp3','P1_MATHS_N3_SEM3_VDP3_V6',31),
 'n3-sem3-vdp3-v5':('n3-sem3-v5/vdp3','P1_MATHS_N3_SEM3_VDP3_V5',31),
 'n3-sem3-vdp2-v5':('n3-sem3-v5/vdp2','P1_MATHS_N3_SEM3_VDP2_V5',18),
 'n3-sem3-vdp1-v6':('n3-sem3-v6/vdp1','P1_MATHS_N3_SEM3_VDP1_V6',30),
 'n3-sem3-vdp1-v5':('n3-sem3-v5/vdp1','P1_MATHS_N3_SEM3_VDP1_V5',30),
 'n1-sem3-vdp1-v5':('n1-sem3-vdp1-v5','P1_MATHS_N1_SEM3_VDP1_V5',23),
 'n1-sem3-vdp1-v4':('n1-sem3-vdp1-v4','P1_MATHS_N1_SEM3_VDP1_V4',23),
 'n1-sem3-vdp1-v3':('n1-sem3-vdp1-v3','P1_MATHS_N1_SEM3_VDP1_V3',23),
 'n1-sem3-vdp1-v2':('n1-sem3-vdp1-v2','P1_MATHS_N1_SEM3_VDP1_V2',23),
 'n3-sem4-vdp2-v2':('n3-sem4-v2/vdp2','P1_MATHS_N3_SEM4_VDP2_V2',16),
 'n3-sem4-vdp1':('n3-sem4/vdp1','P1_MATHS_N3_SEM4_VDP1',16),
 'n3-sem4-vdp2':('n3-sem4/vdp2','P1_MATHS_N3_SEM4_VDP2',16),
 'n1-sem3-vdp1':('n1-sem3-vdp1','P1_MATHS_N1_SEM3_VDP1',23),
 'n2-sem1-vdp3':('n2-sem1/vdp3','P1_MATHS_N2_SEM1_VDP3',13),
 'n2-sem1-vdp4':('n2-sem1/vdp4','P1_MATHS_N2_SEM1_VDP4',17),
 **{stem:(f'n3-sem3-v4/vdp{i}',f'P1_MATHS_N3_SEM3_VDP{i}_V4',slides)
    for i,(stem,slides) in enumerate(zip(week_three_v4, [30,18,31,47]),1)},
 **{stem:(f'n3-sem3-v3/vdp{i}',f'P1_MATHS_N3_SEM3_VDP{i}_V3',slides)
    for i,(stem,slides) in enumerate(zip(week_three_v3, [30,18,31,47]),1)},
 **{stem:(f'n3-sem3-v2/vdp{i}',f'P1_MATHS_N3_SEM3_VDP{i}_V2',slides)
    for i,(stem,slides) in enumerate(zip(week_three_v2, [30,18,31,47]),1)},
 **{stem:(f'n3-sem3/vdp{i}',f'P1_MATHS_N3_SEM3_VDP{i}',slides)
    for i,(stem,slides) in enumerate(zip(week_three, [30,18,31,47]),1)},
 'signed-addition':('n1-sem2-vdp2','P1_MATHS_N1_SEM2_VDP2',26),
 'n1-sem2-vdp3':('n1-sem2-vdp3','P1_MATHS_N1_SEM2_VDP3',30),
 'n1-sem2-vdp4':('n1-sem2-vdp4','P1_MATHS_N1_SEM2_VDP4',19),
 'like-terms':('n2-sem2-vdp2','P1_MATHS_N2_SEM2_VDP2',27),
 'factorization-v2':('n3-sem2-vdp2-2026-11-10','P1_MATHS_N3_SEM2_VDP2',13),
 'factorization-review':('n3-sem2-vdp2-2026-11-12','P1_MATHS_N3_SEM2_VDP2',13),
 'fractions-v2':('n3-sem2-vdp3-2026-11-10','P1_MATHS_N3_SEM2_VDP3',28),
 'fractions-review':('n3-sem2-vdp3-2026-11-12','P1_MATHS_N3_SEM2_VDP3',28),
 'polynomial-subtraction':('n2-sem2-vm4','P1_MATHS_N2_SEM2_VM4',47),
}
parser=argparse.ArgumentParser()
parser.add_argument('lesson',nargs='*')
args=parser.parse_args()
groups = {'week-four': ['n3-sem4-vdp1','n3-sem4-vdp2-v2'], 'week-one': ['n2-sem1-vdp3','n2-sem1-vdp4'], 'week-three': week_three, 'week-three-v2': week_three_v2, 'week-three-v3': week_three_v3, 'week-three-v4': week_three_v4}
selected = [stem for key in args.lesson for stem in groups.get(key, [key])]
if any(stem not in lessons for stem in selected):
    parser.error('Choose one of '+', '.join(lessons))
for stem in selected or (name for name in lessons if not name.endswith('-review') and name!='signed-addition' and not name.startswith(('n3-sem3-', 'n1-sem2-', 'n2-sem1-', 'n1-sem3-', 'n3-sem4-'))):
    folder,file,slides=lessons[stem]
    out=Path('outputs')/folder
    video=out/(file+'.mp4')
    subprocess.run([sys.executable,'-X','utf8','scripts/verify-n3.py',str(out),'--filename',video.name,'--slides',str(slides)],check=True)
    checks=json.loads((out/'review-frames.json').read_text(encoding='utf-8'))
    for item in checks:
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(item['frame']/30),'-i',str(video),'-frames:v','1',str(out/('export-'+item['name']+'.png'))],check=True)
    print(stem, 'encoded checkpoints:',len(checks),flush=True)

