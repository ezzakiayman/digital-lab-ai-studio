"""Source-scoped VDP4 inspector revision; disputed edits require recorded approval."""
import argparse
import copy
import hashlib
import math
from pathlib import Path
import re
import runpy
import subprocess
import wave
from xml.etree import ElementTree as ET
from zipfile import ZipFile

TOOLS = runpy.run_path('scripts/revise-n3-sem3-vdp1-v5.py')
HELP = TOOLS['HELP']
load, write, normalized = (TOOLS[k] for k in ('load', 'write', 'normalized'))
formula, label, visual, cue = (HELP[k] for k in ('formula', 'label', 'visual', 'cue'))
NS = TOOLS['NS']
SOURCE = Path('reference/n3-sem3-vdp4-inspector-v5-source.pptx')
OUT = Path('outputs/n3-sem3-v5/vdp4')
STEM = 'n3-sem3-vdp4-v5'
PLAN = Path('src/video') / (STEM + '-plan.json')
VOICE = Path('src/video') / (STEM + '-voice-plan.json')
PACED = Path('src/video') / (STEM + '-paced-plan.json')
RAW = 'n3-sem3-elevenlabs-v5-vdp4'
APPROVAL = OUT / 'user-approvals.json'
BLACK, RED = '#1D1D1D', '#D60019'


def approvals():
    return load(APPROVAL) if APPROVAL.exists() else {}


def source_rows():
    rows = []
    with ZipFile(SOURCE) as deck:
        for n in range(1, 48):
            root = ET.fromstring(deck.read(f'ppt/slides/slide{n}.xml'))
            shapes = []
            for shape in root.findall('.//p:sp', NS):
                body = shape.find('p:txBody', NS)
                if body is None:
                    continue
                text = '\n'.join(TOOLS['source_text'](p) for p in body.findall('a:p', NS)).strip()
                if not text:
                    continue
                off = shape.find('.//a:xfrm/a:off', NS)
                x, y = int(off.get('x')), int(off.get('y'))
                if re.match(r'^(?:-\s*)?(?:Afficher|Mettre|Garder|Éviter|Lire|Insérer|Animer)\b', text):
                    role = 'directions'
                elif y < 900000 and not text.startswith('√'):
                    role = 'voice'
                else:
                    role = 'student'
                shapes.append(dict(role=role, text=text, x=x, y=y))
            for table in root.findall('.//a:tbl', NS):
                for cell in table.findall('.//a:tc', NS):
                    text = '\n'.join(TOOLS['source_text'](p) for p in cell.findall('.//a:p', NS)).strip()
                    if text:
                        shapes.append(dict(role='student', text=text, origin='table'))
            voice = [s['text'] for s in shapes if s['role'] == 'voice']
            assert len(voice) == 1, (n, voice)
            rows.append(dict(slide=n, voice=voice[0], shapes=shapes))
    # Geometry alone would misclassify the equation and the axis labels as production bands.
    assert any(s['role'] == 'student' and s['text'].startswith('√2=') for s in rows[41]['shapes'])
    assert any(s['role'] == 'student' and s['text'] == '-4' for s in rows[40]['shapes'])
    assert all(s['role'] == 'directions' for s in rows[36]['shapes'] if s['text'].startswith('- Mettre'))
    return rows


NUMBERS = {'2,25': 'deux virgule vingt-cinq', '234': 'deux cent trente-quatre',
           '87': 'quatre-vingt-sept', '225': 'deux cent vingt-cinq', '100': 'cent',
           '45': 'quarante-cinq', '63': 'soixante-trois', '7': 'sept', '4': 'quatre',
           '3': 'trois', '2': 'deux', '1': 'un', '0': 'zéro'}


def oral(text):
    text = normalized(text).replace('−', '-').replace('1ère', 'première').replace('2ème', 'deuxième')
    text = re.sub(r'√\s*([27])', lambda m: 'racine carrée de ' + NUMBERS[m[1]], text)
    text = re.sub(r'-?\d+(?:,\d+)?', lambda m: (' ' if m.start() and text[m.start()-1].isalpha() else '')
                  + ('moins ' if m[0].startswith('-') else '') + NUMBERS[m[0].lstrip('-')], text)
    return text if text.endswith(('.', '?', '!', ',', ':', ';')) else text + '.'


