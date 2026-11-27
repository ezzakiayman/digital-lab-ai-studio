"""Retain Kore and the source word; force French locale and contextual French diction."""
import argparse,copy,hashlib,json,math,runpy,wave
from pathlib import Path

STEM='n1-sem3-vdp1-v5'
VIDEO=Path('src/video')
PUBLIC=Path('public')
OUT=Path('outputs')/STEM
BASE=VIDEO/'n1-sem3-vdp1-v4-lesson.json'
TOOLS=runpy.run_path('scripts/prepare-n1-sem3-vdp1.py')
STYLE='Français de France uniquement, accent français natif, diction pédagogique naturelle. Prononcer les r français et les voyelles nasales françaises. Les sons sont ɛks, pʁɛ, sjɔ̃, puis ɛkspʁɛsjɔ̃. Ne pas adopter une prononciation anglaise.'

def load(path):return json.loads(path.read_text(encoding='utf8'))
def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def prepare():
 original=load(BASE)['scenes'][5]
 texts=[b['text'] for b in original['beats']]
 scene=dict(id=original['id'],episode=1,kind='pronunciation',audio=f'{STEM}/expression-fr.wav',
  speechMode='verbatim',languageCode='fr-FR',speechStyle=STYLE,
  narration=' '.join(texts),beats=[dict(stage=i,text=t,**{'from':0}) for i,t in enumerate(texts)])
 assert texts[0].startswith('Écoutez la prononciation du mot')
 write(VIDEO/(STEM+'-voice-plan.json'),dict(scenes=[scene]))
 print('Full original French introduction plus the same syllables; fr-FR and French style metadata')

def timeline():
 before=load(BASE);data=copy.deepcopy(before)
 scene=data['scenes'][5];voice=load(VIDEO/(STEM+'-paced-plan.json'))['scenes'][0]
 audio=PUBLIC/voice['audio'];tag=load(Path(str(audio)+'.json'))
 assert (tag['provider'],tag['voice'],tag['languageCode'])==('gemini','Kore','fr-FR')
 assert tag['speechStyle']==STYLE
 alignment=load(audio.parent/'alignment'/(voice['id']+'.json'))
 assert alignment['signature']==hashlib.sha256(audio.read_bytes()+voice['narration'].encode()).hexdigest()
 beats=copy.deepcopy(voice['beats']);cursor=0
 for i,beat in enumerate(beats):
  beat['from']=round(alignment['words'][cursor]['start']*30) if i else 0
  cursor+=len(TOOLS['RUNTIME']['words'](beat['text']))
 assert cursor==len(alignment['words']) and all(a['from']<b['from'] for a,b in zip(beats,beats[1:]))
 assert [b['text'] for b in beats]==[b['text'] for b in scene['beats']]
 with wave.open(str(audio)) as w:seconds=w.getnframes()/w.getframerate()
 scene.update(audio=voice['audio'],beats=beats,holdSeconds=1.2,durationInFrames=math.ceil((seconds+1.2)*30),
              timingMethod='MMS_FA known-transcript alignment')
 for i,(a,b) in enumerate(zip(before['scenes'],data['scenes'])):
  if i!=5:assert a==b
 assert all(v['kind']!='clip' for s in data['scenes'] for v in s['art'])
 write(VIDEO/(STEM+'-lesson.json'),data)
 write(OUT/'revision-source.json',dict(sourceTimeline=BASE.as_posix(),unchangedScenes=6,
  sourceWordsUnchanged=True,nativePronunciationPreserved=True,languageCode='fr-FR',
  speechStyleMetadata=True,voice='Kore',pptMediaUsed=False))
 print('French-locale pronunciation',scene['durationInFrames'],'frames; six other scenes identical')

def check():
 import subprocess,numpy as np
 helpers=runpy.run_path('scripts/check-n3-sem3-bilingual.py')
 before=load(Path('outputs/n1-sem3-vdp1-v4/timeline.json'));after=load(OUT/'timeline.json')
 movie=OUT/'P1_MATHS_N1_SEM3_VDP1_V5.mp4'
 track=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
 offset=0;report=[]
 for i,(a,b) in enumerate(zip(before['scenes'],after['scenes'])):
  audio=PUBLIC/b['audio'];pcm=helpers['samples'](audio)
  r=dict(scene=b['id'],encodedStartCorrelation=helpers['match_audio'](track,pcm[:24000],offset))
  if i!=5:assert a==b
  else:
   tag=load(Path(str(audio)+'.json'));assert tag['languageCode']=='fr-FR' and tag['speechStyle']==STYLE and tag['voice']=='Kore'
   assert [x['text'] for x in a['beats']]==[x['text'] for x in b['beats']]
   assert a['art']==b['art'] and a['pronunciation']==b['pronunciation']
   start=b['beats'][1]['from']*800
   r.update(languageCode='fr-FR',pronunciationCorrelation=helpers['match_audio'](track,pcm[start:],offset+start))
  report.append(r);offset+=b['durationInFrames']*800
 write(OUT/'voice-verification.json',report)
 verification=load(OUT/'verification.json');verification.update(audio='Gemini Kore French, approved separate Arabic insert retained, AAC',vocabularyVoice=dict(provider='gemini',voice='Kore',languageCode='fr-FR',speechStyleMetadata=True),pptMediaUsed=False,unchangedScenes=6)
 write(OUT/'verification.json',verification)
 print('fr-FR, unspoken style metadata, same Kore voice/source wording and encoded insert verified')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('step',choices=['prepare','timeline','check'])
 dict(prepare=prepare,timeline=timeline,check=check)[p.parse_args().step]()
