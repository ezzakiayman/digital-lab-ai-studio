"""Create the native After Effects file from the editable scene package (py-aep 0.20.0)."""
import argparse
import json
from bisect import bisect_right
from pathlib import Path
import py_aep
from py_aep import ImportOptions
from py_aep.enums import KeyframeInterpolationType
from py_aep.models.properties.shape import Shape
from collect import keyed

FPS=30
def keys(track):
    return track.get('keys') if isinstance(track,dict) else None

def first(track):
    return keys(track)[0][1] if keys(track) else track

def write(prop, track, convert=lambda v:v):
    if keys(track):
        points=keys(track)
        prop.set_values_at_times([k[0]/FPS for k in points],[convert(k[1]) for k in points])
        for key,record in zip(prop.keyframes,points):
            if len(record)>2 and record[2]=='hold':
                key.out_interpolation_type=KeyframeInterpolationType.HOLD
    else:
        prop.value=convert(track)

def at(track,f):
    points=keys(track)
    if not points:
        return track
    i=max(0,bisect_right([k[0] for k in points],f)-1)
    a=points[i]
    if i+1==len(points) or (len(a)>2 and a[2]=='hold'):
        return a[1]
    b=points[i+1]
    t=max(0,min(1,(f-a[0])/(b[0]-a[0])))
    return [u+(v-u)*t for u,v in zip(a[1],b[1])]

def native_shape(s):
    return Shape(s['vertices'],s['inTangents'],s['outTangents'],closed=s['closed'])

def clip(layer,d):
    samples=[]
    for f in range(d['start'],d['end']):
        x,y,w,h=at(d['maskRect'],f)
        px,py=at(d['position'],f)
        sx,sy=at(d.get('scale',[100,100]),f)
        ax,ay=(x-px)*100/sx,(y-py)*100/sy
        bx,by=ax+w*100/sx,ay+h*100/sy
        samples.append((f,[ax,ay,bx,by]))
    def rect(values):
        ax,ay,bx,by=values
        return Shape([[ax,ay],[bx,ay],[bx,by],[ax,by]],closed=True)
    mask=layer['ADBE Mask Parade'].add_property('ADBE Mask Atom')
    mask.name='Révélation de la syllabe'
    write(mask['ADBE Mask Shape'],keyed(samples),rect)

def make_text(comp,d):
    layer=comp.add_text(d['text'])
    doc=layer.text.source_text.value
    doc.font=d['font']
    doc.font_size=d['size']
    doc.apply_fill=True
    doc.apply_stroke=False
    doc.fill_color=first(d['fill'])
    layer.text.source_text.value=doc
    if keys(d['fill']):
        animator=layer.text['ADBE Text Animators'].add_property('ADBE Text Animator')
        animator.name='Couleur du mot'
        animator['ADBE Text Selectors'].add_property('ADBE Text Selector')
        color=animator['ADBE Text Animator Properties'].add_property('ADBE Text Fill Color')
        write(color,d['fill'],lambda rgb:[*rgb,1.0])
    return layer

def make_path(comp,d):
    layer=comp.add_shape()
    items=layer['ADBE Root Vectors Group']
    shape=items.add_property('ADBE Vector Shape - Group')
    write(shape['ADBE Vector Shape'],d['path'],native_shape)
    if 'fill' in d:
        fill=items.add_property('ADBE Vector Graphic - Fill')
        write(fill['ADBE Vector Fill Color'],d['fill'],lambda rgb:[*rgb,1.0])
    if 'stroke' in d:
        stroke=items.add_property('ADBE Vector Graphic - Stroke')
        write(stroke['ADBE Vector Stroke Color'],d['stroke'],lambda rgb:[*rgb,1.0])
        write(stroke['ADBE Vector Stroke Width'],d.get('strokeWidth',1))
        stroke['ADBE Vector Stroke Line Cap'].value={'butt':1,'round':2,'square':3}[d['lineCap']]
        stroke['ADBE Vector Stroke Line Join'].value={'miter':1,'round':2,'bevel':3}[d['lineJoin']]
    if 'trimEnd' in d and d['trimEnd']!=100:
        trim=items.add_property('ADBE Vector Filter - Trim')
        write(trim['ADBE Vector Trim End'],d['trimEnd'])
    return layer

def build(root):
    data=json.loads((root/'project.json').read_bytes())
    assert data['fps']==FPS
    project=py_aep.new('22.6x64',platform='windows').project
    scenes=project.root_folder.add_folder('Séquences à modifier')
    media=project.root_folder.add_folder('Médias')
    cache={}
    def footage(rel):
        if rel not in cache:
            file=(root/rel).resolve(strict=True)
            assert file.is_relative_to(root.resolve())
            item=project.import_file(ImportOptions(str(file)))
            item.parent_folder=media
            cache[rel]=item
        return cache[rel]
    total=sum(s['frames'] for s in data['scenes'])
    def comp(folder,name,n):
        c=folder.add_comp(name,data['width'],data['height'],1,n/FPS,FPS)
        c.bg_color=[1,1,1]
        return c
    master=comp(project.root_folder,data['name'],total)
    base=master.add_solid([1,1,1],'Fond blanc',1920,1080,1,total/FPS)
    base.locked=True
    start=0
    for s in data['scenes']:
        print(s['name'],flush=True)
        c=comp(scenes,s['name'],s['frames'])
        bg=c.add(base.source,s['frames']/FPS)
        bg.locked=True
        vo=c.add(footage(s['audio']))
        vo.name='Voix off — '+s['name']
        vo.audio_enabled=True
        for d in s['layers']:
            if d['type']=='path':
                layer=make_path(c,d)
            elif d['type']=='text':
                layer=make_text(c,d)
            elif d['type']=='image':
                layer=c.add(footage(d['asset']),s['frames']/FPS)
            else:
                raise ValueError(d['type'])
            layer.name=d['name']
            layer.transform.anchor_point.value=[0,0,0]
            write(layer.transform.position,d.get('position',[0,0]),lambda v:[*v,0])
            write(layer.transform.scale,d.get('scale',[100,100]),lambda v:[*v,100])
            write(layer.transform.opacity,d.get('opacity',100))
            if 'maskRect' in d:
                clip(layer,d)
            layer.in_point=d['start']/FPS
            layer.out_point=d['end']/FPS
        for m in s['markers']:
            c.marker_property.set_value_at_time(m['frame']/FPS,m['label'])
            master.marker_property.set_value_at_time((start+m['frame'])/FPS,m['label'])
        nested=master.add(c)
        nested.name=s['name']
        nested.start_time=start/FPS
        nested.in_point=start/FPS
        start+=s['frames']
        nested.out_point=start/FPS
    guide=master.add(footage(data['reference']))
    guide.name='Référence MP4 — activer pour comparer'
    guide.guide_layer=True
    guide.audio_enabled=False
    guide.enabled=False
    guide.locked=True
    dest=root/(data['name']+'.aep')
    project.save(dest)
    print(dest,flush=True)
    return dest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package_folder',type=Path)
    build(parser.parse_args().package_folder)