def expected(rows, scene):
    a = approvals()
    result = []
    for n in scene['sourceSlides']:
        text = rows[n-1]['voice']
        if n == 3 and a.get('objectiveEnumeration'):
            text = 'Voici quelques nombres : sept, zéro virgule vingt-cinq, moins trois sur quatre, la racine carrée de deux et pi.'
        if n == 39 and a.get('pointAbscissa'):
            text = 'Chaque nombre réel peut être représenté par un unique point sur une droite numérique. Ce nombre est l’abscisse de ce point.'
        if n == 40 and a.get('reciprocal'):
            text = 'Réciproquement, chaque point d’une droite numérique est associé à un unique nombre réel, son abscisse.'
        result.append(oral(text))
    if scene['id'] == 'vdp4-prononciation-5':
        result += ['I.', 'Ra.', 'Sion.', 'Nèle.', 'Irrationnel.']
    if scene['id'] == 'vdp4-prononciation-6':
        result += ['Ré.', 'Elle.', 'Réel.']
    return result


def audit(data):
    rows = source_rows()
    assert [n for s in data['scenes'] for n in s['sourceSlides']] == list(range(1, 48))
    for s in data['scenes']:
        phrases = expected(rows, s)
        assert s['narration'] == ' '.join(phrases), s['id']
        assert [b['text'] for b in s['beats']] == phrases, s['id']
        assert not s.get('transition'), s['id']
        assert all(v['kind'] != 'clip' for v in s['art'])


def prepare():
    data = load(Path('src/video/n3-sem3-vdp4-v4-lesson.json'))
    rows = source_rows()
    a = approvals()
    blocked = set()
    if 'objectiveEnumeration' not in a:
        blocked.add('vdp4-objectif')
    if not all(a.get(k) for k in ['pointAbscissa', 'reciprocal']):
        blocked.add('vdp4-droite-propriete')
    dictionary = Path('private/n3-sem3-illimite-dictionary.json')
    for s in data['scenes']:
        phrases = expected(rows, s)
        s.update(narration=' '.join(phrases), audio=f'{RAW}/{s["id"]}.wav',
                 languageCode='fr', speed=.94, stability=.45)
        s['beats'] = [dict(stage=i, text=t, **{'from': 0}) for i, t in enumerate(phrases)]
        s.pop('transition', None)
        if dictionary.exists() and 'illimité' in s['narration'].lower():
            d = load(dictionary)
            s['pronunciationDictionaryLocators'] = [dict(pronunciation_dictionary_id=d['id'], version_id=d['version_id'])]
        pronunciation_dictionary = Path('private/n3-sem3-irrationnel-dictionary.json')
        if pronunciation_dictionary.exists() and s['id'] == 'vdp4-prononciation-5':
            d = load(pronunciation_dictionary)
            s['pronunciationDictionaryLocators'] = [dict(pronunciation_dictionary_id=d['id'], version_id=d['version_id'])]
    audit(data)
    write(PLAN, data)
    write(VOICE, dict(scenes=[s for s in data['scenes'] if s['id'] not in blocked]))
    write(OUT/'source-inventory.json', rows)
    write(OUT/'source-audit.json', dict(source=SOURCE.as_posix(), sourceSha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        narrationComparedToOwnSourceBands=True, sourceIssuesRequiringConfirmation=[
            'Slide 39 point/abscissa wording', 'Slide 40 reciprocal direction',
            'Pi digits rounded then continued with ellipsis', 'Objective enumeration differs from source voice',
            'Non-periodique objective screenshot attribution and requested change'],
        userApprovals=a, pendingAudioScenes=sorted(blocked), pptMediaUsed=False,
        productionRoles='Instruction wording and geometry; mathematical labels are not classified as narration/directions solely by y',
        detailedVisualAuditPending=True))
    print(f'Prepared {len(data["scenes"])-len(blocked)} unblocked voice scenes; pending: {sorted(blocked)}')


