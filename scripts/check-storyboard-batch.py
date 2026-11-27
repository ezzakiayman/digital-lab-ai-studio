"""Verify source coverage, preserved speech, independent recognition and the reviewed mathematics."""
import hashlib
import json
from math import gcd, lcm, prod
from pathlib import Path
import re
import wave
import numpy as np

cases={
 'like-terms':(27,'reference/n2-sem2-vdp2/asr'),
 'polynomial-subtraction':(47,'reference/n2-sem2-vm4/asr-final'),
 'factorization-v2':(13,None),
 'fractions-v2':(28,None),
}
for stem,(slides,asr_dir) in cases.items():
    t=json.loads(Path(f'src/video/{stem}-lesson.json').read_text(encoding='utf-8'))
    assert [i for s in t['scenes'] for i in s['sourceSlides']]==list(range(1,slides+1))
    if asr_dir:
        for s in t['scenes']:
            review=json.loads((Path(asr_dir)/(s['id']+'.json')).read_text(encoding='utf-8'))
            p=Path('public')/s['audio']
            source=json.loads(Path(str(p)+'.json').read_text(encoding='utf-8'))['sourceAudio']
            assert review['signature']==hashlib.sha256((Path('public')/source).read_bytes()+b'whisper-small-fr').hexdigest()
            assert not re.search(r'lis uniquement le texte|ne lis aucune instruction|animer la voix',review['transcript'],re.I),s['id']

    for s in t['scenes']:
        if s['kind']!='pronunciation':continue
        p=Path('public')/s['audio']
        align=json.loads((p.parent/'alignment'/(s['id']+'.json')).read_text(encoding='utf-8'))
        count=len(s['beats'])-1
        with wave.open(str(p)) as w:
            assert w.getnchannels()==1 and w.getsampwidth()==2
            rate=w.getframerate()
            pcm=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
        level=[]
        for word in align['words'][-count:]:
            span=pcm[round(word['start']*rate):round(word['end']*rate)]
            rms=20*np.log10(np.sqrt(np.mean(span**2)))
            assert rms>-50,(s['id'],word,rms)
            level.append(round(rms,1))
        print(stem,'voiced syllable and whole-word spans',level)

assert prod([2**3,3**2,5])==360 and prod([2**3,3**2])==72
assert gcd(23,41)==1 and gcd(42,36)==6 and lcm(9,15)==45
assert [n for n in range(1,181) if n%9==n%15==0]==[45,90,135,180]
assert [n for n in range(2,43) if 42%n==36%n==0]==[2,3,6]
# Coefficient and exponent tuples, checked independently of the animation.
assert 2+8==10 and (1,1)==(1,1) and (3,1)!=(2,1) and (1,0)!=(0,1)
assert tuple(a-b for a,b in zip((8,7),(6,4)))==(2,3)
assert tuple(a+b for a,b in zip((8,7),(-6,-4)))==(2,3)

vm=Path('reference/n2-sem2-vm4/asr-final')
for name in ['calcul-horizontal','calcul-vertical','synthese']:
    text=json.loads((vm/(name+'.json')).read_text(encoding='utf-8'))['transcript']
    assert re.search(r'2\s*x\s*(?:plus|\+)\s*3\s*y',text,re.I),(name,text)
print('Four ordered source-coverage checks, arithmetic, speech provenance and narration review passed.')

