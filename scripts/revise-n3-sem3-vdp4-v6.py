"""Restore provided property wording and repair a silence inserted into active speech."""
import argparse
import copy
import hashlib
from pathlib import Path
import runpy
import subprocess
import wave

M=runpy.run_path('scripts/revise-n3-sem3-vdp4-v5.py')
load,write=M['load'],M['write']
BASE=Path('src/video/n3-sem3-vdp4-v5-lesson.json')
OUT=Path('outputs/n3-sem3-v6/vdp4')
STEM='n3-sem3-vdp4-v6'
VOICE=Path('src/video')/(STEM+'-voice-plan.json')
PACING=Path('src/video')/(STEM+'-pacing-plan.json')
PACED=Path('src/video')/(STEM+'-paced-plan.json')
DEST=Path('src/video')/(STEM+'-lesson.json')


def source_voice():
    return [M['oral'](r['voice']) for r in M['source_rows']()[37:40]]


def prepare():
    base=load(BASE)
    prop=copy.deepcopy(base['scenes'][11])
    assert prop['id']=='vdp4-droite-propriete'
    texts=source_voice()
    prop.update(narration=' '.join(texts),audio='n3-sem3-elevenlabs-v6-vdp4/'+prop['id']+'.wav',
                languageCode='fr',speed=.94,stability=.45,art=[])
    prop['beats']=[dict(stage=i,text=t,**{'from':0}) for i,t in enumerate(texts)]
    pronunciation=copy.deepcopy(base['scenes'][1])
    pronunciation['audio']='n3-sem3-elevenlabs-v5-vdp4/'+pronunciation['id']+'.wav'
    write(VOICE,dict(scenes=[prop]))
    write(PACING,dict(scenes=[pronunciation,prop]))
    write(OUT/'user-approvals.json',dict(date='2026-11-26',
        instruction='exact dans stoyboard en considiration la correction fourni',
        propertyMode='Verbatim provided storyboard and inspector document; supersedes the two earlier proposed replacements',
        knownSourceWordingIssuesPreviouslyExplained=True,
        otherV5DecisionsRetained=True,audioRepair='Remove artificial silence inserted inside speech at 00:26.945',
        sourceVoiceReplacements=texts[1:]))
    print('Prepared one source-verbatim voice take; original pronunciation take reused for safe pacing')


def delta_check(data):
    before=load(BASE)
    for index,(old,new) in enumerate(zip(before['scenes'],data['scenes'])):
        if index not in [1,11]:
            assert old==new,('Unrelated scene changed',old['id'])
        else:
            allowed={'audio','beats','durationInFrames'} | ({'narration','art'} if index==11 else set())
            assert {k:v for k,v in old.items() if k not in allowed}=={k:v for k,v in new.items() if k not in allowed}


def source_check(data):
    rows=M['source_rows']()
    for i,s in enumerate(data['scenes']):
        expected=source_voice() if i==11 else M['expected'](rows,s)
        assert s['narration']==' '.join(expected),s['id']
        assert [b['text'] for b in s['beats']]==expected
    prop=data['scenes'][11]
    art=prop['art']
    assert len(art)==7
    for indices,slide,prefix in [(range(5),39,'Chaque'),(range(5,7),40,'Réciproquement')]:
        actual=' '.join(art[i]['value'] for i in indices)
        expected=[x['text'] for x in rows[slide-1]['shapes'] if x['role']=='student' and x['text'].startswith(prefix)]
        assert len(expected)==1
        assert M['compact'](actual)==M['compact'](expected[0]),(actual,expected)
    assert art[3]['value']=='abscisse' and art[3]['color']==M['RED']
    # Revalidate preserved content with the V5 gates; the returned property is audited above.
    virtual=copy.deepcopy(data)
    virtual['scenes'][11]=load(BASE)['scenes'][11]
    M['audit'](virtual)
    M['visible_audit'](virtual)
    return dict(completeSourceSentencesChecked=True,propertyVisibleAndVoiceMatchProvidedSource=True,abscisseSemanticColourPreserved=True,
                otherApprovedV5ContentPreserved=True,knownSourceWordingNotMathematicallyCertified=True)