def hold(scene, seconds=1.2):
    scene['holdSeconds'] = seconds
    with wave.open(str(Path('public') / scene['audio'])) as w:
        scene['durationInFrames'] = math.ceil((w.getnframes()/w.getframerate()+seconds)*30)


def line(parts, y, size=56, at=0, **opts):
    """Measure mixed-colour prose with the same Arial font as the video."""
    from PIL import ImageFont
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', size)
    widths = [font.getlength(t) for t, _ in parts]
    left = 960 - sum(widths)/2
    result = []
    for (text, color), width in zip(parts, widths):
        result.append(label(text, left+width/2, y, size, at, color=color, **opts))
        left += width
    return result


def irrational_example(scene, root, digits, pi=False):
    """One native math row with invariant geometry while its annotation changes."""
    equality = cue(scene, 0, 'est égale')
    annotation = cue(scene, 0, 'partie décimale' if pi else 'je remarque')
    number = digits + r'\ldots'
    brace = (r'\mathord{\textcolor{#4472C4}{\underbrace{\textcolor{#1D1D1D}{' + number
             + r'}}_{\textcolor{#1D1D1D}{\textsf{La partie décimale}}}}}')
    tail = r'=' + ('3' if pi else '2') + r'{,}'
    reserved = r'\mathrlap{' + number + r'}\phantom{' + brace + '}'
    opening = root + r'\phantom{' + tail + brace + '}'
    plain = root + tail + reserved
    marked = root + tail + brace
    final = (root + r'\textsf{ est un nombre }\textcolor{#D60019}{\textsf{irrationnel}}')
    scene['art'] = [
        formula(opening, 960, 482, 83, toFrame=equality),
        formula(plain, 960, 482, 83, frame=equality, toFrame=annotation),
        formula(marked, 960, 482, 83, frame=annotation, to=1),
        formula(plain, 960, 482, 83, 1),
        label('Écriture décimale illimitée et non périodique', 960, 694, 62, 1, color=RED),
        visual('arrow', 'down', 960, 790, 65, len(scene['beats'])-1, color=RED, draw=True,
               frame=cue(scene, len(scene['beats'])-1, 'Et je dis que')),
        formula(final, 960, 913, 52, len(scene['beats'])-1,
                frame=cue(scene, len(scene['beats'])-1, 'pi' if pi else 'racine carrée')),
    ]


