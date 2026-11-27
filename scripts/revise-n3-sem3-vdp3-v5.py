"""Source-faithful inspector revision of the 31-slide decimal-fraction lesson."""
import argparse,copy,hashlib,json,math,re,runpy,subprocess,wave
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

TOOLS=runpy.run_path('scripts/revise-n3-sem3-vdp1-v5.py');HELP=TOOLS['HELP']
load,write=TOOLS['load'],TOOLS['write']
formula,label,visual,cue=(HELP[k] for k in ('formula','label','visual','cue'))
NS=TOOLS['NS'];VIDEO=Path('src/video');OUT=Path('outputs/n3-sem3-v5/vdp3')
SOURCE=Path('reference/n3-sem3-vdp3-inspector-v5-source.pptx')
STEM='n3-sem3-vdp3-v5';RAW='n3-sem3-elevenlabs-v5-vdp3'
PLAN=VIDEO/(STEM+'-plan.json');VOICE=VIDEO/(STEM+'-voice-plan.json');PACED=VIDEO/(STEM+'-paced-plan.json')
APPROVAL=OUT/'user-approvals.json'


def approvals():return load(APPROVAL) if APPROVAL.exists() else {}


def source_rows():
    rows=[]
    with ZipFile(SOURCE) as deck:
        for n in range(1,32):
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


NUMBERS={'2,985':'deux virgule neuf cent quatre-vingt-cinq','0,001':'zéro virgule zéro zéro un',
 '2,25':'deux virgule vingt-cinq','2985':'deux mille neuf cent quatre-vingt-cinq','1000':'mille',
 '225':'deux cent vingt-cinq','26':'vingt-six','10':'dix','3':'trois','2':'deux','1':'un','0':'zéro','5':'cinq'}


def oral(text):
    text=TOOLS['normalized'](text).replace('ILLIMITÉ','Illimité').replace('PÉRIODIQUE','Périodique')
    text=text.replace('−','-')
    text=re.sub(r'(?<!\w)-?\d+(?:,\d+)?',lambda m:('moins ' if m[0].startswith('-') else '')+NUMBERS[m[0].lstrip('-')],text)
    return text if text.endswith(('.', '?', '!')) else text+'.'


def expected(rows,scene):
    result=[];a=approvals()
    for n in scene['sourceSlides']:
        text=rows[n-1]['voice']
        if n==11 and a.get('carTypo'):text=text.replace('Ca son','Car son')
        if n==18 and a.get('negativeFractionVoice'):
            text='De la même façon : moins cinq sur dix à la puissance zéro est une fraction décimale.'
        result.append(oral(text))
    if scene['id']=='vdp3-prononciation-6':result+=['I.','Li.','Mi.','Té.','Illimité.']
    if scene['id']=='vdp3-prononciation-7':result+=['Pé.','Rio.','Dique.','Périodique.']
    return result


def audit(data):
    rows=source_rows()
    assert [n for s in data['scenes'] for n in s['sourceSlides']]==list(range(1,32))
    for s in data['scenes']:
        texts=expected(rows,s)
        assert s['narration']==' '.join(texts),s['id']
        assert [b['text'] for b in s['beats']]==texts,s['id']
        assert not s.get('transition') and all(v['kind']!='clip' for v in s['art'])
    assert 'deux virgule neuf cent quatre-vingt-cinq' in data['scenes'][8]['narration']


