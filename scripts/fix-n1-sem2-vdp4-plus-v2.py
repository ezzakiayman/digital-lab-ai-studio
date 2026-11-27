"""Apply only the user's two explicit positive-sign corrections; preserve all audio."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess

BASE=Path('src/video/n1-sem2-vdp4-lesson.json')
DEST=Path('src/video/n1-sem2-vdp4-v2-lesson.json')
OUT=Path('outputs/n1-sem2-vdp4-v2')

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def expected():
    old=read(BASE)
    new=copy.deepcopy(old)
    scene=next(s for s in new['scenes'] if s['id']=='vdp4-opposes')
    assert scene['art'][2]['value']=='5'
    assert scene['art'][12]['value']==r'\text{L’opposé de }\textcolor{#D60019}{-5}\text{ est }\textcolor{#087746}{5}'
    scene['art'][2]['value']='+5'
    scene['art'][12]['value']=scene['art'][12]['value'].replace('{#087746}{5}','{#087746}{+5}')
    assert scene['art'][10]['value']==scene['art'][11]['value']=='5'
    return new

def main(step):
    if step=='prepare':
        save(DEST,expected())
        save(OUT/'revision-source.json',dict(userRequest='Ajouter le signe + devant cinq dans l’exemple et sa conclusion.',
            changedPaths=['scenes[2].art[2].value','scenes[2].art[12].value'],
            absoluteValuesRemainUnsigned=True,allAudioAndNarrationUnchanged=True,allDurationsUnchanged=True,
            sourceOriginalMovieMd5='1107769ae420cf21bac1f690197b518e',
            timecodeNote='La remarque cite 01:25–02:25 ; la vidéo livrée dure 85,077 s. Passages identifiés par contenu vers 00:23–00:41.',
            scope='Correction visuelle ciblée ; aucune réécriture ni certification nouvelle du reste du contenu historique.'))
        print('Two positive signs prepared; all other timeline fields identical')
        return
    timeline=read(OUT/'timeline.json')
    assert timeline==expected(),'Unexpected timeline change'
    audio=[]
    for movie in [Path('outputs/n1-sem2-vdp4/P1_MATHS_N1_SEM2_VDP4.mp4'),OUT/'P1_MATHS_N1_SEM2_VDP4_V2.mp4']:
        audio.append(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-map','0:a:0','-c:a','copy','-f','adts','-']))
    assert audio[0]==audio[1],'AAC changed'
    save(OUT/'voice-verification.json',dict(encodedAacByteIdenticalToV1=True,aacSha256=hashlib.sha256(audio[1]).hexdigest(),
        onlyTwoApprovedVisualChanges=True,allSixNarrationsUnchanged=True,allDurationsUnchanged=True,absoluteValuesRemainUnsigned=True))
    print('Exact two-field delta and byte-identical encoded AAC verified')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step',choices=['prepare','check'])
    main(parser.parse_args().step)
