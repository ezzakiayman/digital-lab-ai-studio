"""Verify preserved scenes, actual pronunciation audio, cues and encoded sound."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import numpy as np

helpers=runpy.run_path('scripts/check-n3-sem3-bilingual.py')
load,samples,match_audio,RATE=(helpers[k] for k in ('load','samples','match_audio','RATE'))
load=lambda path: helpers['load'](Path(path))
root=Path('outputs/n3-sem4-v2/vdp2')
prior=load('src/video/n3-sem4-vdp2-lesson.json')
current=load(root/'timeline.json')
assert current==load('src/video/n3-sem4-vdp2-v2-lesson.json')
movie=root/'P1_MATHS_N3_SEM4_VDP2_V2.mp4'
track=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-ac','1','-ar',str(RATE),'-f','f32le','-']),dtype='<f4')
report=[]
offset=0
for old,scene in zip(prior['scenes'],current['scenes']):
    audio=Path('public')/scene['audio']
    item=dict(scene=scene['id'],encodedAudioMatch=match_audio(track,samples(audio,count=RATE),offset))
    if not scene.get('pronunciation'):
        assert old==scene
        item['preserved']=True
    else:
        p=scene['pronunciation']
        assert p==dict(word='quotient',syllables=['quo','tient'],style='simplifier',advances=[117,135])
        receipt=load(str(audio)+'.json')
        assert receipt['provider']=='gemini' and receipt['voice']=='Kore'
        original=samples(Path('public')/receipt['sourceAudio'])[receipt['cutLeadingSamples']:]
        expected=np.rint(original.astype(np.float64)*10**(receipt['gainDb']/20)).astype('<i2')
        assert np.array_equal(samples(audio),expected)
        alignment=load(audio.parent/'alignment'/(scene['id']+'.json'))
        assert alignment['signature']==hashlib.sha256(audio.read_bytes()+scene['narration'].encode()).hexdigest()
        cues=[b['from'] for b in scene['beats'][1:]]
        assert cues==[round(w['start']*30) for w in alignment['words']]
        for i,cue in enumerate(cues):
            end=cues[i+1] if i+1<len(cues) else scene['durationInFrames']
            peak=float(np.abs(track[offset+cue*(RATE//30):offset+end*(RATE//30)]).max())
            assert peak>.02
        item.update(provider=receipt['provider'],voice=receipt['voice'],cueFrames=cues,
                    sourcePCM='Exact source cut with recorded volume gain',holdSeconds=scene['holdSeconds'])
    report.append(item)
    offset+=scene['durationInFrames']*(RATE//30)
assert sum(bool(x.get('preserved')) for x in report)==6
result=dict(unchangedScenes=6,scenes=report,limits='Known-transcript alignment and signal checks do not certify phoneme accuracy.')
(root/'revision-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