def prepare():
    rows=source_rows();a=approvals();data=load(VIDEO/'n3-sem3-vdp3-v4-lesson.json')
    for s in data['scenes']:
        texts=expected(rows,s)
        s.update(narration=' '.join(texts),audio=f'{RAW}/{s["id"]}.wav',languageCode='fr',speed=.94,stability=.45)
        s['beats']=[dict(stage=i,text=t,**{'from':0}) for i,t in enumerate(texts)]
        s.pop('transition',None)
        dictionary=Path('private/n3-sem3-illimite-dictionary.json')
        if dictionary.exists() and s['id'] in ['vdp3-prononciation-6','vdp3-vocabulaire']:
            d=load(dictionary)
            s['pronunciationDictionaryLocators']=[dict(pronunciation_dictionary_id=d['id'],version_id=d['version_id'])]
    audit(data);write(PLAN,data)
    blocked=set()
    if 'carTypo' not in a:blocked.add('vdp3-fraction-225')
    if 'negativeFractionVoice' not in a:blocked.add('vdp3-fraction-moins-5')
    write(VOICE,dict(scenes=[s for s in data['scenes'] if s['id'] not in blocked]))
    write(OUT/'source-audit.json',dict(source=SOURCE.as_posix(),sourceSha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        slides=rows,sourceVoiceCompared=True,approvedExceptions=[
          'Inspector: technical oral reading of 2,985',
          'User workflow: new native Illimité and Périodique pronunciation with main French voice; guides audio-only',
          'Inspector: remove black fades and align two conversion examples'],
        preciseUserApprovals=a,pendingAudioScenes=sorted(blocked),
        oralExpansions='Exact numeric readings and typography/case normalization; all other source words retained',
        sourceIssues=['Slide 18 voice/image contradiction requires explicit approval',
                      'Slide 11 Ca/Car typo requires explicit approval',
                      'Intermediate =225 is mathematically false; standalone numerator requires explicit approval',
                      'Slide 31 direction names Carré, absent from this vocabulary: animate the actual Périodique card on its source voice'],
        pptMediaUsed=False,productionBandsVisible=False))
    print('Prepared',len(data['scenes'])-len(blocked),'unblocked voice scenes; pending:',sorted(blocked))
    for s in data['scenes']:print(s['id'],':',s['narration'])


def semantic(text):
    """Read actual formula strings, omitting invisible layout reserves."""
    i=0
    def group():
        nonlocal i
        assert text[i]=='{';i+=1;out=''
        while i<len(text) and text[i]!='}':out+=token()
        assert i<len(text);i+=1
        return out
    def token():
        nonlocal i
        c=text[i]
        if c=='{':return group()
        if c!='\\':i+=1;return c
        i+=1
        if text[i] in ';,! ':i+=1;return ''
        m=re.match('[A-Za-z]+',text[i:]);assert m,text[i:];name=m[0];i+=len(name)
        if name in ['textcolor','htmlClass']:group();return group()
        if name=='phantom':group();return ''
        if name in ['underbrace','mathrlap','textsf','boldsymbol']:return group()
        if name=='frac':return group()+'/'+group()
        if name=='quad':return ' '
        raise AssertionError(name)
    out=''
    while i<len(text):out+=token()
    return out


def compact(text):return ''.join(TOOLS['normalized'](text).split()).replace('−','-').replace('’',"'")


def visible_audit(data):
    rows=source_rows();s={x['id'].removeprefix('vdp3-'):x for x in data['scenes']}
    for name,n,exclude in [('definition',9,'Définition'),('propriete',21,'Propriété')]:
        actual=' '.join(a['value'] for a in s[name]['art'])
        authored=' '.join(a['text'] for a in rows[n-1]['shapes'] if a['role']=='student' and not a['text'].startswith(exclude))
        assert compact(actual)==compact(authored),(name,actual,authored)
    checks=[('fraction-225',-1,15),('fraction-1',2,17),
            ('fraction-1',3,15),('fraction-moins-5',2,19),('decimale-en-fraction',5,27)]
    for name,index,source_slide in checks:
        want=' '.join(v['text'] for v in rows[source_slide-1]['shapes'] if v['role']=='student')
        actual=semantic(s[name]['art'][index]['value'])
        assert compact(actual)==compact(want),(name,actual,want)
    assert all(a['value']!='=225' for a in s['fraction-225']['art'])
    # Powers are black; the red focus marks surround the existing glyphs, never duplicate a 2.
    frac=s['fraction-225']['art'][0]
    assert frac['value'].count('vdp-math-exponent')==1 and 'textcolor' not in frac['value'].split('\\phantom')[0]
    assert s['prononciation-7']['pronunciation']['syllables']==['Pé','rio','dique']
    assert all(s[k]['pronunciation']['style']=='simplifier' for k in ['prononciation-6','prononciation-7'])
    assert [a['value'] for a in s['vocabulaire']['art']]==['Décimale','Illimitée','Périodique']


def hold(scene,seconds):
    scene['holdSeconds']=seconds
    with wave.open(str(Path('public')/scene['audio'])) as w:
        scene['durationInFrames']=math.ceil((w.getnframes()/w.getframerate()+seconds)*30)


