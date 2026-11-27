"""Add short reflection pauses only in inter-idea gaps, without changing speech rate/pitch.
Original Gemini WAVs and alignments remain untouched. Word times shift by inserted silence.
"""
import hashlib,json,wave,argparse
from pathlib import Path
from speech_pause import quiet_cut
p=argparse.ArgumentParser();p.add_argument('--plan',default='src/video/n3-plan.json');p.add_argument('--audio-dir',default='n3-paced');p.add_argument('--output',default='src/video/n3-paced-plan.json');p.add_argument('--gap-seconds',type=float,help='minimum silence between narrated ideas');args=p.parse_args()
if args.gap_seconds is not None and not 0 < args.gap_seconds <= 3:p.error('--gap-seconds must be in (0, 3]')
root=Path('public')/args.audio_dir;(root/'alignment').mkdir(parents=True,exist_ok=True)
plan=json.loads(Path(args.plan).read_text(encoding='utf-8'));report=[]
for scene in plan['scenes']:
 source=Path('public')/scene['audio'];alignment=json.loads((source.parent/'alignment'/(scene['id']+'.json')).read_text(encoding='utf-8'))
 assert alignment['signature']==hashlib.sha256(source.read_bytes()+scene['narration'].encode('utf-8')).hexdigest()
 words=alignment['words'];boundaries=[];skipped=[];index=0
 with wave.open(str(source)) as w:params=w.getparams();pcm=w.readframes(w.getnframes());rate=w.getframerate();width=w.getsampwidth()*w.getnchannels()
 for beat in scene['beats'][:-1]:
  import re
  index+=len([x for x in (re.sub(r'[^\wً-ْٰ]','',t) for t in beat['text'].split()) if x])
  before,after=words[index-1]['end'],words[index]['start'];gap=max(0,after-before)
  if after<before:continue
  target=1.0 if scene['kind'] in ['verification','divisible-example','property1','property2','multiples','divisors','prime-ranges','one'] else 0.85
  extra=0 if gap>=1.2 else max(0.25,target-gap)
  requested=beat.get('pauseAfter',args.gap_seconds)
  if requested is not None:
   assert 0 < requested <= 3, (scene['id'], requested)
   extra=max(0,requested-gap)
  if extra>0.08:
   sample=quiet_cut(pcm,rate,params.sampwidth,params.nchannels,before,after)
   if sample is None:
    skipped.append(dict(before=before,after=after,reason='No verified quiet PCM window; never insert silence in active speech'))
    continue
   count=round(extra*rate)
   boundaries.append(dict(sample=sample,frames=count,originalGap=round(gap,3)))
 chunks=[];last=0
 for cut in boundaries:chunks.extend([pcm[last*width:cut['sample']*width],b'\0'*(cut['frames']*width)]);last=cut['sample']
 chunks.append(pcm[last*width:]);target=root/(scene['id']+'.wav')
 with wave.open(str(target),'wb') as w:w.setparams(params);w.writeframes(b''.join(chunks))
 def shift(t):return t+sum(c['frames']/rate for c in boundaries if c['sample']/rate<=t)
 for word in words:word.update(start=round(shift(word['start']),3),end=round(shift(word['end']),3))
 alignment.update(signature=hashlib.sha256(target.read_bytes()+scene['narration'].encode('utf-8')).hexdigest(),pauseEdits=boundaries,skippedUnsafePauseEdits=skipped)
 (root/'alignment'/(scene['id']+'.json')).write_text(json.dumps(alignment,ensure_ascii=False,indent=2),encoding='utf-8')
 receipt=json.loads(Path(str(source)+'.json').read_text());receipt.update(processing='Short inter-idea reflection gaps; unchanged pitch and speech rate',sourceAudio=scene['audio'])
 Path(str(target)+'.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');scene['audio']=str(target.relative_to('public')).replace('\\','/')
 report.append(dict(id=scene['id'],pausesAdded=len(boundaries),secondsAdded=round(sum(c['frames']/rate for c in boundaries),3),unsafePausesSkipped=len(skipped)))
Path(args.output).write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'pacing-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Paced',len(plan['scenes']),'scenes; added',round(sum(r['secondsAdded'] for r in report),2),'seconds inside existing speech gaps.')
