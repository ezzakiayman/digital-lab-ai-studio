"""Revise only the quotient pronunciation insert; preserve six approved scenes."""
import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
import wave
import numpy as np

PREFIX=Path('src/video/n3-sem4-vdp2-v2')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def prepare():
    plan=read('src/video/n3-sem4-plan.json')
    scene=deepcopy(next(s for s in plan['scenes'] if s['episode']==2 and s['id'].endswith('prononciation')))
    text=['Écoutez la lecture du mot quotient.','Co.','Cyan.','Quotient.']
    scene.update(audio='n3-sem4-v2-kore/n3-sem4-vdp2-prononciation.wav',kind='pronunciation',art=[],
                 narration=' '.join(text),beats=[dict(stage=i,text=t,**{'from':0}) for i,t in enumerate(text)],
                 pronunciation=dict(word='quotient',syllables=['quo','tient'],style='simplifier',advances=[117,135]))
    write(str(PREFIX)+'-plan.json',dict(scenes=[scene]))
    write(str(PREFIX)+'-google-voice-plan.json',dict(scenes=[dict(id=scene['id'],audio=scene['audio'],
                                                              narration=scene['narration'],speechMode='verbatim')]))


def timeline():
    lesson=read('src/video/n3-sem4-vdp2-lesson.json')
    scene=read(str(PREFIX)+'-paced-plan.json')['scenes'][0]
    audio=Path('public')/scene['audio']
    alignment=read(audio.parent/'alignment'/(scene['id']+'.json'))
    assert alignment['signature']==hashlib.sha256(audio.read_bytes()+scene['narration'].encode()).hexdigest()
    # The reference insert starts with syllables, without an introductory caption or word.
    intro_words=len(scene['beats'][0]['text'].split())
    cut=round((alignment['words'][intro_words]['start']-.5)*24000)
    assert cut/24000>alignment['words'][intro_words-1]['end']+.1
    with wave.open(str(audio)) as w:
        params=w.getparams()
        assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(24000,1,2)
        w.setpos(cut)
        pcm=w.readframes(w.getnframes()-cut)
    gain_db=-3
    pcm=np.rint(np.frombuffer(pcm,dtype='<i2')*10**(gain_db/20)).astype('<i2').tobytes()
    target=Path('public/n3-sem4-kore-insert')/audio.name
    (target.parent/'alignment').mkdir(parents=True,exist_ok=True)
    with wave.open(str(target),'wb') as w:
        w.setparams(params)
        w.writeframes(pcm)
    receipt=read(str(audio)+'.json')
    receipt.update(sourceAudio=scene['audio'],cutLeadingSamples=cut,gainDb=gain_db,
                   processing='Reference pronunciation insert; introduction cut at silence; volume matched to the lesson')
    write(str(target)+'.json',receipt)
    scene['audio']=target.relative_to('public').as_posix()
    scene['beats'][0]['text']=''
    scene['narration']=' '.join(b['text'] for b in scene['beats'] if b['text'])
    alignment['words']=alignment['words'][intro_words:]
    for word in alignment['words']:
        word.update(start=round(word['start']-cut/24000,3),end=round(word['end']-cut/24000,3))
    alignment.update(signature=hashlib.sha256(target.read_bytes()+scene['narration'].encode()).hexdigest(),
                     sourceAudio=audio.as_posix(),cutLeadingSamples=cut)
    write(target.parent/'alignment'/(target.stem+'.json'),alignment)
    audio=target
    count=0
    for index,beat in enumerate(scene['beats']):
        beat['from']=round(alignment['words'][count]['start']*30) if index else 0
        count+=len([w for w in (re.sub(r'[^\wً-ْٰ]','',s) for s in beat['text'].split()) if w])
    assert count==len(alignment['words'])
    assert all(a['from']<b['from'] for a,b in zip(scene['beats'],scene['beats'][1:]))
    with wave.open(str(audio)) as w: seconds=w.getnframes()/w.getframerate()
    scene.update(timingMethod='MMS_FA known-transcript alignment, remapped after PCM cuts',holdSeconds=1.5,
                 durationInFrames=math.ceil((seconds+1.5)*30))
    scene.pop('episode')
    for i,old in enumerate(lesson['scenes']):
        if old['id']==scene['id']:lesson['scenes'][i]=scene
    assert [n for s in lesson['scenes'] for n in s['sourceSlides']]==list(range(1,17))
    write(str(PREFIX)+'-lesson.json',lesson)
    print('7 scenes; revised pronunciation',scene['durationInFrames'],'frames; other six scenes preserved')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('step',choices=['prepare','timeline'])
    (prepare if p.parse_args().step=='prepare' else timeline)()
