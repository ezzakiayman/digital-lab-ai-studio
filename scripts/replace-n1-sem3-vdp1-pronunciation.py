"""Generate native Expression pronunciation with the lesson voice, without PPT media."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import runpy
import wave

import numpy as np
from PIL import ImageFont

STEM='n1-sem3-vdp1-v4'
PUBLIC=Path('public')
OUT=Path('outputs')/STEM
VIDEO=Path('src/video')
BASE=VIDEO/'n1-sem3-vdp1-v3-lesson.json'
PARTS=['Ex','pre','ssion']
PHONES=['Èks.','Prè.','Sion.','Expression.']
TOOLS=runpy.run_path('scripts/prepare-n1-sem3-vdp1.py')


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def prepare():
    scene=dict(id='expression-syllables',kind='pronunciation',
               audio=f'{STEM}/expression-syllables.wav',speechMode='verbatim',
               narration=' '.join(PHONES),beats=[dict(stage=i,text=t,**{'from':0}) for i,t in enumerate(PHONES)])
    write(VIDEO/(STEM+'-voice-plan.json'),dict(scenes=[scene]))
    print('Generate Kore syllables and whole word; phonetic aids are never visible')


def timeline():
    original=load(BASE)
    data=copy.deepcopy(original)
    scene=data['scenes'][5]
    fresh=load(VIDEO/(STEM+'-paced-plan.json'))['scenes'][0]
    syllable_audio=PUBLIC/fresh['audio']
    alignment=load(syllable_audio.parent/'alignment'/(fresh['id']+'.json'))
    assert alignment['signature']==hashlib.sha256(syllable_audio.read_bytes()+fresh['narration'].encode()).hexdigest()
    assert len(alignment['words'])==4
    lead=Path('public/n1-sem3-vdp1-v3/n1-sem3-vdp1-prononciation.wav')
    intro=TOOLS['pcm'](lead)
    pronunciation=TOOLS['pcm'](syllable_audio)
    rate=24000
    gap=round(.55*rate)
    shift=len(intro)//2+gap
    dest=PUBLIC/STEM/'expression-complete.wav'
    # Match the active speech RMS of the original Kore lead, preserving pitch and rate.
    def active_rms(raw):
        pcm=np.frombuffer(raw,dtype='<i2').astype(np.float64)
        loud=pcm[np.abs(pcm)>250]
        return float(np.sqrt(np.mean(loud*loud)))
    gain_db=float(np.clip(20*math.log10(active_rms(intro)/active_rms(pronunciation)),-6,6))
    samples=np.frombuffer(pronunciation,dtype='<i2').astype(np.float64)
    gain=min(10**(gain_db/20),28000/max(1,float(np.abs(samples).max())))
    pronunciation=np.rint(samples*gain).astype('<i2').tobytes()
    dest.parent.mkdir(parents=True,exist_ok=True)
    TOOLS['save_wave'](dest,intro+bytes(gap*2)+pronunciation)
    lead_tag=load(Path(str(lead)+'.json'))
    tag=load(Path(str(syllable_audio)+'.json'))
    assert (tag['provider'],tag['voice'],tag['model'])==(lead_tag['provider'],lead_tag['voice'],lead_tag['model'])
    tag.update(sourceAudio=syllable_audio.relative_to(PUBLIC).as_posix(),
               sourceLead=lead.as_posix(),newPronunciationStartSample=shift,
               pronunciationGainDb=20*math.log10(gain),
               processing='Original source-wording Kore lead plus newly generated Kore syllables and word; no PPT video/audio')
    write(Path(str(dest)+'.json'),tag)
    lead_text=scene['beats'][0]['text']
    beats=[dict(stage=0,text=lead_text,**{'from':0})]
    beats.extend(dict(stage=i+1,text=t,**{'from':round((shift/rate+w['start'])*30)})
                 for i,(t,w) in enumerate(zip(PHONES,alignment['words'])))
    font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',64)
    advances=[round(font.getlength(part),3) for part in PARTS]
    scene.update(kind='pronunciation',art=[TOOLS['text']('Expression',594,0,130,color='#087ABA',weight=700,to=1)],audio=dest.relative_to(PUBLIC).as_posix(),beats=beats,
                 narration=' '.join([lead_text,*PHONES]),
                 pronunciation=dict(word='Expression',syllables=PARTS,style='simplifier',advances=advances),
                 durationInFrames=math.ceil((len(intro)/48000+gap/rate+len(pronunciation)/48000+1.2)*30),
                 holdSeconds=1.2,timingMethod='MMS_FA known-transcript alignment, remapped after PCM insertion')
    assert all(a['from']<b['from'] for a,b in zip(beats,beats[1:]))
    assert ''.join(PARTS)=='Expression'
    for i,(a,b) in enumerate(zip(original['scenes'],data['scenes'])):
        if i!=5:assert a==b
    assert not any(v['kind']=='clip' for s in data['scenes'] for v in s['art'])
    write(VIDEO/(STEM+'-lesson.json'),data)
    write(OUT/'revision-source.json',dict(sourceTimeline=BASE.as_posix(),
          unchangedScenes=6,sameVoice=dict(provider=tag['provider'],voice=tag['voice'],model=tag['model']),
          approvedSourceLeadUnchanged=True,syllables=PARTS,phoneticGuidesVisible=False,
          pptMediaUsed=False,pronunciationStartSample=shift,gainDb=20*math.log10(gain)))
    print('New native pronunciation:',scene['durationInFrames'],'frames; six other scenes unchanged')


def check():
    helpers=runpy.run_path('scripts/check-n3-sem3-bilingual.py')
    original=load(Path('outputs/n1-sem3-vdp1-v3/timeline.json'))
    data=load(OUT/'timeline.json')
    import subprocess
    video=OUT/'P1_MATHS_N1_SEM3_VDP1_V4.mp4'
    track=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
    offset=0;report=[]
    for i,(prior,scene) in enumerate(zip(original['scenes'],data['scenes'])):
        audio=PUBLIC/scene['audio'];pcm=helpers['samples'](audio)
        row=dict(scene=scene['id'],encodedStartCorrelation=helpers['match_audio'](track,pcm[:24000],offset))
        if i!=5:assert prior==scene
        else:
            assert scene['pronunciation']['syllables']==PARTS
            assert len(scene['art'])==1 and scene['art'][0]['value']=='Expression' and scene['art'][0]['to']==1
            tag=load(Path(str(audio)+'.json'));source=helpers['samples'](PUBLIC/tag['sourceAudio'])
            shift=tag['newPronunciationStartSample'];gain=10**(tag['pronunciationGainDb']/20)
            assert np.array_equal(pcm[shift:],np.rint(source.astype(np.float64)*gain).astype('<i2'))
            lead=helpers['samples'](Path(tag['sourceLead']))
            assert np.array_equal(pcm[:len(lead)],lead)
            row['newPronunciationCorrelation']=helpers['match_audio'](track,pcm[shift:],offset+shift)
            assert (tag['provider'],tag['voice'])==('gemini','Kore')
        assert not any(v['kind']=='clip' for v in scene['art'])
        report.append(row);offset+=scene['durationInFrames']*800
    write(OUT/'voice-verification.json',report)
    verification=load(OUT/'verification.json')
    verification.update(audio='Gemini Kore French; approved isolated Arabic insert retained; AAC',
                        vocabularyVoice=dict(provider='gemini',voice='Kore',model='gemini-3.8-flash-lite-tts'),
                        pptMediaUsed=False,unchangedScenes=6)
    write(OUT/'verification.json',verification)
    print('Same Kore voice, six identical scenes, original lead, no PPT media, encoded insert verified')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('step',choices=['prepare','timeline','check'])
    dict(prepare=prepare,timeline=timeline,check=check)[p.parse_args().step]()