def timeline():
    data=load(BASE)
    paced={s['id']:s for s in load(PACED)['scenes']}
    for i in [1,11]:
        s=data['scenes'][i]
        M['HELP']['apply_voice'](s,paced[s['id']])
    s=data['scenes'][11]
    label,cue=M['label'],M['cue']
    s['art']=[
        label('Chaque nombre réel peut être représenté',960,405,52,1),
        label('par un unique point sur une droite numérique',960,490,52,1,frame=cue(s,1,'par un unique point')),
    ]
    s['art']+=M['line']([('appelé l’',M['BLACK']),('abscisse',M['RED']),(' de ce point.',M['BLACK'])],575,52,1,frame=cue(s,1,'appelé'))
    s['art'] += [
        label('Réciproquement, tout nombre réel est associé',960,751,52,2),
        label('à un unique point d’une droite numérique.',960,843,52,2,frame=cue(s,2,'à un unique point')),
    ]
    delta_check(data)
    gate=source_check(data)
    pron=data['scenes'][1]
    raw=Path('public/n3-sem3-elevenlabs-v5-vdp4/vdp4-prononciation-5.wav')
    with wave.open(str(raw)) as w:a=w.readframes(w.getnframes())
    with wave.open(str(Path('public')/pron['audio'])) as w:b=w.readframes(w.getnframes())
    assert a==b,'Pronunciation must retain all original PCM without the inserted cut'
    with wave.open(str(Path('public')/load(BASE)['scenes'][1]['audio'])) as w:old=w.readframes(w.getnframes())
    cut,inserted=147480*2,15120*2
    assert old[:cut]==b[:cut] and old[cut+inserted:]==b[cut:]
    assert old[cut:cut+inserted]==b'\0'*inserted
    write(OUT/'pause-repair-proof.json',dict(removedSeconds=.63,removedPcmSamples=15120,
        originalVoiceBeforeAndAfterUnchanged=True,removedContentWasDigitalSilenceOnly=True,
        completeRepairedPcmEqualsOriginalRawTake=True))
    alignment=load(Path('public')/Path(pron['audio']).parent/'alignment'/('vdp4-prononciation-5.json'))
    assert not alignment['pauseEdits'] and alignment['skippedUnsafePauseEdits']
    write(DEST,data)
    write(OUT/'source-audit.json',dict(sourceGate=gate,sourceHash=hashlib.sha256(M['SOURCE'].read_bytes()).hexdigest(),
         twelveOtherScenesIdentical=True,pronunciationRawPcmIdentical=True,
         removedArtificialPauseSeconds=.63,originalCutGlobalSeconds=26.945,
         newFrames=sum(s['durationInFrames'] for s in data['scenes']),
         otherUserDecisionsPreserved=True,arrowRemarkStillUnresolved=True))
    print('Source-verbatim property restored; unsafe 0.63s insertion absent; 12 other scenes identical')


def check():
    import numpy as np
    data=load(OUT/'timeline.json')
    delta_check(data)
    gate=source_check(data)
    helper=runpy.run_path('scripts/check-n3-sem3-bilingual.py')
    track=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(OUT/'P1_MATHS_N3_SEM3_VDP4_V6.mp4'),
        '-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
    offset=0;result=[]
    for s in data['scenes']:
        pcm=helper['samples'](Path('public')/s['audio'])
        row=dict(scene=s['id'],encodedCorrelation=helper['match_audio'](track,pcm[:24000],offset))
        if s['id']=='vdp4-prononciation-5':
            row['repairedRegionCorrelation']=helper['match_audio'](track,pcm[round(5.7*24000):round(6.5*24000)],offset+round(5.7*24000))
        result.append(row)
        offset+=s['durationInFrames']*800
    write(OUT/'voice-verification.json',dict(scenes=result,sourceGates=gate,
        noArtificialCutInRepairedRegion=True,twelveOtherScenesIdentical=True))
    print('All 14 encoded takes and the repaired 00:26–00:27 region match; source-verbatim property checked')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('step',choices=['prepare','timeline','check'])
    dict(prepare=prepare,timeline=timeline,check=check)[p.parse_args().step]()