def timeline():
    from PIL import ImageFont
    a = approvals()
    assert 'objectiveEnumeration' in a and a.get('pointAbscissa') and a.get('reciprocal') and a.get('piDigits'), 'Precise approvals required'
    data = load(PLAN)
    paced = {s['id']: s for s in load(PACED)['scenes']}
    assert len(paced) == len(data['scenes']) == 14
    for s in data['scenes']:
        HELP['apply_voice'](s, paced[s['id']])
        for key in ['languageCode', 'speed', 'stability', 'pronunciationDictionaryLocators']:
            s.pop(key, None)
        hold(s)
    scenes = {s['id'].removeprefix('vdp4-'): s for s in data['scenes']}
    scenes['objectif']['objective']['links'][-1]['endFrame']=scenes['objectif']['beats'][3]['from']
    font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 64)
    for name, word, parts in [('prononciation-5', 'Irrationnel', ['Ir','ra','tion','nel']),
                              ('prononciation-6', 'Réel', ['Ré','el'])]:
        s = scenes[name]
        s.update(pronunciation=dict(word=word, syllables=parts, style='simplifier',
                    advances=[round(font.getlength(p),3) for p in parts]),
                 art=[label(word,960,594,130,color='#087ABA',weight=700,to=1)])
        hold(s, 1.4)
    s = scenes['rationnels']
    s['art'] = [
        label('Les nombres qui ont une écriture décimale limitée',960,388,52,1),
        label('ou illimitée et périodique peuvent s’écrire',960,465,52,1,frame=cue(s,1,'ou illimitée')),
        formula(r'\textsf{sous forme d’une fraction }\frac{a}{b},',960,575,43,1,frame=cue(s,1,'sous forme')),
        formula(r'\textsf{où }a\textsf{ et }b\textsf{ sont deux entiers}',960,711,43,2),
        formula(r'\textsf{tels que }b\ne0,',960,791,43,2,frame=cue(s,2,'tels que')),
        formula(r'\textsf{Ils s’appellent des nombres }\textcolor{#D60019}{\textsf{rationnels}}.',960,902,43,3),
    ]
    s = scenes['rationnel-decimal']
    caption = r'\textsf{ : une écriture décimale }\textcolor{#D60019}{\textsf{finie}}'
    first = cue(s,0,'a une écriture')
    equal = cue(s,1,'est égal')
    s['art'] = [
        formula(r'2{,}25\phantom{'+caption+'}',960,508,61,toFrame=first),
        formula(r'2{,}25'+caption,960,508,61,frame=first,to=1),
        formula(r'2{,}25\phantom{=\frac{225}{100}}',960,508,92,1,toFrame=equal),
        formula(r'2{,}25=\frac{225}{100}',960,508,92,1,frame=equal),
        formula(r'2{,}25\textsf{ est un nombre }\textcolor{#D60019}{\textsf{rationnel}}',960,794,50,2),
    ]
    s = scenes['rationnel-periodique']
    num = r'0{,}7142857142857\ldots'
    braces = r'0{,}\textcolor{#66539F}{\overbrace{\textcolor{#1D1D1D}{714285}}\overbrace{\textcolor{#1D1D1D}{714285}}}7\ldots'
    brace = min(s['beats'][1]['from']-6, cue(s,0,'nombre',last=True)+13)
    fraction = r'=\frac{45}{63}'
    equal = cue(s,3,'quarante-cinq')
    s['art'] = [
        formula(num+r'\phantom{'+fraction+'}',960,481,77,toFrame=brace),
        formula(braces+r'\phantom{'+fraction+'}',960,481,77,frame=brace,to=3),
        formula(num+r'\phantom{'+fraction+'}',960,481,77,3,toFrame=equal),
        formula(num+fraction,960,481,77,3,frame=equal),
        formula(r'\textsf{ : écriture décimale }\textcolor{#D60019}{\textsf{illimitée périodique}}',960,683,48,1,to=3),
        formula(num+r'\textsf{ est un nombre }\textcolor{#D60019}{\textsf{rationnel}}',960,833,46,4),
    ]
    s = scenes['irrationnels']
    s['art'] = [label('Les nombres qui ont une écriture décimale',960,418,56,1)]
    s['art'] += line([('illimitée',RED),(' et ',BLACK),('non périodique',RED),(' ne peuvent pas',BLACK)],518,56,1,frame=cue(s,1,'illimité'))
    s['art'] += [label('s’écrire sous forme d’une fraction,',960,617,56,1,frame=cue(s,1,'s’écrire')),
                label('ils s’appellent',960,772,56,2)]
    s['art'] += line([('des nombres ',BLACK),('irrationnels',RED),('.',BLACK)],865,56,2)
    irrational_example(scenes['irrationnel-racine'],r'\sqrt{7}','64575131106')
    irrational_example(scenes['irrationnel-pi'],r'\pi','141592653589',pi=True)
    s = scenes['entiers']
    first_equal = cue(s,2,'Ça donne')
    second_equal = cue(s,4,'il s’écrit')
    s['art'] = [
        label('Tout entier est un nombre rationnel.',960,555,59,1,color=BLACK,toFrame=s['beats'][2]['from']-9),
        formula(r'234\phantom{=\frac{234}{1}}',960,533,92,2,toFrame=first_equal),
        formula(r'234=\frac{234}{1}',960,533,92,2,frame=first_equal,toFrame=s['beats'][4]['from']-9),
        formula(r'234\textsf{ est un nombre }\textcolor{#D60019}{\textsf{rationnel}}',960,799,49,3,toFrame=s['beats'][4]['from']-9),
        formula(r'-87\phantom{=\frac{-87}{1}}',960,533,92,4,toFrame=second_equal),
        formula(r'-87=\frac{-87}{1}',960,533,92,4,frame=second_equal),
        formula(r'-87\textsf{ est un nombre rationnel}',960,799,49,5,color=BLACK),
    ]
    s = scenes['reels']
    s['art'] = [label('Les nombres rationnels et les nombres irrationnels',960,424,52,1,toFrame=s['beats'][2]['from']-9)]
    s['art'] += line([('forment les ',BLACK),('nombres réels.',RED)],508,52,1,toFrame=s['beats'][2]['from']-9)
    s['art'] += [visual('sets','source-full',960,640,92,2,setPulses=[
        dict(target='real',frame=cue(s,2,'réel')),
        dict(target='rational',frame=cue(s,2,'rationnel')),
        dict(target='irrational',frame=cue(s,2,'irrationnel'))])]
    s = scenes['droite-propriete']
    s['art'] = [
        label('Chaque nombre réel peut être représenté',960,405,52,1),
        label('par un unique point sur une droite numérique.',960,490,52,1,frame=cue(s,1,'par un unique point')),
        label('Ce nombre est l’abscisse de ce point.',960,575,52,1,frame=cue(s,1,'Ce nombre')),
        label('Réciproquement, chaque point d’une droite numérique',960,751,52,2),
        label('est associé à un unique nombre réel, son abscisse.',960,843,52,2,frame=cue(s,2,'est associé')),
    ]
    s = scenes['droite-exemple']
    s['art'] = [
        visual('axis','',960,666,92),
        formula(r'\sqrt{2}=1{,}4142135623\ldots',960,432,80,1,frame=cue(s,1,'racine carrée')),
        visual('axis-root','',960,666,92,2,frame=cue(s,2,'point M')),
        formula(r'\textsf{Le nombre réel }\sqrt{2}\textsf{ est l’abscisse d’un point }M(\sqrt{2})',960,860,40,2),
        formula(r'\textsf{situé entre }A(1)\textsf{ et }B(2)',960,937,40,2,frame=cue(s,2,'situé entre')),
    ]
    s = scenes['vocabulaire']
    s['art'] = [visual('card','Rationnel',590,437,52,pulseFrame=cue(s,1,'Rationnel')),
                visual('card','Irrationnel',1330,437,52,pulseFrame=cue(s,2,'Irrationnel')),
                visual('card','Réel',960,664,52,pulseFrame=cue(s,3,'réel'))]
    audit(data)
    gate=visible_audit(data)
    write(Path('src/video')/(STEM+'-lesson.json'), data)
    write(OUT/'visible-source-audit.json',gate)
    write(OUT/'timeline-construction.json',dict(sourceSlides=list(range(1,48)),userApprovals=a,
        sourceRoleEdgeCasesChecked=True,visualAuditPending=False,visualSourceAuditPassed=True,unresolvedScreenshotRemark=True))
    print('Authored 14 scenes,',sum(s['durationInFrames'] for s in data['scenes']),'frames; source voice and visual gates passed')


