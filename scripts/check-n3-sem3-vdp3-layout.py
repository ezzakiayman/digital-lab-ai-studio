"""Measure alignment in encoded MP4 frames, independently of the scene coordinates."""
import json
from pathlib import Path
import numpy as np
from PIL import Image

OUT=Path('outputs/n3-sem3-v5/vdp3')


def bands(indices):
    result=[]
    for i in indices:
        if not result or i>result[-1][-1]+1:result.append([int(i)])
        else:result[-1].append(int(i))
    return result


def black(path):return np.asarray(Image.open(path).convert('RGB')).max(axis=2)<90


a=black(OUT/'export-vdp3-fraction-1.png');rows=[]
for name,top,bottom in [('top',435,515),('bottom',745,825)]:
    fraction=bands(np.where(a[top:bottom,600:850].sum(axis=1)>140)[0]+top)
    equal=bands(np.where(a[top:bottom,850:990].sum(axis=1)>55)[0]+top)
    assert len(fraction)==1 and len(equal)==2,(fraction,equal)
    bar=(fraction[0][0]+fraction[0][-1])/2
    axis=sum((b[0]+b[-1])/2 for b in equal)/2
    assert abs(bar-axis)<=1.5,(bar,axis)
    line=equal[0][len(equal[0])//2];xs=np.where(a[line,850:990])[0]+850
    rows.append(dict(row=name,fractionBarY=bar,equalsAxisY=axis,deltaPixels=abs(bar-axis),equalsX=[int(xs.min()),int(xs.max())]))
assert rows[0]['equalsX']==rows[1]['equalsX']

positions=[]
for name in ['export-revision-vdp3-fraction-225-0-before-fade.png','export-vdp3-fraction-225.png']:
    a=black(OUT/name);ys=np.where(a[530:590,600:850].sum(axis=1)>140)[0]+530
    assert len(ys)>0,name
    positions.append([int(ys.min()),int(ys.max())])
assert positions[0]==positions[1],positions
report=dict(encodedRows=rows,sharedEqualsColumn=True,
            stableFractionBarBeforeAfterResult=positions,measurement='Black-ink runs in final encoded frames; axis tolerance 1.5 px')
(OUT/'encoded-math-layout-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,indent=2))
