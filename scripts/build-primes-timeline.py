"""Build frame cues from locally aligned, paced narration. No estimated final timing."""
import argparse,hashlib,json,math,re,wave
from pathlib import Path

def tokens(text):return [w for w in (re.sub(r'[^\wً-ْٰ]','',t).lower() for t in text.split()) if w]
p=argparse.ArgumentParser()
p.add_argument('--revised',action='store_true')
stem='primes-v2' if p.parse_args().revised else 'primes'
plan=json.loads(Path(f'src/video/{stem}-paced-plan.json').read_text(encoding='utf-8'))
number_words=[['deux','trois','cinq','sept'],['onze','treize','dix-sept','dix-neuf'],['vingt-trois','vingt-neuf'],['trente et un','trente-sept'],['quarante et un','quarante-trois','quarante-sept'],['cinquante-trois','cinquante-neuf'],['soixante et un','soixante-sept'],['soixante et onze','soixante-treize','soixante-dix-neuf'],['quatre-vingt-trois','quatre-vingt-neuf'],['quatre-vingt-dix-sept']]
for scene in plan['scenes']:
    audio=Path('public')/scene['audio']
    data=json.loads((audio.parent/'alignment'/(scene['id']+'.json')).read_text(encoding='utf-8'))
    assert data['signature']==hashlib.sha256(audio.read_bytes()+scene['narration'].encode('utf-8')).hexdigest(),scene['id']
    words=data['words'];offsets=[];index=0
    for b in scene['beats']:
        offsets.append(index);b['from']=0 if b['stage']==0 else round(words[index]['start']*30);index+=len(tokens(b['text']))
    assert index==len(words)
    with wave.open(str(audio)) as w:seconds=w.getnframes()/w.getframerate()
    scene['durationInFrames']=math.ceil((seconds+scene.get('holdSeconds',0.9))*30)
    scene['timingMethod']='MMS_FA known-transcript alignment';scene['cues']={}
    def cue(name,phrase,beat,occurrence=-1):
        start=offsets[beat];end=offsets[beat+1] if beat+1<len(offsets) else len(words)
        span=[w['word'].lower() for w in words[start:end]];needle=tokens(phrase)
        hits=[i for i in range(len(span)-len(needle)+1) if span[i:i+len(needle)]==needle]
        if not hits:raise RuntimeError(f'Missing cue {scene["id"]}/{name}: {phrase}')
        scene['cues'][name]=round(words[start+hits[occurrence]]['start']*30)
    kind=scene['kind']
    if kind=='intro':
        cue('explanation0','identifier',1);cue('explanation1','تحقق',2)
        for i,word in enumerate(['deux','trois','cinq','sept','onze']):cue('prime'+str(i),word,3)
    if kind=='definition':cue('condition','si et seulement',1);cue('two','exactement',1);cue('focus','uniquement',2)
    if kind=='divisors':
        divisors=['un','quarante et un'] if scene['value']==41 else ['un','deux','cinq','dix']
        for i,word in enumerate(divisors):cue('divisor'+str(i),word,1,1 if scene['value']==41 and i==0 else -1)
        cue('conclusion','Donc',2,0)
    if kind=='prime-ranges':
        for row in range(5):
            for col,word in enumerate(number_words[scene['rangeStart']+row]):cue(f'row{row}number{col}',word,row)
    if kind=='vocabulary':
        cue('diviseurs','Diviseur',1);cue('divisible','Divisible',2);cue('premier','Premier',3,0)
Path(f'src/video/{stem}-lesson.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Aligned prime lesson timeline:',len(plan['scenes']),'scenes,',sum(s['durationInFrames'] for s in plan['scenes'])/30,'seconds')