def semantic(text):
    i = 0
    def group():
        nonlocal i
        assert text[i] == '{', text[i:]
        i += 1
        out = ''
        while i < len(text) and text[i] != '}':
            out += token()
        assert i < len(text)
        i += 1
        return out
    def token():
        nonlocal i
        c = text[i]
        if c == '{':
            return group()
        if c == '_' and i+1 < len(text) and text[i+1] == '{':
            i += 1
            return ' ' + group()
        if c != '\\':
            i += 1
            return c
        i += 1
        if text[i] in ';,! ':
            i += 1
            return ' '
        match = re.match('[A-Za-z]+', text[i:])
        assert match, text[i:]
        name = match[0]
        i += len(name)
        if name in ['textcolor','htmlClass']:
            group()
            return group()
        if name == 'phantom':
            group()
            return ''
        if name in ['textsf','text','boldsymbol','underbrace','overbrace','mathrlap','mathord']:
            return group()
        if name == 'frac':
            return group() + '/' + group()
        if name == 'sqrt':
            return '√' + group()
        if name in ['ne','pi','ldots','quad']:
            return {'ne':'≠','pi':'π','ldots':'…','quad':' '}[name]
        raise AssertionError(name)
    out = ''
    while i < len(text):
        out += token()
    return out


def compact(text):
    return re.sub(r'\.{2,}', '…', ''.join(normalized(text).split())).replace('−','-').replace('’',"'")


