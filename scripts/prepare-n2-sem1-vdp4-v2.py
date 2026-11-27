"""Build the 33-slide N2 SEM1 VDP4 timeline from its reviewed source and actual French audio cues."""
import argparse
import hashlib
import json
import runpy
import unicodedata
import zipfile
from xml.etree import ElementTree as ET
from pathlib import Path
from PIL import ImageFont

SOURCE_HASH = '4a70f4f3267284922bb9257f7060f622f8d63f6c16a8aff0523b88cbef3fba56'
OUT = Path('outputs/n2-sem1-vdp4-v2')
TIMELINE = Path('src/video/n2-sem1-vdp4-v2-lesson.json')
RUNTIME = runpy.run_path('scripts/prepare-n3-sem3.py')
TITLE = 'Identifier les éléments d’un monôme'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def normalized(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())

def review_pptx(path):
    """Read narration plus the learner text used to check the banner, definitions and duplicate."""
    ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
        'mc':'http://schemas.openxmlformats.org/markup-compatibility/2006'}
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    if sha!=SOURCE_HASH:
        raise ValueError('Review the new storyboard before using this version-specific layout')
    slides=[]
    with zipfile.ZipFile(path) as deck:
        for number in range(1,34):
            tree=ET.fromstring(deck.read(f'ppt/slides/slide{number}.xml'))
            objects=tree.find('p:cSld/p:spTree',ns)
            voices=[]
            visible=[]
            for item in objects:
                choice=item.find('mc:Choice',ns)
                shapes=[item] if choice is None else list(choice)
                for shape in shapes:
                    offset=shape.find('p:spPr/a:xfrm/a:off',ns)
                    if offset is None or not shape.tag.endswith('}sp'):
                        continue
                    paragraphs=shape.findall('p:txBody/a:p',ns)
                    string=' '.join(''.join(t.text or '' for t in part.iter() if t.tag.endswith('}t')) for part in paragraphs).strip()
                    if not string:
                        continue
                    y=int(offset.get('y'))
                    if y<750000:
                        voices.append(string)
                    elif number in (1,2,3,4,5,19,20,33) and y < (600 if number==33 else 520)*9525:
                        visible.append(string)
            assert len(voices)==1,number
            slides.append(dict(slide=number,voice=voices[0],learnerText=visible))
        artwork=deck.read('ppt/media/image40.png')
        assert hashlib.sha256(artwork).hexdigest()=='7739e6c55d2a2157d6eac979c07b8350b070a6104568c6ec0124ce64a396b846'
        asset=Path('public/n2-sem1-vdp4-v2/microphone.png')
        asset.parent.mkdir(parents=True,exist_ok=True)
        asset.write_bytes(artwork)
    return dict(sha256=sha,slides=slides)

def build(review, timing):
    assert review['sha256'] == timing['sourceSha256'] == SOURCE_HASH
    assert [s['slide'] for s in review['slides']] == list(range(1,34))
    assert [i for s in timing['scenes'] for i in s['sourceSlides']] == list(range(1,34))
    source = {s['slide']:s for s in review['slides']}
    scenes = []
    for voice in timing['scenes']:
        units = voice['units']
        first = voice['sourceSlides'][0]
        for unit in units:
            if unit['role'] == 'sourceVoice':
                assert normalized(unit['text']) == normalized(source[unit['slide']]['voice'])
        scene = {k:voice[k] for k in ('id','sourceSlides','narration','audio','durationInFrames')}
        scene.update(type='monomial-study',kind='diagram',title={
            1:'Déclaration de l’objectif',4:'Définition 1 : monôme',6:'Un seul terme',
            10:'Deux termes',14:'Coefficient et variables',19:'Définition 2 : degré d’un monôme',
            21:'Degré du monôme',27:'Monôme',28:'Degré',29:'Ce qu’il faut retenir',
        }[first],timingMethod='MMS_FA known-transcript alignment'+(', remapped after PCM insertion' if voice['quietPauseEdits'] else ''),cues={})
        scene['beats'] = [dict(stage=i,text=u['text'],**{'from':0 if i==0 else u['frame']}) for i,u in enumerate(units)]
        scene['wordCues'] = [dict(word=w['word'],startFrame=round(w['start']*30)) for w in voice['words']]
        if first == 1:
            text = RUNTIME['text']
            objective = RUNTIME['objective_art'](TITLE,[
                ('Identifier',1,text('c’est reconnaître',672,size=59,weight=700),text('un élément et le nommer.',752,size=59,weight=700)),
                ('les éléments d’un monôme',2),
            ])
            gloss = ' '.join(v['value'] for v in objective['links'][0]['art'])
            assert any(normalized(t)==gloss for t in source[2]['learnerText'])
            assert all(TITLE in source[n]['learnerText'] for n in [1,2,3])
            scene.update(type='vdp-sequence',kind='intro',objective=objective,art=[],speechMode='verbatim')
            del scene['wordCues']
        elif first in (4,19):
            lines = (['Un monôme est une expression algébrique','à un seul terme.'] if first==4 else
                     ['Le degré d’un monôme non nul est la somme','des exposants de ses variables.'])
            assert scene['title'] in source[first]['learnerText']
            assert any(normalized(t)==' '.join(lines) for t in source[first+1]['learnerText'])
            scene.update(kind='definition',lines=lines)
        elif first in (27,28):
            parts = ['Mo','nôme'] if first==27 else ['De','gré']
            font = ImageFont.truetype('arialbd.ttf',64)
            scene.update(kind='reading',reading=dict(word=''.join(parts),parts=parts,advances=[round(font.getlength(part),2) for part in parts]))
        elif first == 29:
            # The user explicitly chose to keep both visible occurrences on slide 33.
            assert source[33]['learnerText'].count('Degré')==2
            scene.update(kind='recap',showSourceDuplicate=True)
        scenes.append(scene)
    return dict(version=1,level='2AC',videoType='VDP',lesson=TITLE,fps=30,scenes=scenes)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path,help='Original 33-slide PPTX or its independently reviewed inventory JSON')
    args=parser.parse_args()
    review=review_pptx(args.source) if args.source.suffix.lower()=='.pptx' else read(args.source)
    result=build(review,read(OUT/'voice-timing.json'))
    TIMELINE.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(len(result['scenes']), 'scènes,',sum(s['durationInFrames'] for s in result['scenes']),'images')

