"""Check a portable Digital Lab After Effects source bundle against its delivered Remotion timeline."""
import argparse
import hashlib
import json
import math
import tempfile
import wave
from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath
from zipfile import ZipFile


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def normalized_member(name):
    path = PurePosixPath(name)
    require(name and ':' not in name and '\\' not in name and not path.is_absolute()
            and '..' not in path.parts, f'Unsafe archive member {name!r}')
    return path


def file_digest(path):
    with path.open('rb') as contents:
        return hashlib.file_digest(contents, 'sha256').hexdigest()


def local_asset(root, name):
    path = root.joinpath(*normalized_member(name).parts)
    require(path.is_file() and path.resolve().is_relative_to(root.resolve()), f'Missing bundled asset {name}')
    return path


def values(spec):
    if isinstance(spec, dict) and 'keys' in spec:
        return [v[1] for v in spec['keys']]
    return [spec]


def value_at(track,frame):
    if not isinstance(track,dict) or 'keys' not in track:
        return track
    keys=track['keys']
    current=keys[0]
    for nxt in keys[1:]:
        if frame<nxt[0]:
            if frame<=current[0] or len(current)>2 and current[2]=='hold':
                return current[1]
            t=(frame-current[0])/(nxt[0]-current[0])
            if isinstance(current[1],list):
                return [a+(b-a)*t for a,b in zip(current[1],nxt[1])]
            return current[1]+(nxt[1]-current[1])*t
        current=nxt
    return current[1]


def compare_numeric(actual,expected,detail,tolerance=.04):
    if isinstance(expected,(list,tuple)):
        require(isinstance(actual,(list,tuple)) and len(actual)>=len(expected),detail)
        for a,b in zip(actual,expected):
            compare_numeric(a,b,detail,tolerance)
    else:
        require(abs(actual-expected)<tolerance,f'{detail}: {actual} vs {expected}')


def check_layer(layer, duration, directory):
    require(layer.get('name') and layer['type'] in {'text','image','path'}, f'Invalid editable layer {layer}')
    lo, hi = layer['start'], layer['end']
    require(isinstance(lo, int) and isinstance(hi, int) and 0 <= lo < hi <= duration,
            f'Invalid range {layer["name"]} {lo}:{hi}')
    animated = 0
    for prop,spec in layer.items():
        if isinstance(spec, dict) and 'keys' in spec:
            keys = spec['keys']
            frames = [key[0] for key in keys]
            require(keys and all(isinstance(f,int) and 0 <= f <= duration for f in frames)
                    and frames == sorted(set(frames)), f'Invalid {prop} keyframes on {layer["name"]}')
            animated += int(len(keys)>1)
    if layer['type']=='text':
        require(all(isinstance(t,str) for t in values(layer['text'])), 'Invalid text source')
    if layer['type']=='image':
        local_asset(directory, layer['asset'])
    for prop in ('fill','stroke'):
        if prop in layer:
            for color in values(layer[prop]):
                if color is not None:
                    require(len(color) in (3,4) and all(math.isfinite(c) and 0<=c<=1 for c in color),
                            f'Invalid {prop}: {color}')
    if layer['type']=='path':
        for shape in values(layer['path']):
            coords = [shape[k] for k in ('vertices','inTangents','outTangents')]
            require(len(coords[0])>0 and len({len(c) for c in coords})==1,
                    f'Invalid Bezier arrays on {layer["name"]}')
            require(all(len(pt)==2 and all(math.isfinite(n) for n in pt) for c in coords for pt in c),
                    'Non-finite Bezier coordinate')
    return animated


def audit_project(bundle, timeline, production_root, expected_video):
    read = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
    project = read(bundle/'project.json')
    source = read(timeline)
    fps = source['fps']
    require((project['fps'],project['width'],project['height'])==(fps,1920,1080),'Project format differs from approved export')
    reference = local_asset(bundle,project['reference'])
    require(file_digest(reference)==file_digest(expected_video),'Reference MP4 differs from delivered video')
    original = source['scenes']
    scenes = project['scenes']
    require([s['id'] for s in scenes]==[s['id'] for s in original],'Scene order or content differs from video')
    layers = Counter()
    audio_files = []
    markers = []
    animated = 0
    offset=0
    for scene,old in zip(scenes,original):
        n = scene['frames']
        require(n==old['durationInFrames'],f'Duration mismatch {scene["id"]}')
        audio = local_asset(bundle,scene['audio'])
        require(file_digest(audio)==file_digest(production_root/'public'/old['audio']),f'WAV altered: {audio.name}')
        with wave.open(str(audio),'rb') as voice:
            require(voice.getnframes()/voice.getframerate()<=n/fps, f'Voice clipped in {scene["id"]}')
        audio_files.append(scene['audio'])
        require(scene.get('layers'),f'Blank scene {scene["id"]}')
        for marker in scene['markers']:
            require(0<=marker['frame']<n and marker['label'],f'Invalid marker: {marker}')
        actual = [m['frame'] for m in scene['markers']]
        expected = [b['from'] for b in old['beats']] if len(old['sourceSlides'])>1 else [0]
        require(all(t in actual for t in expected),f'Missing slide cues for {scene["id"]}: {expected} vs {actual}')
        markers.extend(offset+t for t in expected)
        for layer in scene['layers']:
            animated += check_layer(layer,n,bundle)
            layers[layer['type']]+=1
        offset+=n
    require(len(set(audio_files))==len(scenes), 'Voice stems are not independent per scene')
    require(layers['text']>0 and layers['path']>0 and layers['image']>0 and animated>0,
            'Project lacks expected editable content')
    return dict(scenes=len(scenes),frames=offset,fps=fps,slideMarkerFrames=markers,
                unchangedAudio=len(audio_files),referenceSha256=file_digest(reference),
                layers=dict(layers),animatedProperties=animated)