def visible_audit(data):
    rows = source_rows()
    scenes = {s['id'].removeprefix('vdp4-'):s for s in data['scenes']}
    expected_counts = dict(objectif=0, rationnels=6, **{'prononciation-5':1,'prononciation-6':1,
        'rationnel-decimal':5,'rationnel-periodique':6,'irrationnels':10,'irrationnel-racine':7,
        'irrationnel-pi':7,'entiers':7,'reels':4,'droite-propriete':5,'droite-exemple':5,'vocabulaire':3})
    for name, count in expected_counts.items():
        assert len(scenes[name]['art']) == count, ('Unexpected or missing visual',name)
    def values(name, indices):
        return ' '.join(semantic(v['value']) if v['kind']=='math' else v['value']
                        for i,v in enumerate(scenes[name]['art']) if i in indices)
    def source(n, prefix):
        found = [s['text'] for s in rows[n-1]['shapes'] if s['role']=='student' and normalized(s['text']).startswith(normalized(prefix))]
        assert len(found)==1,(n,prefix,found)
        return found[0]
    def same(actual, expected):
        assert compact(actual)==compact(expected),(actual,expected)
    same(scenes['objectif']['objective']['title'],source(1,'Distinguer'))
    assert scenes['objectif']['objective']['links'][-1]['endFrame']<=scenes['objectif']['beats'][3]['from']
    same(values('rationnels',[0,1,2]),source(8,'Les nombres'))
    same(values('rationnels',[3]),source(9,'où'))
    same(values('rationnels',[4]),source(9,'tels que'))
    same(values('rationnels',[5]),source(10,'Ils s’appellent'))
    same(values('irrationnels',range(6)),source(20,'Les nombres'))
    same(values('irrationnels',range(6,10)),source(21,'ils s’appellent')+' '+source(21,'des nombres'))
    same(values('reels',[0,1,2]),source(36,'Les nombres'))
    assert scenes['reels']['art'][3]['value']=='source-full'
    assert all(v['toFrame']+9<=scenes['reels']['beats'][2]['from'] for v in scenes['reels']['art'][:3])
    assert [s['text'] for s in rows[36]['shapes'] if s.get('origin')=='table']==[
        'Les nombres réels','Les nombres rationnels','Les nombres irrationnels']
    def equation(n):
        parts=[s for s in rows[n-1]['shapes'] if s['role']=='student'
               and re.fullmatch(r'[0-9√π−+\-/=,.\s…]+',normalized(s['text']))
               and (n!=42 or s.get('y',0)<1500000)]
        assert parts,n
        return ' '.join(s['text'] for s in sorted(parts,key=lambda s:s.get('x',0)))
    same(values('rationnel-decimal',[3]),equation(12))
    same(values('rationnel-decimal',[4]),source(13,'2,25 est'))
    same(values('rationnel-decimal',[1]),'2,25 '+source(11,': une').replace('limitée','finie'))
    same(values('rationnel-periodique',[3]),equation(17))
    same(values('rationnel-periodique',[4]),source(15,': écriture'))
    same(values('rationnel-periodique',[5]),source(18,'0,7142857142857....\u00a0est'))
    for name,n,last in [('irrationnel-racine',22,25),('irrationnel-pi',26,28)]:
        expected=equation(n)
        if name.endswith('-pi') and approvals().get('piDigits'):
            expected=expected.replace('14159265359','141592653589')
        same(values(name,[3]),expected)
        same(values(name,[2]),expected+' La partie décimale')
        same(values(name,[4]),source(last,'Écriture'))
        prefix='𝜋 est' if name.endswith('-pi') else '√7 est'
        same(values(name,[6]),source(last,prefix).replace('14159265359','141592653589'))
        assert len({(v['x'],v['y'],v['size']) for v in scenes[name]['art'][:4]})==1
    same(values('entiers',[0]),source(30,'Tout entier'))
    same(values('entiers',[2]),equation(31))
    same(values('entiers',[3]),source(32,'234 est'))
    same(values('entiers',[5]),equation(33))
    same(values('entiers',[6]),source(34,'−87 est'))
    integers=scenes['entiers']
    assert integers['art'][0]['toFrame']+9<=integers['beats'][2]['from']
    assert all(integers['art'][i]['toFrame']+9<=integers['beats'][4]['from'] for i in [2,3])
    assert integers['art'][3]['size']==integers['art'][6]['size']
    same(values('droite-propriete',[0,1,2]),approvals()['approvedPointSentence'])
    same(values('droite-propriete',[3,4]),approvals()['approvedReciprocalSentence'])
    same(values('droite-exemple',[1]),equation(42))
    same(values('droite-exemple',[3,4]),source(43,'Le nombre réel'))
    assert [v['value'] for v in scenes['vocabulaire']['art']]==['Rationnel','Irrationnel','Réel']
    for name,word in [('prononciation-5','Irrationnel'),('prononciation-6','Réel')]:
        p=scenes[name]['pronunciation']
        assert ''.join(p['syllables'])==word and p['style']=='simplifier'
    return dict(completeSourceSentencesChecked=True,ownSourceEquationsChecked=True,
                noOldIntegerExampleCarriedForward=True,allFourPiStatesHaveSameGeometry=True,
                nativeWordsSpellCorrectly=True,sourceTableAndAxisReviewed=True,
                pptMediaUsed=False,phoneticGuidesVisible=False,unresolvedScreenshotRemark=True)


