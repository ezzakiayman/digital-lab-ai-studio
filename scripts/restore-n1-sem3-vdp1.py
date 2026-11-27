"""Restore the 23-slide source verbatim; only approved graphic/Arabic corrections persist."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import unicodedata
from xml.etree import ElementTree as ET
from zipfile import ZipFile

BASE = runpy.run_path('scripts/prepare-n1-sem3-vdp1.py')
RUNTIME = BASE['RUNTIME']
VIDEO = Path('src/video')
PUBLIC = Path('public')
STEM = 'n1-sem3-vdp1-v3'
SOURCE = Path('reference/n1-sem3-vdp1-v3-source.pptx')
OUT = Path('outputs') / STEM
PLAN = VIDEO / (STEM+'-plan.json')
PACED = VIDEO / (STEM+'-paced-plan.json')
AR = Path('public/n1-sem3-vdp1-v2/objectif-ar.wav')
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
TEXT = BASE['text']


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf8')


def normalized(value):
    return ' '.join(unicodedata.normalize('NFKC', value).split())


def read_source():
    """Retain drawing and OMML text in document order, with explicit band provenance."""
    rows = []
    with ZipFile(SOURCE) as deck:
        for number in range(1, 24):
            root = ET.fromstring(deck.read(f'ppt/slides/slide{number}.xml'))
            shapes = []
            for shape in root.findall('.//p:sp', NS):
                body = shape.find('p:txBody', NS)
                if body is None:
                    continue
                value = ''.join(t.text or '' for t in body.iter() if t.tag.endswith('}t')).strip()
                if not value:
                    continue
                off = shape.find('.//a:xfrm/a:off', NS)
                assert off is not None
                y = int(off.get('y'))
                role = 'voice' if y < 700000 else 'directions' if y >= 5000000 else 'student'
                shapes.append(dict(role=role, text=value, y=y))
            voices = [s['text'] for s in shapes if s['role']=='voice']
            assert len(voices)==1, (number, voices)
            rows.append(dict(slide=number, voice=voices[0], shapes=shapes))
    return rows


def oral(value):
    """Reading-only expansion of mathematical notation/ordinals, never paraphrasing."""
    value = normalized(value)
    for literal, spoken in [('1er', 'première'), ('2e', 'deuxième'),
                            ('(+7)', 'plus sept'), ('(−15)', 'moins quinze'), ('(+5)', 'plus cinq'),
                            ('(−6)', 'moins six'), ('(+4)', 'plus quatre'), ('(−3)', 'moins trois')]:
        value = value.replace(literal, spoken)
    return value


def set_beats(scene, values):
    scene['beats'] = [dict(stage=i, text=text, **{'from': 0}) for i, text in enumerate(values)]
    scene['narration'] = ' '.join(values)


def prepared():
    rows = read_source()
    voice = {row['slide']: oral(row['voice']) for row in rows}
    scenes = copy.deepcopy(BASE['main_scenes']())
    for scene in scenes:
        scene['audio'] = f'{STEM}/{scene["id"]}.wav'
    for scene, slides in zip(scenes[:4], [(1,2,3,4), (5,6), (7,8,9,10), (11,12)]):
        set_beats(scene, [voice[n] for n in slides])
    # Retain the exact source words, dividing only on the actual source signed numbers.
    conclusion = voice[18]
    pieces = conclusion.split('plus sept, moins quinze et plus cinq')
    assert len(pieces)==2 and not pieces[1], conclusion
    set_beats(scenes[4], [voice[n] for n in range(13,18)]+[
        pieces[0].rstrip(), 'plus sept,', 'moins quinze', 'et plus cinq'])
    for beat in scenes[4]['beats'][5:-1]:
        beat['pauseAfter'] = .28
    set_beats(scenes[5], [voice[19]])
    ending = voice[23]
    before, after = ending.split('moins six, plus quatre et moins trois')
    set_beats(scenes[6], [voice[n] for n in range(20,23)]+[
        before.rstrip(), 'moins six,', 'plus quatre', 'et moins trois'+after])
    for beat in scenes[6]['beats'][3:-1]:
        beat['pauseAfter'] = .28
    scenes[1]['art'] = [TEXT('Toute suite d’additions de nombres',479,1,68,weight=700),
                        TEXT('s’appelle : expression numérique.',655,1,68)]
    scenes[3]['art'] = [TEXT('Les nombres additionnés dans une expression numérique',468,1,51,weight=700),
                        TEXT('s’appellent : termes',646,1,70)]
    algebra = BASE['algebra']
    right = BASE['right']
    scenes[6]['art'] = [
        BASE['art']('card','Expression numérique',495,1,41,535,to=2,pulse=1),
        right(875,495,1,to=2),
        algebra(BASE['SUMMARY'],495,1,71,1280),
        BASE['art']('card','Terme',744,2,48,535,pulse=2),
        right(875,744,4),
        algebra('(−6)',744,4,58,1104), TEXT(',',747,5,50,1185),
        algebra('(+4)',744,5,58,1273), TEXT('et',744,6,38,1374),
        algebra('(−3)',744,6,58,1480),
        TEXT('Trois termes',872,6,49,1290,weight=700),
    ]
    # Objective's approved Arabic recording says the same source words, with tashkeel.
    assert re.search(r'[\u0600-\u06ff]', scenes[0]['narration'])
    audit(rows, scenes)
    return rows, scenes


def audit(rows, scenes):
    """A deterministic source gate, independent of whether the audio aligns well."""
    def comparable(value):
        return re.sub(r'\s+', ' ', value).strip()
    for scene in scenes:
        expected = ' '.join(oral(rows[n-1]['voice']) for n in scene['sourceSlides'])
        assert comparable(scene['narration'])==comparable(expected), scene['id']
    assert [n for s in scenes for n in s['sourceSlides']]==list(range(1,24))
    for index, slide in [(1,6), (3,12)]:
        visible = ' '.join(v['value'] for v in scenes[index]['art'])
        originals = [s['text'] for s in rows[slide-1]['shapes'] if s['role']=='student'
                     and not s['text'].startswith('Définition')]
        assert len(originals)==1 and normalized(visible)==normalized(originals[0]), slide
    # All remaining non-template visible strings must exist in a source learner shape.
    learners = [normalized(s['text']).replace('–','−') for row in rows for s in row['shapes'] if s['role']=='student']
    allowed = {'+','-','down','right',',','et','(+7)','(−15)','(+5)','(−6)','(+4)','(−3)'}
    for scene in scenes:
        for visual in scene['art']:
            text=normalized(visual['value'])
            assert text in allowed or any(text in source for source in learners), (scene['id'], text)


def prepare():
    rows, scenes = prepared()
    write(PLAN, {'scenes': scenes})
    intro = copy.deepcopy(scenes[0])
    french = re.split(r'(?=[\u0600-\u06ff])', intro['narration'], maxsplit=1)[0].strip()
    intro.update(id=intro['id']+'-fr', audio=f'{STEM}/objectif-fr.wav', narration=french)
    write(VIDEO/(STEM+'-voice-plan.json'), {'scenes':[intro, *scenes[1:5], scenes[6]]})
    # The original lead-in already says these exact words; only quote/period typography differs.
    source = Path('public/n1-sem3-vdp1/n1-sem3-vdp1-prononciation.wav')
    dest = PUBLIC/scenes[5]['audio']
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    write(Path(str(dest)+'.json'), {**load(Path(str(source)+'.json')),
          'sourceAudio':source.as_posix(),'processing':'Original lead-in reused; spoken words unchanged'})
    write(OUT/'source-audit.json', {
        'source':SOURCE.as_posix(), 'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'slides':rows, 'authoredVoiceMatchesAll23SourceBands':True,
        'visibleDefinitionsMatchSource':True,
        'readingOnlyExpansions':'1er/2e as ordinal words; signed mathematical notation read aloud; NFKC glyph/space normalization',
        'approvedExceptions':['Arabic حصة pronunciation recording retained from V2','Operation plus remains black'],
        'productionBandsVisible':False,
    })
    print('Source gate passed: 23 narration bands, two exact visible definitions, original repetitions')


def assemble():
    fr=PUBLIC/STEM/'objectif-fr.wav'
    ar=BASE['pcm'](AR)
    french=BASE['pcm'](fr)
    gap=bytes(round(.28*24000)*2)
    dest=PUBLIC/STEM/'n1-sem3-vdp1-objectif.wav'
    BASE['save_wave'](dest,french+gap+ar)
    tag=load(Path(str(fr)+'.json'))
    ar_tag=load(Path(str(AR)+'.json'))
    tag.update(arabicModel=ar_tag['model'],arabicVoice=ar_tag['voice'],arabicLanguageCode='ar',
               arabicStartSample=(len(french)+len(gap))//2,arabicSamples=len(ar)//2,
               parts=[fr.as_posix(),AR.as_posix()])
    write(Path(str(dest)+'.json'),tag)


def diction():
    """Keep the source words; punctuation-only metadata clarifies the start of Toute suite."""
    import numpy as np
    source=PUBLIC/STEM/'n1-sem3-vdp1-definition-expression.wav'
    backup=source.with_name('definition-expression-first-take.wav')
    if not backup.exists():
        shutil.copyfile(source,backup)
        shutil.copyfile(Path(str(source)+'.json'),Path(str(backup)+'.json'))
    alignment=load(source.parent/'alignment'/'n1-sem3-vdp1-definition-expression.json')
    # First sentence stays sample-identical. Its endpoint comes from the first take.
    boundary=next(i for i,w in enumerate(alignment['words']) if w['word']=='Toute')
    assert boundary==8
    end=alignment['words'][boundary-1]['end']
    lead=BASE['pcm'](backup)[:round((end+.10)*24000)*2]
    parts=[]
    audit_parts=[]
    for name in ['definition-articulated']:
        path=PUBLIC/STEM/(name+'.wav')
        raw=BASE['pcm'](path)
        pcm=np.frombuffer(raw,dtype='<i2')
        active=np.flatnonzero(np.abs(pcm.astype(np.int32))>65)
        assert active.size
        start=max(0,int(active[0]) - 1920)
        stop=min(len(pcm),int(active[-1])+1921)
        parts.append(raw[start*2:stop*2])
        audit_parts.append(dict(audio=path.as_posix(),startSample=start,endSample=stop))
    recipe=load(VIDEO/(STEM+'-definition-articulated-plan.json'))
    # Only a reading pause and terminal punctuation differ from the source voice band.
    compare=lambda t: re.sub(r'[,\.\s]','',t)
    assert compare(recipe['scenes'][0]['narration'])==compare(oral(read_source()[5]['voice']))
    BASE['save_wave'](source,lead+bytes(round(.45*24000)*2)+parts[0])
    tag=load(Path(str(backup)+'.json'))
    tag.update(processing='Original lead-in, same source words with a reading pause after Toute',
               dictionParts=audit_parts, originalLeadSamples=len(lead)//2)
    write(Path(str(source)+'.json'),tag)
    print('Diction adjusted with identical source words; original lead-in retained')


def timeline():
    rows, expected = prepared()
    plan=load(PACED)
    assert [s['narration'] for s in plan['scenes']]==[s['narration'] for s in expected]
    result={1:dict(version=1,lesson=BASE['TITLE'],level='1AC',videoType='VDP',fps=30,scenes=[])}
    RUNTIME['finish_timeline'](plan,result,prefix='n1-sem3-vdp',suffix='-v3',counts={1:23})
    data=result[1]
    # Use the original clip and its original sound together, on an exact frame boundary.
    item=data['scenes'][5]
    lead=PUBLIC/item['audio']
    clip=Path('public/n1-sem3-vdp1/prononciation-expression.mp4')
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(clip),'-ac','1','-ar','24000','-f','s16le','-'])
    before=BASE['pcm'](lead)
    start=math.ceil((len(before)/48000+.25)*30)
    dest=lead.with_name(lead.stem+'-source.wav')
    BASE['save_wave'](dest,before+bytes(start*1600-len(before))+raw)
    tag=load(Path(str(lead)+'.json'))
    tag.update(embeddedSource='Slide 19 original pronunciation video',embeddedStartFrame=start,embeddedFrames=math.floor(len(raw)/1600))
    write(Path(str(dest)+'.json'),tag)
    item.update(audio=dest.relative_to(PUBLIC).as_posix(),durationInFrames=start+math.ceil(len(raw)/1600)+21,
                timingMethod='Source pronunciation clip synchronized to its own audio')
    item['art'].append(BASE['art']('clip',clip.relative_to(PUBLIC).as_posix(),703,0,434,
                                  frame=start,clipFrames=math.floor(len(raw)/1600)))
    # Place the example after its source words "par exemple", with its original right arrow.
    vocab=data['scenes'][6]
    alignment=load((PUBLIC/vocab['audio']).parent/'alignment'/(vocab['id']+'.json'))
    words=alignment['words']
    cursor=0
    for beat in vocab['beats'][:2]:
        cursor += len(RUNTIME['words'](beat['text']))
    example_end=round(words[cursor-1]['end']*30)
    vocab['art'][1]['frame']=max(vocab['beats'][1]['from']+12,example_end-12)
    vocab['art'][2]['frame']=example_end+8
    write(VIDEO/(STEM+'-lesson.json'),data)
    print('Final source-faithful timeline:',sum(s['durationInFrames'] for s in data['scenes']),'frames')


def check():
    """Recheck authored source fidelity and the corrected/source inserts in encoded audio."""
    import numpy as np
    helpers=runpy.run_path('scripts/check-n3-sem3-bilingual.py')
    rows,expected=prepared()
    data=load(OUT/'timeline.json')
    assert [s['narration'] for s in data['scenes']]==[s['narration'] for s in expected]
    for index in [1,3]:
        assert data['scenes'][index]['art']==expected[index]['art']
    movie=OUT/'P1_MATHS_N1_SEM3_VDP1_V3.mp4'
    track=np.frombuffer(subprocess.check_output([
        'ffmpeg','-v','error','-i',str(movie),'-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
    offset=0
    report=[]
    for index,scene in enumerate(data['scenes']):
        audio=PUBLIC/scene['audio']
        pcm=helpers['samples'](audio)
        entry=dict(scene=scene['id'],sourceSlides=scene['sourceSlides'],
                   encodedStartCorrelation=helpers['match_audio'](track,pcm[:24000],offset))
        if index==0:
            tag=load(Path(str(audio)+'.json'))
            alignment=load(audio.parent/'alignment'/(scene['id']+'.json'))
            start=tag['arabicStartSample']
            start+=sum(g['frames'] for g in alignment['pauseEdits'] if g['sample']<=start)
            arabic=helpers['samples'](AR)
            assert np.array_equal(pcm[start:start+len(arabic)],arabic)
            entry.update(arabicStartSeconds=(offset+start)/24000,
                         approvedArabicCorrelation=helpers['match_audio'](track,arabic,offset+start))
        if index==1:
            tag=load(Path(str(audio)+'.json'))
            assert tag.get('dictionParts'), 'Use the selected articulated source take'
            entry['dictionParts']=tag['dictionParts']
        if index==5:
            clip=next(v for v in scene['art'] if v['kind']=='clip')
            raw=np.frombuffer(subprocess.check_output([
                'ffmpeg','-v','error','-i',str(PUBLIC/clip['value']),'-ac','1','-ar','24000','-f','s16le','-']),dtype='<i2')
            start=clip['frame']*800
            assert np.array_equal(pcm[start:start+len(raw)],raw)
            entry['sourcePronunciationCorrelation']=helpers['match_audio'](track,raw,offset+start)
        report.append(entry)
        offset+=scene['durationInFrames']*800
    write(OUT/'voice-verification.json',report)
    verification=load(OUT/'verification.json')
    verification.update(authoredSourceNarrationGate='passed for all 23 slide voice bands, with notation/ordinal oral expansions recorded',
                        visibleSourceDefinitions='matched',
                        audio='Gemini Kore French, approved isolated ElevenLabs Arabic insert, source pronunciation clip; AAC',
                        arabicModel=load(Path(str(AR)+'.json'))['model'])
    write(OUT/'verification.json',verification)
    print('Source narration gate, both definitions, seven encoded starts, Arabic and original clip verified')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','assemble','diction','timeline','check'])
    {'prepare':prepare,'assemble':assemble,'diction':diction,'timeline':timeline,'check':check}[parser.parse_args().action]()
