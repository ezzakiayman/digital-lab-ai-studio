"""Check scene continuity and mathematical placement in the encoded VDP4 export."""
import json
import argparse
from pathlib import Path
import numpy as np
from PIL import Image

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--folder',type=Path,default=Path('outputs/n3-sem3-v5/vdp4'))
OUT=parser.parse_args().folder


def pixels(name):
    return np.asarray(Image.open(OUT/('export-'+name+'.png')).convert('RGB'))


def bounds(mask):
    ys,xs=np.where(mask)
    assert len(xs)>100
    return [int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]


pi=[]
for name in ['revision-vdp4-irrationnel-pi-1','revision-vdp4-irrationnel-pi-2']:
    a=pixels(name)[340:470,400:1510]
    pi.append(bounds(a.max(axis=2)<90))
assert max(abs(a-b) for a,b in zip(*pi))<=1,pi
before_last=pixels('vdp4-entiers-step-4')[720:900,300:1620]
old_ink=int((before_last.max(axis=2)<100).sum())
assert old_ink==0,'Previous integer caption remains during negative example'
property_image=pixels('vdp4-entiers-step-1')[450:650,300:1620]
assert (property_image.max(axis=2)<100).sum()>300
blue=int(((property_image[:,:,2]>property_image[:,:,0]+40)
          &(property_image[:,:,0]<120)&(property_image[:,:,2]>140)).sum())
assert blue==0,'Blue text remains in the property'
axis=pixels('vdp4-droite-exemple')[655:674,1000:1200].astype(int)
red=(axis[:,:,0]>150)&(axis[:,:,1]<80)&(axis[:,:,2]<100)
ys,xs=np.where(red)
assert len(xs)>30
point_x=float(np.mean(xs))+1000
assert 1026<point_x<1177 and abs(point_x-(875+151*2**.5))<2
objective=pixels('vdp4-objectif')[620:960,250:1680]
assert not (objective.max(axis=2)<100).any(),'Objective samples carried into source slide 4'
sets=pixels('vdp4-reels')[365:525,300:1620]
assert not (sets.max(axis=2)<100).any(),'Previous property sentence carried into source slide 37'
report=dict(piAnchorStable=True,piNumberPixelBounds=pi,
            previousIntegerRemoved=True,previousCaptionPixels=old_ink,
            propertyTextBlack=True,bluePropertyPixels=blue,
            sqrtTwoPointBetweenOneAndTwo=True,encodedPointX=round(point_x,3),
            objectiveExamplesEndOnSourceSlide=True,propertySentenceReplacedBySourceTable=True,
            pixelChecks='Actual decoded frames; source text and temporal membership audited separately')
(OUT/'encoded-layout-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Encoded π anchor stable; no old integer caption, property black, √2 point correctly placed')