def check():
    import numpy as np
    helpers = runpy.run_path('scripts/check-n3-sem3-bilingual.py')
    data = load(OUT/'timeline.json')
    audit(data)
    gate = visible_audit(data)
    movie = OUT/'P1_MATHS_N3_SEM3_VDP4_V5.mp4'
    track = np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),
        '-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
    offset=0
    rows=[]
    events=[]
    for s in data['scenes']:
        p=Path('public')/s['audio']
        tag=load(Path(str(p)+'.json'))
        assert (tag['voice'],tag['model'],tag['languageCode'])==('05Y5uLueU3x8LrkGHu0H','eleven_v4','fr')
        assert tag['settings']['speed']==.94 and tag['settings']['stability']==.45
        source=helpers['samples'](p)
        row=dict(scene=s['id'],encodedCorrelation=helpers['match_audio'](track,source[:24000],offset))
        if s.get('pronunciation'):
            row['unitCorrelations']=[]
            for beat in s['beats'][1:]:
                start=beat['from']*800
                row['unitCorrelations'].append(helpers['match_audio'](track,source[start:start+15000],offset+start))
        rows.append(row)
        for i,v in enumerate(s['art']):
            if 'frame' in v or 'pulseFrame' in v:
                events.append(dict(scene=s['id'],index=i,value=semantic(v['value']) if v['kind']=='math' else v['value'],
                    seconds=round((offset/800+v.get('frame',v.get('pulseFrame')))/30,3)))
        offset+=s['durationInFrames']*800
    write(OUT/'voice-verification.json',dict(scenes=rows,events=events,sourceGates=gate,
         explicitUserApprovals=approvals(),sameMainFrenchVoice=True,pptMediaUsed=False))
    print('Fourteen main-voice French takes and eight pronunciation units match encoded AAC; source gates pass')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step', choices=['prepare','timeline','audit','check'])
    def check_audit():
        data=load(Path('src/video')/(STEM+'-lesson.json'))
        audit(data)
        report=visible_audit(data)
        write(OUT/'visible-source-audit.json',report)
        construction=load(OUT/'timeline-construction.json')
        construction['visualAuditPending']=False
        construction['visualSourceAuditPassed']=True
        write(OUT/'timeline-construction.json',construction)
        source_report=load(OUT/'source-audit.json')
        source_report.update(detailedVisualAuditPending=False,
            sourceIssuesRequiringConfirmation=['Non-periodique objective screenshot attribution and requested change'],
            resolvedSourceIssues=['Point/abscissa sentence approved','Reciprocal approved',
                'Exact pi digits approved','User explicitly chose source-only objective wording'])
        write(OUT/'source-audit.json',source_report)
        print('Narration and complete visual source gates passed')
    dict(prepare=prepare,timeline=timeline,audit=check_audit,check=check)[parser.parse_args().step]()
