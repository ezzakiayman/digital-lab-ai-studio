"""Verify the finished full export without modifying it."""
import json,subprocess,re
from pathlib import Path
root=Path('outputs/full');video=root/'Digital-Lab-Comparer-et-ranger.mp4'
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True,encoding='utf-8'))
v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'])==(1920,1080,'h264','30/1')
assert a['codec_name']=='aac' and abs(float(meta['format']['duration'])-180)<0.1
assert int(v['nb_frames'])==5400
decode=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(video),'-f','null','-'],capture_output=True,text=True)
assert decode.returncode==0 and not decode.stderr.strip(),decode.stderr
qc=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vf','blackdetect=d=0.1:pix_th=0.02','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
assert qc.returncode==0
black=re.findall(r'black_start:[^\n]+',qc.stderr)
assert not black,black
report={'video':video.name,'width':1920,'height':1080,'fps':30,'frames':5400,'durationSeconds':float(meta['format']['duration']),'videoCodec':'h264','audioCodec':'aac','fullDecode':'passed','unexpectedBlackIntervals':black,'audioPeakDb':re.findall(r'max_volume: ([\-\d.]+) dB',qc.stderr),'limits':'Black-frame detection does not detect white blank frames. Typography and word alignment are manually reviewed, not certified.'}
(root/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
