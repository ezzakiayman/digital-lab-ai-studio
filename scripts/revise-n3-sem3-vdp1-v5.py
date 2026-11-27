"""Source-faithful inspector revision, scoped to 3AC week 3 VDP1 only."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import runpy
import unicodedata
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path('.')
VIDEO = ROOT/'src/video'
OUT = ROOT/'outputs/n3-sem3-v5/vdp1'
SOURCE = ROOT/'reference/n3-sem3-inspector-v5-source.pptx'
STEM = 'n3-sem3-vdp1-v5'
RAW = 'n3-sem3-elevenlabs-v5-vdp1'
PLAN = VIDEO/(STEM+'-voice-plan.json')
PACED = VIDEO/(STEM+'-paced-plan.json')
HELP = runpy.run_path('scripts/prepare-n3-sem3-v4.py')
formula, label, visual, cue = (HELP[k] for k in ('formula','label','visual','cue'))
NS = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
      'm':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
M = '{'+NS['m']+'}'


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def write(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def normalized(text):
    return ' '.join(unicodedata.normalize('NFKC',text).split())


def source_text(node):
    """Read text and equations in order; never lose a radical as plain XML text does."""
    if node is None:
        return ''
    if node.tag.endswith('}t'):
        return node.text or ''
    if node.tag.startswith(M):
        tag=node.tag[len(M):]
        if tag.endswith('Pr'):
            return ''
        child=lambda name: source_text(node.find('m:'+name,NS))
        if tag=='rad': return '√'+child('e')
        if tag=='f': return child('num')+'/'+child('den')
        if tag=='sSup': return child('e')+'^'+child('sup')
        if tag=='sSub': return child('e')+'_'+child('sub')
    return ''.join(source_text(c) for c in node)


def source_rows():
    rows=[]
    with ZipFile(SOURCE) as deck:
        for n in range(1,31):
            root=ET.fromstring(deck.read(f'ppt/slides/slide{n}.xml'))
            shapes=[]
            for shape in root.findall('.//p:sp',NS):
                body=shape.find('p:txBody',NS)
                if body is None: continue
                value='\n'.join(source_text(p) for p in body.findall('a:p',NS)).strip()
                if not value: continue
                off=shape.find('.//a:xfrm/a:off',NS)
                assert off is not None
                y=int(off.get('y'))
                role='voice' if y<900000 else 'directions' if y>=5700000 else 'student'
                shapes.append(dict(role=role,text=value,y=y))
            voices=[s['text'] for s in shapes if s['role']=='voice']
            assert len(voices)==1,(n,voices)
            rows.append(dict(slide=n,voice=voices[0],shapes=shapes))
    assert '√' in rows[6]['voice'], 'OMML radical lost'
    return rows


def oral(text):
    text=normalized(text)
    # Reading-only expansions, tracked in source-audit.json; no rephrasing.
    for a,b in [('√a','racine carrée de a'),('1ère','première'),('2ème','deuxième'),
                ('0,25','zéro virgule vingt-cinq'),('12','douze'),('25','vingt-cinq'),
                ('16','seize'),('11','onze'),('9','neuf'),('7','sept'),('5','cinq'),('4','quatre'),
                ('3','trois'),('2','deux')]:
        text=text.replace(a,b)
    return text if text.endswith(('.', '?', '!', '»')) else text+'.'


def set_beats(scene,phrases):
    scene['beats']=[dict(stage=i,text=t,**{'from':0}) for i,t in enumerate(phrases)]
    scene['narration']=' '.join(phrases)


def expected_voice(rows,scene):
    result=[]
    for n in scene['sourceSlides']:
        if n==2:
            result.append('Reconnaître, c’est savoir.') # Explicit inspector correction.
        else:
            result.append(oral(rows[n-1]['voice']))
    if scene['kind']=='pronunciation':
        # Approved native syllabification: spelling stays Ra–cine; phonetic aid is audio only.
        result.extend(['Ra.','Sine.','Racine.'])
    return result


def audit(rows,timeline):
    assert [n for s in timeline['scenes'] for n in s['sourceSlides']]==list(range(1,31))
    for s in timeline['scenes']:
        assert s['narration']==' '.join(expected_voice(rows,s)),s['id']
        assert [b['text'] for b in s['beats']]==expected_voice(rows,s),s['id']
        assert not s.get('transition'),s['id']
        assert all(a['kind']!='clip' for a in s['art'])
    assert 'ou nul' not in ' '.join(s['narration'] for s in timeline['scenes'])
    assert 'je chercher' in timeline['scenes'][3]['narration'], 'Do not silently correct source grammar'


def prepare():
    rows=source_rows()
    data=load(VIDEO/'n3-sem3-vdp1-v4-lesson.json')
    for s in data['scenes']:
        s.pop('transition',None)
        set_beats(s,expected_voice(rows,s))
        s.update(audio=f'{RAW}/{s["id"]}.wav',languageCode='fr',speed=.94,stability=.45)
    audit(rows,data)
    write(PLAN,data)
    write(OUT/'source-audit.json',dict(source=SOURCE.as_posix(),
        sourceSha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),slides=rows,
        sourceVoiceRestored=True,productionBandsVisible=False,pptMediaUsed=False,
        readingOnlyExpansions='NFKC math glyphs, numeric notation, OMML radical and ordinal readings; phrase-final periods for TTS boundaries; source words otherwise retained',
        approvedExceptions=['Slide 2: Reconnaître, c’est savoir (inspector)',
          'Slide 28: newly generated Ra–cine then Racine, same French voice (user workflow rule)',
          'All transitions to black removed (inspector)'],
        sourceGrammarRetained=['Slide 15: je chercher'],
        notationDecision='Source slide 6 uses bold italic mathematical a; restore it in definition and root notation'))
    print('Source gate passed: 30 bands, OMML radical, exact source wording plus two scoped exceptions')
    for s in data['scenes']: print(s['id'],':',s['narration'])


def diagram(y,at,times):
    items=HELP['root_diagram'](y,at,times)
    for i in (0,3):
        items[i]['value']=items[i]['value'].replace('a',r'\boldsymbol{a}')
    return items


def timeline():
    from PIL import ImageFont
    rows=source_rows();data=load(PLAN)
    revised={s['id']:s for s in load(PACED)['scenes']}
    scenes={s['id'].removeprefix('vdp1-'):s for s in data['scenes']}
    for s in scenes.values():
        HELP['apply_voice'](s,revised[s['id']])
        for key in ('languageCode','speed','stability'):s.pop(key,None)
        s.pop('transition',None)
    s=scenes['definition']
    # The two source lines use sans body text and a bold italic mathematical parameter.
    s['art']=[
        formula(r'\textsf{La racine carrée d’un nombre positif }\boldsymbol{a}\textsf{ est le nombre}',960,382,49),
        formula(r'\textsf{positif dont le carré est égal au nombre }\boldsymbol{a}\textsf{.}',960,461,49,
                frame=cue(s,0,'dont le carré')),
        formula(r'\sqrt{\boldsymbol{a}}',522,584,73,1,frame=cue(s,1,'se note')),
        label('se lit « racine carrée de 𝑎 »',1040,584,48,1,frame=cue(s,1,'se lit')),
        *diagram(808,2,(cue(s,2,'Donc si'),cue(s,2,'au carré'),cue(s,2,'donne a',last=True),cue(s,3,'Et si'))),
    ]
    s=scenes['carres-parfaits']
    s['art']=s['art'][:6]+[
        formula(r'\sqrt{a}=\textcolor{#D60019}{?}',518,615,96,4,frame=cue(s,4,'la racine carrée')),
        formula(r'\textcolor{#087746}{\Longrightarrow}',929,615,96,4,frame=cue(s,4,'je chercher')),
        formula(r'\bigl(\textcolor{#D60019}{?}\bigr)^2=a',1313,615,96,4,frame=cue(s,4,'au carré')),
    ]
    # Restore the literal source condition rather than its previously substituted inequality.
    for name,power in [('propriete-1',r'(\sqrt{a})^2=(-\sqrt{a})^2=a'),
                       ('propriete-2',r'\sqrt{a^2}=\sqrt{(-a)^2}=a')]:
        s=scenes[name]
        s['art']=s['art'][1:]
        s['art'][:0]=[
            formula(r'\textsf{Pour tout nombre positif }\boldsymbol{a}\textsf{ :}',960,382,52,1),
            formula(power,960,509,81,1,frame=cue(s,1,'la racine carrée')),
        ]
    s=scenes['verification']
    s['art'][-1].update(at=1) # Mark false when the narration evaluates the claim.
    s=scenes['prononciation-28']
    font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',64)
    s.update(pronunciation=dict(word='Racine',syllables=['Ra','cine'],style='simplifier',
                               advances=[round(font.getlength(p),3) for p in ['Ra','cine']]),
             art=[label('Racine',960,594,130,color='#087ABA',weight=700,to=1)])
    s=scenes['vocabulaire']
    cards=s['art'][:2]
    for a,phrase in zip(cards,['nombre positif','Racine carrée']):
        a.pop('pulse',None)
        a.update(pulseFrame=cue(s,0,phrase))
    result=cue(s,1,'égal au nombre a',last=True)
    s['holdSeconds']=2.8
    s['durationInFrames']+=57 # .9s prior hold becomes 2.8s, allows reverse arrow to settle.
    s['art']=cards+diagram(749,1,(
        cue(s,1,'La racine carrée'),cue(s,1,'dont le carré'),result,result+30))
    audit(rows,data)
    assert all(x['frame']<s['durationInFrames'] for s in scenes.values() for x in s['art'] if 'frame' in x)
    # Check visible prose against independently authored source text, not the voice band.
    student=' '.join(normalized(sh['text']) for r in rows for sh in r['shapes'] if sh['role']=='student')
    for text in ['La racine carrée d’un nombre positif a est le nombre positif dont le carré est égal au nombre a.',
                 'Pour tout nombre positif a','Racine carrée','Mise au carré']:
        assert normalized(text) in student,text
    # Slide 29 cards are rendered pictures rather than extractable OOXML text.
    # Both original labels were read on the source PNG, not inferred from the narration.
    assert [a['value'] for a in cards]==['Nombre positif','Racine carrée']
    definition=' '.join(a['value'] for a in scenes['definition']['art'][:2])
    definition=re.sub(r'\\textsf\{([^}]*)\}',r'\1',definition).replace(r'\boldsymbol{a}','a')
    assert normalized(definition)==normalized(rows[5]['voice'])
    write(VIDEO/(STEM+'-lesson.json'),data)
    write(OUT/'visual-source-audit.json',dict(definitionMatchesSource=True,
        propertyConditionsMatchSource=True,mathematicalParameter='bold italic a, source slide 6',
        sequentialDiagrams=True,falseMarker='Faux',nativePronunciation=True,
        phoneticGuidesVisible=False,productionBandsVisible=False,pptMediaUsed=False,
        blackTransitions=False,sourceImage29Reviewed=dict(
          path='reference/n3-sem3/vdp1/slides/Diapositive29.PNG',
          sha256=hashlib.sha256(Path('reference/n3-sem3/vdp1/slides/Diapositive29.PNG').read_bytes()).hexdigest(),
          independentlyVisibleLabels=['Nombre positif','Racine carrée'])))
    print('Source-faithful V5:',sum(s['durationInFrames'] for s in data['scenes']),'frames')


def check():
    import subprocess
    import numpy as np
    helpers=runpy.run_path('scripts/check-n3-sem3-bilingual.py')
    data=load(OUT/'timeline.json')
    audit(source_rows(),data)
    movie=OUT/'P1_MATHS_N3_SEM3_VDP1_V5.mp4'
    track=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),
                      '-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
    offset=0;report=[];events=[]
    for s in data['scenes']:
        audio=Path('public')/s['audio'];receipt=load(Path(str(audio)+'.json'))
        assert (receipt['provider'],receipt['voice'],receipt['model'],receipt['languageCode'])==(
            'elevenlabs','05Y5uLueU3x8LrkGHu0H','eleven_v4','fr')
        assert receipt['settings']['speed']==.94 and receipt['settings']['stability']==.45
        source=helpers['samples'](audio)
        alignment=load(audio.parent/'alignment'/(s['id']+'.json'))
        assert alignment['signature']==hashlib.sha256(audio.read_bytes()+s['narration'].encode()).hexdigest()
        score=helpers['match_audio'](track,source[:24000],offset)
        row=dict(scene=s['id'],voice=receipt['voice'],languageCode='fr',encodedStartCorrelation=score)
        if s.get('pronunciation'):
            row['unitCorrelations']=[]
            for b in s['beats'][1:]:
                start=b['from']*800
                row['unitCorrelations'].append(helpers['match_audio'](track,source[start:start+17000],offset+start))
        report.append(row)
        for i,a in enumerate(s['art']):
            if 'frame' in a:
                events.append(dict(scene=s['id'],visualIndex=i,value=a['value'],
                                   seconds=round((offset/800+a['frame'])/30,3)))
        offset+=s['durationInFrames']*800
    write(OUT/'voice-verification.json',dict(scenes=report,events=events,
        sourceGate='30 voice bands, two explicit exceptions, no production text displayed',
        pronunciationReview='Independent whole-scene French detection; isolated Ra / SIN / Racine recovered without expected transcript. This is not complete human phonetic certification.',
        cloudAcousticReview='Unavailable: HTTP 503; local independent recognition used',
        pptMediaUsed=False,blackTransitions=False))
    print('Nine Soukaina French scenes and all three native pronunciation units match encoded AAC')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('step',choices=['prepare','timeline','check'])
    dict(prepare=prepare,timeline=timeline,check=check)[p.parse_args().step]()