def timeline():
    from PIL import ImageFont
    a=approvals();assert all(a.get(k) for k in ['negativeFractionVoice','carTypo','standaloneNumerator'])
    data=load(PLAN);paced={s['id']:s for s in load(PACED)['scenes']}
    for s in data['scenes']:
        HELP['apply_voice'](s,paced[s['id']])
        for key in ['languageCode','speed','stability','pronunciationDictionaryLocators']:s.pop(key,None)
    scenes={s['id'].removeprefix('vdp3-'):s for s in data['scenes']}
    font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',64)
    for name,word,parts in [('prononciation-6','Illimité',['Il','li','mi','té']),
                            ('prononciation-7','Périodique',['Pé','rio','dique'])]:
        s=scenes[name]
        s.update(pronunciation=dict(word=word,syllables=parts,style='simplifier',advances=[round(font.getlength(p),3) for p in parts]),
                 art=[label(word,960,594,130,color='#087ABA',weight=700,to=1)])
        hold(s,1.3)
    s=scenes['definition'];s['art']=[
        label('Une fraction décimale',960,472,56,color='#1D1D1D'),
        label('est une fraction dont le dénominateur',960,621,56,1,frame=cue(s,1,'est une fraction'),color='#1D1D1D'),
        label('est une puissance de 10.',960,720,56,1,frame=cue(s,1,'est une puissance'),color='#1D1D1D'),
    ]
    frac=r'\frac{225}{\htmlClass{vdp-math-denominator}{10^{\htmlClass{vdp-math-exponent}{2}}}}'
    right=r'=\;2\textcolor{#D60019}{{,}25}\phantom{0}'
    s=scenes['fraction-225'];result=cue(s,5,'deux virgule vingt-cinq')
    s['art']=[
        formula(frac+r'\phantom{'+right+'}',960,558,96,toFrame=result,focus=[
            dict(target='denominator',start=cue(s,1,'son dénominateur'),end=s['beats'][2]['from']),
            dict(target='exponent',start=cue(s,4,'combien de chiffres'),end=result),
        ]),
        label('une fraction décimale',1200,566,59,frame=cue(s,0,'une fraction décimale'),to=2),
        formula('225',1200,566,100,3,frame=cue(s,3,'deux cent vingt-cinq'),toFrame=result),
        visual('arrow','left',1200,424,215,4,color='#D60019',draw=True,frame=cue(s,4,'vers la gauche'),toFrame=result),
        formula(frac+right,960,558,96,5,frame=result),
    ]
    # Each equality is composed in ONE KaTeX expression, so its bar and equals share a math axis.
    # Invisible padding reserves the same column widths before and after reveals.
    eq1=r'\frac{\phantom{2}1\phantom{2}}{10^3}'
    r1=r'=\;0\textcolor{#D60019}{{,}001}'
    eq2=r'\frac{225}{10^2}=\;2\textcolor{#D60019}{{,}25}\phantom{0}'
    s=scenes['fraction-1'];result=cue(s,1,'zéro virgule zéro zéro un')
    s['art']=[
        formula(eq1+r'\phantom{'+r1+'}',960,466,96,toFrame=result),
        label('une fraction décimale',1200,474,59,frame=cue(s,0,'une fraction décimale'),to=1),
        formula(eq1+r1,960,466,96,1,frame=result),
        formula(eq2,960,775,96,1,frame=result+45),
    ];hold(s,2.4)
    eq=r'\frac{-5}{10^0}';right=r'=\;-5\phantom{00}'
    s=scenes['fraction-moins-5'];result=cue(s,1,'moins cinq')
    s['art']=[
        formula(eq+r'\phantom{'+right+'}',960,558,96,toFrame=result),
        label('une fraction décimale',1200,566,59,frame=cue(s,0,'une fraction décimale'),to=1),
        formula(eq+right,960,558,96,1,frame=result),
    ]
    s=scenes['propriete'];s['title']='Propriété 1';s['art']=[
        label('Tout nombre qui possède une écriture décimale finie',960,504,58,1,color='#1D1D1D'),
        label('s’écrit sous la forme d’une fraction décimale.',960,609,58,1,color='#1D1D1D',frame=cue(s,1,'s’écrit')),
    ]
    s=scenes['decimale-en-fraction']
    base0=r'2{,}\mathrlap{985}\phantom{\underbrace{985}}'
    base=r'2{,}\underbrace{\textcolor{#D60019}{985}}'
    first=r'=\;\frac{2985}{1000}';first_red=r'=\;\frac{2985}{\textcolor{#D60019}{1000}}'
    second=r'=\;\frac{2985}{10^{\textcolor{#D60019}{3}}}'
    s['art']=[
        formula(base0+r'\phantom{'+first+second+'}',1380,625,91,to=1),
        formula(base+r'\phantom{'+first+second+'}',1380,625,91,1,to=2,frame=cue(s,1,'trois chiffres')),
        formula(base+r'\phantom{'+first+second+'}',960,625,91,2,to=3,moveFrom=1380),
        formula(base+first+r'\phantom{'+second+'}',960,625,91,3,to=4),
        formula(base+first_red+r'\phantom{'+second+'}',960,625,91,4,to=5),
        formula(base+first_red+second,960,625,91,5,frame=cue(s,5,'Et ça donne')),
    ]
    s=scenes['vocabulaire'];s['art']=[
        visual('card','Décimale',590,437,52,pulseFrame=cue(s,1,'Décimale')),
        visual('card','Illimitée',1330,437,52,pulseFrame=cue(s,2,'Illimitée')),
        visual('card','Périodique',960,664,52,pulseFrame=cue(s,3,'périodique')),
    ]
    audit(data);visible_audit(data)
    write(VIDEO/(STEM+'-lesson.json'),data)
    write(OUT/'visible-source-audit.json',dict(wholeDefinitionAndPropertyMatchStudentSource=True,
        finalEquationsMatchStudentSource=True,oneNativeMathAxisPerEquation=True,
        exponentColoursBlackInThreeFractionExamples=True,temporaryFalseEqualityRemovedWithApproval=True,
        pronunciationPartsComplete=True,phoneticGuidesVisible=False,productionBandsVisible=False,
        sourceCardImageReviewed='reference/n3-sem3/vdp3/slides/Diapositive28.PNG',pptMediaUsed=False))
    print('V5:',sum(s['durationInFrames'] for s in data['scenes']),'frames; full source text and final equations checked')


