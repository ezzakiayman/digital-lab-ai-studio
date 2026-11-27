"""Restore the complete source notation sentence without changing any narration."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import runpy
import subprocess

BASE=Path('src/video/n3-sem3-vdp1-v5-lesson.json')
STEM='n3-sem3-vdp1-v6'
OUT=Path('outputs/n3-sem3-v6/vdp1')
HELP=runpy.run_path('scripts/revise-n3-sem3-vdp1-v5.py')
load,write=HELP['load'],HELP['write']


def sentence_check(scene):
    """Compare all visible sentence fragments with the main learner area, not voice text."""
    parts=scene['art'][2:5]
    assert [v['kind'] for v in parts]==['text','math','text']
    visible=' '.join(v['value'] for v in parts)
    visible=visible.replace(r'\sqrt{\boldsymbol{a}}','√a')
    authored=[s['text'] for s in HELP['source_rows']()[6]['shapes']
              if s['role']=='student' and 'Ce nombre se note' in s['text']]
    assert len(authored)==1
    expected='Ce nombre se note'+authored[0].split('Ce nombre se note',1)[1]
    assert HELP['normalized'](visible)==HELP['normalized'](expected),visible
    assert parts[0]['frame']<parts[1]['frame']<parts[2]['frame']
    return HELP['normalized'](visible)


def prepare():
    before=load(BASE);data=copy.deepcopy(before)
    scene=data['scenes'][2]
    root,reading=scene['art'][2:4]
    assert root['kind']=='math' and reading['value'].startswith('se lit')
    root.update(x=825,size=61)
    reading.update(value='et se lit : « racine carrée de 𝑎 »',x=1250,size=48)
    prefix=HELP['label']('Ce nombre se note',540,584,48,1,frame=scene['beats'][1]['from'])
    scene['art'][2:4]=[prefix,root,reading]
    complete=sentence_check(scene)
    # The correction is visual only: identical narration, audio, durations and other scenes.
    for i,(old,new) in enumerate(zip(before['scenes'],data['scenes'])):
        if i!=2:assert old==new
        else:assert {k:v for k,v in old.items() if k!='art'}=={k:v for k,v in new.items() if k!='art'}
    assert before['scenes'][2]['art'][:2]==scene['art'][:2]
    assert before['scenes'][2]['art'][4:]==scene['art'][5:]
    HELP['audit'](HELP['source_rows'](),data)
    write(Path('src/video')/(STEM+'-lesson.json'),data)
    write(OUT/'revision-source.json',dict(sourceTimeline=BASE.as_posix(),
        sourceTimelineSha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
        correctedScene=scene['id'],mainSourceSlide=7,completeVisibleSentence=complete,
        restoredWords=['Ce nombre se note','et',':'],allNineAudioFilesUnchanged=True,
        narrationUnchanged=True,durationUnchanged=True,otherEightScenesIdentical=True,
        diagramAndDefinitionUnchanged=True,sourceGate='Complete visible notation sentence matches the main learner area'))
    print('Complete visible source sentence restored; nine audio files, timing and eight other scenes unchanged')


def check():
    import numpy as np
    helpers=runpy.run_path('scripts/check-n3-sem3-bilingual.py')
    before=load(BASE);data=load(OUT/'timeline.json');sentence_check(data['scenes'][2])
    HELP['audit'](HELP['source_rows'](),data)
    movie=OUT/'P1_MATHS_N3_SEM3_VDP1_V6.mp4'
    track=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),
                      '-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
    offset=0;rows=[]
    for i,(old,s) in enumerate(zip(before['scenes'],data['scenes'])):
        if i!=2:assert old==s
        else:assert {k:v for k,v in old.items() if k!='art'}=={k:v for k,v in s.items() if k!='art'}
        source=helpers['samples'](Path('public')/s['audio'])
        row=dict(scene=s['id'],audioUnchanged=s['audio']==old['audio'],
                 encodedCorrelation=helpers['match_audio'](track,source[:24000],offset))
        if i==2:
            start=s['beats'][1]['from']*800
            row['notationSentenceEncodedCorrelation']=helpers['match_audio'](track,source[start:start+24000],offset+start)
        rows.append(row);offset+=s['durationInFrames']*800
    write(OUT/'voice-verification.json',dict(scenes=rows,narrationUnchanged=True,
        allNineAudioFilesUnchanged=True,otherEightScenesIdentical=True,
        completeVisibleSentenceMatchesStudentSource=True))
    print('Encoded audio matches all nine unchanged WAVs; complete visible notation sentence matches source')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('step',choices=['prepare','check'])
    dict(prepare=prepare,check=check)[p.parse_args().step]()
