"""Set scene durations from WAV and use cached known-transcript word intervals.
Explicit paced mode uses silence-edited WAVs with shifted alignment. If no alignment
exists, cue timing falls back to text weighting; never call that forced alignment.
"""
import json,math,wave,sys,re,hashlib
from pathlib import Path
paced='--paced' in sys.argv
plan=json.loads(Path('src/video/n3-paced-plan.json' if paced else 'src/video/n3-plan.json').read_text(encoding='utf-8'))
preview='--preview' in sys.argv
if preview:plan['scenes']=[s for s in plan['scenes'] if (Path('public')/s['audio']).exists()]
for scene in plan['scenes']:
    with wave.open(str(Path('public')/scene['audio'])) as w:
        seconds=w.getnframes()/w.getframerate()
        assert w.getnchannels()==1 and w.getsampwidth()==2 and seconds>0.5
    scene['durationInFrames']=math.ceil((seconds+(0.9 if paced else 0.45))*30)
    words=[len(b['text'].split())+2 for b in scene['beats']];total=sum(words);used=0
    alignment_path=(Path('public')/scene['audio']).parent/'alignment'/(scene['id']+'.json')
    alignment_data=json.loads(alignment_path.read_text(encoding='utf-8')) if alignment_path.exists() else None
    if alignment_data:
        signature=hashlib.sha256((Path('public')/scene['audio']).read_bytes()+scene['narration'].encode('utf-8')).hexdigest()
        if alignment_data.get('signature')!=signature:raise RuntimeError('Stale alignment for '+scene['id']+'; run scripts/align-n3.py')
    alignment=alignment_data['words'] if alignment_data else None
    scene['cues']={}
    for b,weight in zip(scene['beats'],words):
        if alignment:
            token_index=sum(len([w for w in (re.sub(r'[^\wً-ْٰ]','',t) for t in prev['text'].split()) if w]) for prev in scene['beats'][:b['stage']])
            b['from']=0 if b['stage']==0 else round(alignment[token_index]['start']*30)
        else:b['from']=round(used/total*seconds*30)
        used+=weight
    if alignment:
        scene['timingMethod']='MMS_FA known-transcript alignment'
        def cue(name,word,occurrence=0):
            hits=[w for w in alignment if w['word'].lower()==word.lower()]
            if len(hits)>occurrence:scene['cues'][name]=round(hits[occurrence]['start']*30)
        if scene['kind']=='intro':
            cue('explanation1','trouver');cue('explanation2','المضاعف');cue('positiveExamples','cinquantehuit');cue('invalidExamples','zéro')
        if scene['kind']=='multiples':
            cue('number12','douze');cue('number24','vingtquatre');cue('number36','trentesix');cue('circle12','douze',1)
        if scene['kind']=='vocabulary':
            cue('multiple','multiple');cue('commun','commun');cue('ppcm','P')
        if scene['kind']=='acronym':
            for i,(letter,word) in enumerate(zip(['P','P','C','M'],['plus','petit','commun','multiple'])):
                cue('letter'+str(i),letter,1 if i==1 else 0);cue('word'+str(i),word)
Path('reference/n3/preview.json' if preview else 'src/video/n3-lesson.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"Timeline ready: {len(plan['scenes'])} scenes, {sum(s['durationInFrames'] for s in plan['scenes'])/30:.2f} seconds.")
