"""Convert reviewed, paced narration into frame cues for the two new 2AC videos."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import wave

parser=argparse.ArgumentParser()
parser.add_argument('stem',choices=['like-terms','polynomial-subtraction'])
stem=parser.parse_args().stem
base=Path('src/video')
plan=json.loads((base/f'{stem}-paced-plan.json').read_text(encoding='utf-8'))

def tokens(text):
    return [word for word in (re.sub(r'[^\wً-ْٰ]','',token).lower() for token in text.split()) if word]

for scene in plan['scenes']:
    audio=Path('public')/scene['audio']
    data=json.loads((audio.parent/'alignment'/(scene['id']+'.json')).read_text(encoding='utf-8'))
    assert data['signature']==hashlib.sha256(audio.read_bytes()+scene['narration'].encode()).hexdigest()
    words=data['words']
    offsets=[0]
    for beat in scene['beats']:
        index=offsets[-1]
        beat['from']=0 if index==0 else round(words[index]['start']*30)
        offsets.append(index+len(tokens(beat['text'])))
    assert offsets[-1]==len(words)
    with wave.open(str(audio)) as w:
        scene['durationInFrames']=math.ceil((w.getnframes()/w.getframerate()+scene.get('holdSeconds',.9))*30)
    scene['timingMethod']='MMS_FA known-transcript alignment'
    scene['cues']={}
    def cue(name,phrase,beat):
        start,end=offsets[beat:beat+2]
        expected=tokens(phrase)
        actual=[w['word'].lower() for w in words[start:end]]
        hits=[i for i in range(len(actual)-len(expected)+1) if actual[i:i+len(expected)]==expected]
        assert hits,(scene['id'],name,phrase)
        scene['cues'][name]=round(words[start+hits[0]]['start']*30)
    kind=scene['kind']
    if stem=='like-terms':
        if kind=='intro':
            cue('sum','deux ix plus',1)
            cue('likePair','deux ix et',2)
            cue('unlikePair','deux ix au cube',3)
        if kind=='definition':
            cue('sameVariables','ont les mêmes variables',1)
            cue('samePowers','avec les mêmes exposants',1)
        if kind=='comparison' and scene['example']=='like':
            cue('expand0','s’écrit cinq',3)
            cue('expand1','s’écrit quatre',3)
            cue('xPower','exposant de ix',4)
            cue('yPower','exposant de i grec',5)
        if kind=='synthesis':
            for i,(expression,result) in enumerate([('deux ix plus cinq','les termes sont'),('trois ix','les variables sont'),('cinq ix','l’exposant'),('trois ix','sont semblables')]):
                cue('summaryExample'+str(i),expression,i+1)
                cue('summaryResult'+str(i),result,i+1)
        if kind=='vocabulary':
            for i,term in enumerate(['terme','variables','exposant','semblables']):
                cue('word'+str(i),term,0)
    else:
        if kind=='intro':cue('difference','calculer leur différence',1)
        if kind=='vertical':
            cue('resultX','deux ix',3)
            cue('resultY','trois i grec',5)
    assert [b['from'] for b in scene['beats']]==sorted({b['from'] for b in scene['beats']})
(base/f'{stem}-lesson.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(stem,len(plan['scenes']),sum(s['durationInFrames'] for s in plan['scenes'])/30,'seconds')

