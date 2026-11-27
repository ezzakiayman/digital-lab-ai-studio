"""Inspector/source revision of the 18-slide square-root comparison lesson only."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import runpy
import subprocess
import unicodedata
import wave
from xml.etree import ElementTree as ET
from zipfile import ZipFile

TOOLS=runpy.run_path('scripts/revise-n3-sem3-vdp1-v5.py')
HELP=TOOLS['HELP']
load,write=TOOLS['load'],TOOLS['write']
formula,label,visual,cue=(HELP[k] for k in ('formula','label','visual','cue'))
NS=TOOLS['NS']
SOURCE=Path('reference/n3-sem3-vdp2-inspector-v5-source.pptx')
VIDEO=Path('src/video')
STEM='n3-sem3-vdp2-v5'
OUT=Path('outputs/n3-sem3-v5/vdp2')
PLAN=VIDEO/(STEM+'-voice-plan.json')
PACED=VIDEO/(STEM+'-paced-plan.json')
SKY='#007DAF'
RED='#D60019'


def source_rows():
    rows=[]
    with ZipFile(SOURCE) as deck:
        for n in range(1,19):
            root=ET.fromstring(deck.read(f'ppt/slides/slide{n}.xml'));shapes=[]
            for shape in root.findall('.//p:sp',NS):
                body=shape.find('p:txBody',NS)
                if body is None:continue
                text='\n'.join(TOOLS['source_text'](p) for p in body.findall('a:p',NS)).strip()
                if not text:continue
                off=shape.find('.//a:xfrm/a:off',NS);assert off is not None
                y=int(off.get('y'));role='voice' if y<900000 else 'directions' if y>=5700000 else 'student'
                shapes.append(dict(role=role,text=text,y=y))
            voices=[s['text'] for s in shapes if s['role']=='voice'];assert len(voices)==1,(n,voices)
            rows.append(dict(slide=n,voice=voices[0],shapes=shapes))
    return rows


def oral(text):
    text=TOOLS['normalized'](text)
    for a,b in [('0,25','zéro virgule vingt-cinq'),('-8','moins huit'),('-1','moins un'),
                ('12','douze'),('11','onze'),('10','dix'),('7','sept'),('5','cinq')]:
        text=text.replace(a,b)
    return text if text.endswith(('.', '?', '!')) else text+'.'


def expected(rows,scene):
    result=[]
    for n in scene['sourceSlides']:
        if n==2:
            result.append('Comparer, c’est utiliser l’un des symboles, supérieur à ou inférieur à.')
        elif n==3:continue # Inspector explicitly replaces the combined explanation in slides 2–3.
        elif n==14:
            result.append('Pourquoi ? Parce que le nombre sous le radical doit être positif.')
        else:result.append(oral(rows[n-1]['voice']))
    if scene['kind']=='pronunciation':result+=['Con.','Pa.','Ré.','Comparer.']
    return result


def audit(data):
    rows=source_rows()
    assert [n for s in data['scenes'] for n in s['sourceSlides']]==list(range(1,19))
    for s in data['scenes']:
        texts=expected(rows,s)
        assert [b['text'] for b in s['beats']]==texts,s['id']
        assert s['narration']==' '.join(texts),s['id']
        assert not s.get('transition') and all(a['kind']!='clip' for a in s['art'])
    all_voice=' '.join(s['narration'] for s in data['scenes'])
    assert 'strictement' not in all_voice and 'ou nul' not in all_voice
    assert 'périodique' not in all_voice
    assert data['scenes'][-1]['narration'].count('cette séance')==1


def prepare():
    data=load(VIDEO/'n3-sem3-vdp2-v4-lesson.json');rows=source_rows()
    for s in data['scenes']:
        phrases=expected(rows,s)
        s.update(narration=' '.join(phrases),audio=f'n3-sem3-elevenlabs-v5-vdp2/{s["id"]}.wav',
                 languageCode='fr',speed=.94,stability=.45)
        s['beats']=[dict(stage=i,text=t,**{'from':0}) for i,t in enumerate(phrases)]
        s.pop('transition',None)
    audit(data);write(PLAN,data)
    write(OUT/'source-audit.json',dict(source=SOURCE.as_posix(),sourceSha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        slides=rows,sourceNarrationRestored=True,approvedExceptions=[
          'Inspector: replace the combined slides 2–3 explanation with the requested French sentence',
          'Inspector: precise replacement of the why sentence, slide 14',
          'User rule: newly generated Com–pa–rer pronunciation with the main French voice; phonetic guides audio only',
          'Inspector: no black fades and textual Faux marker'],
        oralExpansions='Source numeric notation read aloud; final periods only; no lexical rewriting outside scoped exceptions',
        pending=[ 'The periodique capture does not match any of these 18 slides; attribution pending',
                  'Source image card spelling Racine carré: preserve unless user explicitly approves the final e'],
        pptMediaUsed=False,productionBandsVisible=False))
    approved=OUT/'user-approvals.json'
    if approved.exists():
        approval=load(approved);report=load(OUT/'source-audit.json')
        if approval.get('cardFinalE'):
            report['approvedExceptions'].append('User 25 November: source card typo corrected to Racine carrée')
            report['pending']=[p for p in report['pending'] if not p.startswith('Source image card')]
        if approval.get('periodiqueVideo'):
            report['crossLessonRemark']=dict(assignedByUser=approval['periodiqueVideo'],videoNotChanged=True)
            report['pending']=[p for p in report['pending'] if not p.startswith('The periodique capture')]
        write(OUT/'source-audit.json',report)
    for s in data['scenes']:print(s['id'],':',s['narration'])


def compact(value):
    return ''.join(unicodedata.normalize('NFKC',value).split()).replace('−','-')


def plain_formula(text):
    """Read the actual limited KaTeX vocabulary used here, including nested colour groups."""
    index=0
    def group():
        nonlocal index
        assert text[index]=='{';index+=1;out=''
        while index<len(text) and text[index]!='}':out+=token()
        assert index<len(text);index+=1
        return out
    def token():
        nonlocal index
        c=text[index]
        if c=='{':return group()
        if c!='\\':index+=1;return c
        index+=1;match=re.match(r'[A-Za-z]+',text[index:]);assert match,text[index:]
        name=match[0];index+=len(name)
        if name=='textcolor':group();return group()
        if name in ('textsf','boldsymbol'):return group()
        if name=='sqrt':return '√'+group()
        raise AssertionError(name)
    result=''
    while index<len(text):result+=token()
    return result


def visible_audit(data,correct_spelling):
    scenes={s['id'].removeprefix('vdp2-'):s for s in data['scenes']};rows=source_rows()
    original=next(s['text'] for s in rows[7]['shapes'] if s['role']=='student' and 'Pour tous' in s['text'])
    actual=' '.join(plain_formula(v['value']) for v in scenes['propriete']['art'])
    assert compact(actual)==compact(original),(actual,original)
    for name,indices,slide,needle in [
        ('exemple',[0,1,2],9,'5<11'),('exemple',[4,5,6],10,'√'),
        ('attention',[2],12,'−8'),('attention',[4,5,6],13,'√')]:
        actual=' '.join(plain_formula(scenes[name]['art'][i]['value']) for i in indices)
        authored=[s['text'] for s in rows[slide-1]['shapes'] if s['role']=='student' and needle in TOOLS['normalized'](s['text'])]
        assert len(authored)==1,(slide,authored)
        assert compact(actual)==compact(authored[0]),(actual,authored)
    cards=[v['value'] for v in scenes['vocabulaire']['art']]
    assert cards==['Comparer','Carré','Racine carrée' if correct_spelling else 'Racine carré']


def timeline(correct_spelling=False):
    from PIL import ImageFont
    approval=OUT/'user-approvals.json'
    correct_spelling=correct_spelling or (approval.exists() and load(approval).get('cardFinalE',False))
    data=load(PLAN);paced={s['id']:s for s in load(PACED)['scenes']}
    for s in data['scenes']:
        HELP['apply_voice'](s,paced[s['id']])
        for k in ('languageCode','speed','stability'):s.pop(k,None)
    scenes={s['id'].removeprefix('vdp2-'):s for s in data['scenes']}
    s=scenes['prononciation-6'];parts=['Com','pa','rer'];font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',64)
    s.update(pronunciation=dict(word='Comparer',syllables=parts,style='simplifier',advances=[round(font.getlength(p),3) for p in parts]),
             art=[label('Comparer',960,594,130,color='#087ABA',weight=700,to=1)],holdSeconds=1.2)
    with wave.open(str(Path('public')/s['audio'])) as clip:
        s['durationInFrames']=math.ceil((clip.getnframes()/clip.getframerate()+1.2)*30)
    s=scenes['propriete'];s['title']='Propriété 1'
    s['art']=[
        formula(r'\textsf{Pour tous nombres positifs }a\textsf{ et }b\textsf{ :}',960,416,55,1),
        formula(rf'\textsf{{Si }}\textcolor{{{SKY}}}{{\boldsymbol{{a}}<\boldsymbol{{b}}}}',960,590,95,1,frame=cue(s,1,'si')),
        formula(rf'\textsf{{alors }}\textcolor{{{SKY}}}{{\sqrt{{\boldsymbol{{a}}}}<\sqrt{{\boldsymbol{{b}}}}}}',960,793,95,1,frame=cue(s,1,'alors')),
    ]
    s=scenes['exemple']
    s['art']=[
        formula('5',800,439,107,pulseFrame=cue(s,0,'cinq')),
        formula('<',940,439,107,pulseFrame=cue(s,0,'inférieur')),
        formula('11',1115,439,107,pulseFrame=cue(s,0,'onze')),
        visual('arrow','down',960,603,65,1,color=RED,draw=True),
        formula(r'\textcolor{#D60019}{\sqrt{\textcolor{#1D1D1D}{5}}}',720,790,112,1,pulseFrame=cue(s,1,'cinq')),
        formula('<',960,790,112,1,pulseFrame=cue(s,1,'inférieure')),
        formula(r'\textcolor{#D60019}{\sqrt{\textcolor{#1D1D1D}{11}}}',1220,790,112,1,pulseFrame=cue(s,1,'onze')),
    ]
    s=scenes['attention'];at=cue(s,3,'nombre sous le radical')
    s['art']=[
        visual('alert','',960,449,112,pulse=0,to=1),
        visual('alert','',573,454,92,1),formula('-8<-1',960,454,104,1),
        visual('arrow','down',960,607,65,2,color=RED,draw=True),
        formula(r'\sqrt{\textcolor{#D60019}{-8}}',720,783,105,2,pulseFrame=at),
        formula('<',960,783,105,2),
        formula(r'\sqrt{\textcolor{#D60019}{-1}}',1220,783,105,2,pulseFrame=at),
        visual('status','Faux',1505,783,44,2,color=RED,pulse=3,repeatPulse=True),
    ]
    s=scenes['vocabulaire']
    s['art']=[
        visual('card','Comparer',590,437,52,pulseFrame=cue(s,1,'comparer')),
        visual('card','Carré',1330,437,52,pulseFrame=cue(s,3,'carré')),
        visual('card','Racine carrée' if correct_spelling else 'Racine carré',960,664,52,pulseFrame=cue(s,2,'racines carrées')),
    ]
    audit(data);visible_audit(data,correct_spelling)
    write(VIDEO/(STEM+'-lesson.json'),data)
    write(OUT/'visible-source-audit.json',dict(propertyParagraphMatchesWholeSource=True,
        allComparisonExpressionsMatchStudentSource=True,sourceCardImageReviewed=dict(
          path='reference/n3-sem3/vdp2/slides/Diapositive15.PNG',
          sha256=hashlib.sha256(Path('reference/n3-sem3/vdp2/slides/Diapositive15.PNG').read_bytes()).hexdigest()),
        sourceCardSpellingPreserved=not correct_spelling,spellingCorrectionExplicitlyApproved=correct_spelling,
        productionBandsVisible=False,blackFades=False,nativePronunciation=True,pptMediaUsed=False))
    print('V5 timeline:',sum(s['durationInFrames'] for s in data['scenes']),'frames; full visible property and four comparison expressions checked')


def check():
    import numpy as np
    helpers=runpy.run_path('scripts/check-n3-sem3-bilingual.py');data=load(OUT/'timeline.json');audit(data)
    visible_audit(data,load(OUT/'visible-source-audit.json')['spellingCorrectionExplicitlyApproved'])
    movie=OUT/'P1_MATHS_N3_SEM3_VDP2_V5.mp4'
    track=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
    rows=[];offset=0;events=[]
    for s in data['scenes']:
        p=Path('public')/s['audio'];tag=load(Path(str(p)+'.json'))
        assert (tag['voice'],tag['model'],tag['languageCode'])==('05Y5uLueU3x8LrkGHu0H','eleven_v4','fr')
        assert tag['settings']['speed']==.94 and tag['settings']['stability']==.45
        source=helpers['samples'](p)
        row=dict(scene=s['id'],encodedCorrelation=helpers['match_audio'](track,source[:24000],offset))
        if s.get('pronunciation'):
            row['unitCorrelations']=[]
            for b in s['beats'][1:]:
                start=b['from']*800;row['unitCorrelations'].append(helpers['match_audio'](track,source[start:start+16000],offset+start))
        rows.append(row)
        for i,a in enumerate(s['art']):
            if 'frame' in a or 'pulseFrame' in a:
                events.append(dict(scene=s['id'],index=i,value=a['value'],
                    seconds=round((offset/800+a.get('frame',a.get('pulseFrame')))/30,3)))
        offset+=s['durationInFrames']*800
    write(OUT/'voice-verification.json',dict(scenes=rows,events=events,
        sourceNarrationGate=True,completeVisiblePropertyGate=True,pptMediaUsed=False,
        periodiqueCapture='User assigned this remark to N3 SEM3 VDP3; no unrelated video changed'))
    print('Six Soukaina French scenes and four pronunciation units match encoded AAC; source gates pass')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('step',choices=['prepare','timeline','check'])
    p.add_argument('--correct-card-spelling',action='store_true',help='Use only after explicit user approval')
    args=p.parse_args()
    if args.step=='timeline':timeline(args.correct_card_spelling)
    else:dict(prepare=prepare,check=check)[args.step]()
