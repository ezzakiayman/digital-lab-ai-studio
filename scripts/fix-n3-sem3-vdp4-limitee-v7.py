"""Apply the user's precise visible-word choice without changing any narration."""
import argparse
import copy
import hashlib
from pathlib import Path
import runpy
import subprocess

H=runpy.run_path('scripts/revise-n3-sem3-vdp4-v6.py')
M=H['M']
load,write=H['load'],H['write']
BASE=Path('src/video/n3-sem3-vdp4-v6-lesson.json')
DEST=Path('src/video/n3-sem3-vdp4-v7-lesson.json')
OUT=Path('outputs/n3-sem3-v7/vdp4')


def delta_check(data):
    expected=copy.deepcopy(load(BASE))
    scene=expected['scenes'][4]
    assert scene['id']=='vdp4-rationnel-decimal'
    for i in [0,1]:
        assert scene['art'][i]['value'].count('finie')==1
        scene['art'][i]['value']=scene['art'][i]['value'].replace('finie','limitée')
    assert expected==data,'Change exceeds the approved visible-word replacement and matching invisible reserve'


def source_check(data):
    scene=data['scenes'][4]
    source=M['source_rows']()[10]
    caption=next(s['text'] for s in source['shapes'] if s['role']=='student' and s['text'].startswith(': une'))
    actual=M['semantic'](scene['art'][1]['value'])
    assert M['compact'](actual)==M['compact']('2,25 '+caption)
    assert 'écriture décimale limitée' in scene['narration']
    virtual=copy.deepcopy(data)
    virtual['scenes'][4]=load(BASE)['scenes'][4]
    H['source_check'](virtual)


def prepare():
    data=load(BASE)
    for i in [0,1]:
        data['scenes'][4]['art'][i]['value']=data['scenes'][4]['art'][i]['value'].replace('finie','limitée')
    delta_check(data)
    source_check(data)
    write(DEST,data)
    write(OUT/'revision-source.json',dict(date='2026-11-26',sourceSlide=11,
        exactUserChoice='« limitée », comme le storyboard et la voix',
        replacesEarlierInspectorCaptionChoice=True,visibleCaptionMatchesMainSource=True,
        invisibleReserveUpdatedToAvoidLayoutJump=True,allFourteenNarrationsAndAudioFilesUnchanged=True,
        allDurationsUnchanged=True,otherThirteenScenesIdentical=True,
        v6PropertyAndAudioRepairPreserved=True,sourceTimelineSha256=hashlib.sha256(BASE.read_bytes()).hexdigest()))
    print('Only approved visible word and its invisible layout reserve changed; all audio and timing identical')


def check():
    data=load(OUT/'timeline.json')
    delta_check(data)
    source_check(data)
    tracks=[]
    for version in [6,7]:
        movie=Path(f'outputs/n3-sem3-v{version}/vdp4/P1_MATHS_N3_SEM3_VDP4_V{version}.mp4')
        tracks.append(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-map','0:a:0','-c:a','copy','-f','adts','-']))
    assert tracks[0]==tracks[1],'AAC changed in a visual-only revision'
    write(OUT/'voice-verification.json',dict(encodedAacByteIdenticalToV6=True,
        aacSha256=hashlib.sha256(tracks[1]).hexdigest(),allFourteenNarrationsAndAudioFilesUnchanged=True,
        allDurationsUnchanged=True,otherThirteenScenesIdentical=True,
        visibleCaptionMatchesSourceAndVoice=True,v6PropertyAndAudioRepairPreserved=True))
    print('Entire encoded AAC byte-identical to V6; caption matches source and unchanged narration')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step',choices=['prepare','check'])
    dict(prepare=prepare,check=check)[parser.parse_args().step]()