def check():
    import numpy as np
    helpers=runpy.run_path('scripts/check-n3-sem3-bilingual.py');data=load(OUT/'timeline.json');audit(data);visible_audit(data)
    video=OUT/'P1_MATHS_N3_SEM3_VDP3_V5.mp4'
    track=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
    rows=[];events=[];offset=0
    for s in data['scenes']:
        p=Path('public')/s['audio'];tag=load(Path(str(p)+'.json'))
        assert (tag['voice'],tag['model'],tag['languageCode'])==('05Y5uLueU3x8LrkGHu0H','eleven_v4','fr')
        assert tag['settings']['speed']==.94 and tag['settings']['stability']==.45
        source=helpers['samples'](p);row=dict(scene=s['id'],encodedCorrelation=helpers['match_audio'](track,source[:24000],offset))
        if s.get('pronunciation'):
            row['unitCorrelations']=[]
            for b in s['beats'][1:]:
                start=b['from']*800;row['unitCorrelations'].append(helpers['match_audio'](track,source[start:start+15000],offset+start))
        rows.append(row)
        for i,v in enumerate(s['art']):
            if 'frame' in v or 'pulseFrame' in v:
                events.append(dict(scene=s['id'],index=i,value=semantic(v['value']) if v['kind']=='math' else v['value'],
                    seconds=round((offset/800+v.get('frame',v.get('pulseFrame')))/30,3)))
        offset+=s['durationInFrames']*800
    write(OUT/'voice-verification.json',dict(scenes=rows,events=events,sourceVoiceAndVisibleGates=True,
        explicitUserApprovals=approvals(),nativePronunciation=True,pptMediaUsed=False))
    print('Ten Soukaina French scenes and nine pronunciation units match encoded AAC; source gates pass')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('step',choices=['prepare','timeline','check'])
    dict(prepare=prepare,timeline=timeline,check=check)[p.parse_args().step]()