def audit_native(binary, project, bundle):
    """Parse the saved file anew in a relocated directory. This does not launch After Effects."""
    import py_aep
    from py_aep.binary.utils import recursive_find
    require(binary.read_bytes()[:4]==b'RIFX','The .aep is not a RIFX After Effects project')
    parsed=py_aep.parse(str(binary)).project
    comps=list(parsed.compositions)
    master_candidates=[c for c in comps if len(c.composition_layers)==len(project['scenes'])]
    require(len(master_candidates)==1,'Expected one editable master containing all scene comps')
    master=master_candidates[0]
    require((master.width,master.height,round(master.frame_rate))==(1920,1080,project['fps']), 'Master format')
    require(round(master.duration*project['fps'])==sum(s['frames'] for s in project['scenes']), 'Master length')
    require(len(master.guide_layers)==1 and not master.guide_layers[0].enabled
            and not master.guide_layers[0].audio_enabled, 'Reference MP4 must be a disabled, muted guide')
    nested=sorted(master.composition_layers,key=lambda l:l.start_time)
    rows=[]
    offset=0
    checks=Counter()
    for layer,scene in zip(nested,project['scenes']):
        comp=layer.source
        require(round(layer.start_time*project['fps'])==offset,'Scene master offset does not match')
        require(round(comp.duration*project['fps'])==scene['frames'],'Nested comp duration does not match')
        require(round(layer.in_point*project['fps'])==offset and round(layer.out_point*project['fps'])==offset+scene['frames'],
                'Nested scene clipping or offset differs from timeline')
        expected_marks=[(x['frame'],x['label']) for x in scene['markers']]
        actual_marks=[(round(k.time*project['fps']),k.value.comment) for k in comp.marker_property.keyframes]
        require(expected_marks==actual_marks,f'Native markers differ in {comp.name}')
        master_marks={(round(k.time*project['fps']),k.value.comment) for k in master.marker_property.keyframes}
        require(all((offset+frame,label) in master_marks for frame,label in expected_marks),'Missing master markers')
        offset+=scene['frames']
        kinds=Counter(l['type'] for l in scene['layers'])
        require(len(comp.text_layers)>=kinds['text'],f'Missing native text in {comp.name}')
        require(len(comp.shape_layers)>=kinds['path'],f'Missing native vector shapes in {comp.name}')
        files=comp.file_layers
        stems=[l for l in files if l.source.file and Path(l.source.file).suffix.lower()=='.wav']
        require(len(stems)==1 and stems[0].audio_enabled, f'Audio missing or muted in {comp.name}')
        require(Path(stems[0].source.file).name==Path(scene['audio']).name,
                f'Wrong voice in {comp.name}')
        editable=[l for l in reversed(comp.layers) if l in comp.text_layers or l in comp.shape_layers
                  or (l in comp.file_layers and Path(l.source.file).suffix.lower()=='.png')]
        require(len(editable)==len(scene['layers']), f'Layer count in {comp.name}')
        for source, saved in zip(scene['layers'],editable):
            require(saved.name==source['name'],f'Wrong layer order or name {comp.name} / {source["name"]}')
            require((round(saved.in_point*project['fps']),round(saved.out_point*project['fps']))==(source['start'],source['end']),
                    f'Native layer clipped {comp.name} / {saved.name}')
            if source['type']=='text':
                doc=saved.text.source_text.value
                require(doc.text==source['text'] and doc.font==source['font'] and abs(doc.font_size-source['size'])<.05,
                        f'Native text differs in {comp.name} / {saved.name}')
                compare_numeric(doc.fill_color,values(source['fill'])[0],f'Source text fill {saved.name}')
                if isinstance(source['fill'],dict):
                    animator=next(iter(saved.text['ADBE Text Animators']))
                    color=animator['ADBE Text Animator Properties']['ADBE Text Fill Color']
                    authored=source['fill']['keys']
                    time,expected,*_=authored[len(authored)//2]
                    compare_numeric(color.value_at_time(time/project['fps']),expected,'Text color animation')
                    checks['animatedTextColors']+=1
            if source['type']=='path':
                require(saved in comp.shape_layers,f'Non-editable shape {saved.name}')
                contents=saved['ADBE Root Vectors Group']
                shape_prop=contents['ADBE Vector Shape - Group']['ADBE Vector Shape']
                shape=source['path']
                points=shape['keys'] if 'keys' in shape else [[source['start'],shape]]
                time,expected,*_=points[len(points)//2]
                actual=shape_prop.value_at_time(time/project['fps'])
                for attr,key in [('vertices','vertices'),('in_tangents','inTangents'),('out_tangents','outTangents')]:
                    compare_numeric(getattr(actual,attr),expected[key],f'Vector {saved.name} {key}')
                require(actual.closed==expected['closed'],f'Path closed state {saved.name}')
                checks['vectorPaths']+=1
                if len(points)>1:
                    checks['animatedVectorPaths']+=1
                if 'trimEnd' in source and source['trimEnd']!=100:
                    track=source['trimEnd']
                    time=track['keys'][len(track['keys'])//2][0] if isinstance(track,dict) else source['start']
                    trim=contents['ADBE Vector Filter - Trim']['ADBE Vector Trim End']
                    compare_numeric(trim.value_at_time(time/project['fps']),value_at(track,time),'Trim End')
                    checks['trimOperators']+=1
            if 'maskRect' in source:
                mask=next(iter(saved['ADBE Mask Parade']))['ADBE Mask Shape']
                keys=mask.keyframes
                sample=keys[len(keys)//2]
                frame=round(sample.time*project['fps'])
                x,y,w,h=value_at(source['maskRect'],frame)
                tx,ty=value_at(source['position'],frame)
                sx,sy=value_at(source.get('scale',[100,100]),frame)
                actual=[(tx+a*sx/100,ty+b*sy/100) for a,b in sample.value.vertices]
                compare_numeric(actual,[(x,y),(x+w,y),(x+w,y+h),(x,y+h)],f'Syllable clip {saved.name}')
                checks['nativeMasks']+=1
            for prop in ('position','scale','opacity'):
                if prop not in source:
                    continue
                spec=source[prop]
                native=getattr(saved.transform,prop)
                points=spec['keys'] if isinstance(spec,dict) else [[source['start'],spec]]
                for f,expected,*_ in (points[:1]+[points[len(points)//2]]+points[-1:]):
                    val=native.value_at_time(f/project['fps'])
                    nums=expected if isinstance(expected,list) else [expected]
                    actual=val if isinstance(val,(tuple,list)) else [val]
                    require(all(abs(a-b)<.025 for a,b in zip(actual,nums)),f'Native key mismatch {saved.name} / {prop} {f}: {actual} vs {nums}')
        rows.append(dict(name=comp.name,frames=scene['frames'],text=len(comp.text_layers),shapes=len(comp.shape_layers)))
    assets={project['reference'],*(s['audio'] for s in project['scenes']),
            *(l['asset'] for s in project['scenes'] for l in s['layers'] if l['type']=='image')}
    resolved=set()
    for ref in recursive_find(parsed._rifx.chunks,chunk_type='alas',skip_unparsed=True):
        data=json.loads(ref.value)
        target=PureWindowsPath(data['fullpath'])
        ascent=data['ascendcount_base']
        tail=data['ascendcount_target']
        require(ascent==1 and 0<tail<len(target.parts),f'Asset cannot be relocated: {target.name}')
        rel=Path(*target.parts[-tail:]).as_posix()
        local_asset(bundle,rel)
        resolved.add(rel)
    require(resolved==assets,'Embedded relative file references differ from the supplied package')
    return dict(master=master.name,sceneComps=rows,nativeReader='py_aep',relativeMediaLinks=sorted(resolved),
                sampledNativeProperties=dict(checks))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('package',type=Path)
    p.add_argument('--timeline',type=Path,required=True)
    p.add_argument('--reference',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--native',action='store_true',help='Parse and audit a genuine .aep with py_aep.')
    args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.out,prefix='relocated-') as tmp:
        if args.package.is_dir():
            bundle=args.package
            archive=None
        else:
            with ZipFile(args.package) as z:
                names = [normalized_member(entry.filename).as_posix() for entry in z.infolist()]
                require(len(set(n.casefold() for n in names))==len(names),'Duplicate filename in package')
                require(z.testzip() is None,'Corrupt ZIP')
                require(not any(PurePosixPath(n).suffix.lower() in {'.pem','.dpapi','.env','.pptx','.docx'} for n in names),'Unexpected private source file')
                z.extractall(tmp)
            matches=list(Path(tmp).rglob('project.json'))
            require(len(matches)==1,'Expected one project.json in the ZIP')
            bundle=matches[0].parent
            archive=dict(name=args.package.name,sha256=file_digest(args.package),files=len(names),relocated=True)
        root=args.timeline.resolve().parents[2]
        stats=audit_project(bundle,args.timeline,root,args.reference)
        check=dict(archive=archive,project=stats)
        if args.native:
            natives=list(bundle.rglob('*.aep'))
            require(len(natives)==1,'Expected one binary .aep')
            check['aep']=audit_native(natives[0],json.loads((bundle/'project.json').read_bytes()),bundle)
        check['scope']='Portable resources, native data structures and timeline checks. Adobe-hosted playback is a separate check.'
        (args.out/'package-check.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(stats,ensure_ascii=False))


if __name__=='__main__':
    main()

