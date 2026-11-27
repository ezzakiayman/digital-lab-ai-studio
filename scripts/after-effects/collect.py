"""Collect the verified lesson's media and convert sampled SVG properties to editable AE tracks."""
import argparse
import json
import shutil
from bisect import bisect_right
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

NAME = 'P1_MATHS_N2_SEM1_VDP4_V2'
ROOT = Path(__file__).resolve().parents[2]
LESSON_OUT = ROOT / 'outputs/n2-sem1-vdp4-v2'
DEFAULT = LESSON_OUT / 'after-effects' / NAME

def flat(value):
    if isinstance(value, (int,float)):
        return [value]
    if isinstance(value,list):
        return [n for sub in value for n in flat(sub)]
    if isinstance(value,dict):
        return flat([value[k] for k in ('vertices','inTangents','outTangents')])
    raise TypeError(type(value))

def keyed(samples, tolerance=.035):
    """Remove redundant sampled keys while preserving plateaus and one-frame cuts."""
    changes=[]
    for frame,value in samples:
        if not changes or value!=changes[-1][1]:
            changes.append([frame,value])
    if len(changes)==1:
        return changes[0][1]
    points=[]
    for frame,value in changes:
        if points and frame>points[-1][0]+1:
            points.append([frame-1,points[-1][1]])
        points.append([frame,value])
    try:
        arrays=[flat(v) for _,v in points]
    except TypeError:
        return {'keys':[[f,v,'hold'] for f,v in changes]}
    if len({len(a) for a in arrays})!=1:
        return {'keys':[[f,v,'hold'] for f,v in changes]}
    keep={0,len(points)-1}
    intervals=[(0,len(points)-1)]
    while intervals:
        a,b=intervals.pop()
        if b-a<2:
            continue
        start,stop=points[a][0],points[b][0]
        largest=0
        split=None
        for j in range(a+1,b):
            t=(points[j][0]-start)/(stop-start)
            error=max((abs(n-(u+(v-u)*t)) for n,u,v in zip(arrays[j],arrays[a],arrays[b])),default=0)
            if error>largest:
                largest,split=error,j
        if largest>tolerance:
            keep.add(split)
            intervals.extend(((a,split),(split,b)))
    return {'keys':[points[i] for i in sorted(keep)]}

def path_tracks(values):
    positions=[]
    outlines=[]
    for frame,shape in values:
        xs,ys=zip(*shape['vertices'])
        x,y=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2
        positions.append((frame,[x,y]))
        local=dict(shape,vertices=[[round(a-x,4),round(b-y,4)] for a,b in shape['vertices']])
        outlines.append((frame,local))
    return keyed(positions),keyed(outlines)

def packaged_layer(layer, art_dir):
    props=layer['props']
    result=dict(name=layer['name'],type=layer['kind'],start=layer['inFrame'],end=layer['outFrame'])
    for k in ('text','font','size','fill','stroke','strokeWidth','opacity','lineCap','lineJoin','trimEnd','maskRect','position','rotation','scale'):
        if k in props and not (layer['kind']=='image' and k=='size'):
            value=keyed(props[k],.0006 if k in ('fill','stroke') else .035)
            if value is not None:
                result[k]=value
    if layer['kind']=='text':
        result['justify']='left'
    if layer['kind']=='path':
        result['position'],result['path']=path_tracks(props['geometry'])
    if layer['kind']=='image':
        asset=Path(props['asset'][0][1]).name
        result['asset']='Assets/Art/'+asset
        with Image.open(art_dir/asset) as im:
            result['scale']=keyed([(f,[w/im.width*100,h/im.height*100]) for f,(w,h) in props['size']])
    return result

def shadow_art(art_dir):
    # Original SVG silhouette including the eight-pixel border and its 5 px Gaussian blur.
    im=Image.new('L',(1912,276))
    ImageDraw.Draw(im).rounded_rectangle((24,24,1888,252),radius=54,fill=140)
    alpha=im.filter(ImageFilter.GaussianBlur(5))
    rgba=Image.new('RGBA',im.size,(85,85,85,0))
    rgba.putalpha(alpha)
    rgba.save(art_dir/'ombre-objectif.png')

def build(capture,dest):
    voice_dir=dest/'Assets'/'Voix'
    art_dir=dest/'Assets'/'Art'
    ref_dir=dest/'Reference'
    for folder in (voice_dir,art_dir,ref_dir):
        folder.mkdir(parents=True,exist_ok=True)
    for name,path in [('objective-target.png', 'public/brand'),('microphone.png', 'public/n2-sem1-vdp4-v2')]:
        shutil.copyfile(ROOT/path/name,art_dir/name)
    reference=NAME+'.mp4'
    shutil.copyfile(LESSON_OUT/reference,ref_dir/reference)
    shadow_art(art_dir)
    tl=json.loads((ROOT/'src/video/n2-sem1-vdp4-v2-lesson.json').read_bytes())
    project=dict(name=NAME,width=1920,height=1080,fps=30,reference='Reference/'+reference,scenes=[])
    for index,(s,t) in enumerate(zip(capture['scenes'],tl['scenes'],strict=True),1):
        assert s['id']==t['id'] and s['frames']==t['durationInFrames']
        name=f"{index:02d} - {t['title']}"
        audio_name=f"{index:02d}-{s['id']}.wav"
        shutil.copyfile(ROOT/'public'/t['audio'],voice_dir/audio_name)
        scene=dict(id=s['id'],name=name,frames=s['frames'],audio='Assets/Voix/'+audio_name,markers=[],layers=[])
        for i,slide in enumerate(t['sourceSlides']):
            part=t['beats'][i]
            scene['markers'].append(dict(frame=part['from'],label=f"Diapo {slide:02d} — {part['text']}"))
        for layer in s['layers']:
            p=layer['props']
            native=packaged_layer(layer,art_dir)
            if 'shadow' in p and p['shadow'][0][1] is not None:
                positions=[]
                for f,shape in p['geometry']:
                    xs,ys=zip(*shape['vertices'])
                    positions.append((f,[min(xs)-16,min(ys)-12]))
                scene['layers'].append(dict(name='Ombre du bandeau',type='image',start=native['start'],end=native['end'],
                    position=keyed(positions),scale=[100,100],opacity=native.get('opacity',100),asset='Assets/Art/ombre-objectif.png'))
            scene['layers'].append(native)
        project['scenes'].append(scene)
    (dest/'project.json').write_text(json.dumps(project,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    return project

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture',type=Path)
    parser.add_argument('--dest',type=Path,default=DEFAULT)
    args=parser.parse_args()
    project=build(json.loads(args.capture.read_bytes()),args.dest)
    print('Editable layers:',sum(len(s['layers']) for s in project['scenes']))

