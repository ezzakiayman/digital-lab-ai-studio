import json,subprocess,re,wave,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',nargs='?',default='outputs/n3');p.add_argument('--filename',default='Digital-Lab-3AC-PPCM.mp4');p.add_argument('--slides',type=int,default=39);args=p.parse_args()
root=Path(args.root);video=root/args.filename;timeline=json.loads((root/'timeline.json').read_text(encoding='utf-8'))
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True,encoding='utf-8'))
v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');frames=sum(s['durationInFrames'] for s in timeline['scenes'])
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'])==(1920,1080,'h264','30/1')
assert int(v['nb_frames'])==frames and a['codec_name']=='aac'
assert abs(float(meta['format']['duration'])-frames/30)<0.1
covered=sorted({i for s in timeline['scenes'] for i in s['sourceSlides']});assert covered==list(range(1,args.slides+1))
models={};providers={};voices=set()
for scene in timeline['scenes']:
 p=Path('public')/scene['audio'];receipt=json.loads(Path(str(p)+'.json').read_text());models[receipt['model']]=models.get(receipt['model'],0)+1;provider=receipt.get('provider','gemini');providers[provider]=providers.get(provider,0)+1;voices.add(receipt['voice'])
 with wave.open(str(p)) as w:assert w.getnframes()/w.getframerate()<=scene['durationInFrames']/30
decode=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(video),'-f','null','-'],capture_output=True,text=True);assert decode.returncode==0 and not decode.stderr.strip(),decode.stderr
qc=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vf','blackdetect=d=0.1:pix_th=0.02','-af','volumedetect','-f','null','-'],capture_output=True,text=True);assert qc.returncode==0
# VDP storyboards explicitly call for brief fades from black at section changes.
transition_starts=[]
offset=0
for scene in timeline['scenes']:
 if scene['type']=='vdp-sequence' and scene.get('transition'):
  transition_starts.append(offset/30)
 offset+=scene['durationInFrames']
expected_black=[]
black=[]
for interval in re.findall(r'black_start:([-\d.]+) black_end:([-\d.]+) black_duration:([-\d.]+)',qc.stderr):
 start,end,elapsed=map(float,interval)
 if elapsed<=.201 and any(abs(start-cue)<=1/30 for cue in transition_starts):
  expected_black.append(dict(startSeconds=start,endSeconds=end))
 else:
  black.append(interval)
assert not black,black
base_timing='MMS_FA known-transcript alignment'
edited_timing=base_timing+', remapped after PCM cuts'
inserted_timing=base_timing+', remapped after PCM insertion'
embedded_timing='Source pronunciation clip synchronized to its own audio'
methods={s.get('timingMethod') for s in timeline['scenes']}
timing='Estimated phrase timings'
if methods=={base_timing}:timing='Known-transcript MMS_FA alignment'
elif methods<={base_timing,edited_timing}:timing='Known-transcript MMS_FA alignment with sample-cut offsets'
elif methods<={base_timing,edited_timing,inserted_timing}:timing='Known-transcript MMS_FA alignment with PCM edit offsets'
elif methods<={base_timing,edited_timing,inserted_timing,embedded_timing}:timing='Known-transcript MMS_FA alignment and source pronunciation clip timecode'
report={'file':video.name,'resolution':'1920x1080','fps':30,'frames':frames,'durationSeconds':float(meta['format']['duration']),'audio':', '.join(sorted(providers))+' generated, AAC','voice':', '.join(sorted(voices)),'providers':providers,'models':models,'sourceSlidesCovered':covered,'fullDecode':'passed','unexpectedBlackIntervals':black,'authoredBlackFades':expected_black,'audioPeakDb':re.findall(r'max_volume: ([\-\d.]+) dB',qc.stderr),'timing':timing,'limits':'Automatic alignment is not speech recognition; low-confidence words need review. No complete pronunciation or pixel-fidelity certification.'}
(root/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
