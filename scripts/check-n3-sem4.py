"""Check mathematics and review narration in the encoded 3AC week 4 videos."""
import argparse
import json
import math
from pathlib import Path
import runpy
import subprocess

import numpy as np
from faster_whisper import WhisperModel

ROOT=Path("outputs/n3-sem4")
SOURCE=Path("src/video")
PUBLIC=Path("public")
helpers=runpy.run_path("scripts/check-n3-sem3-bilingual.py")
load,samples,match_audio,RATE = (helpers[name] for name in ("load","samples","match_audio","RATE"))


def verify_math():
    checked=0
    for numerator in range(0,31):
        for denominator in range(0,31):
            assert math.isclose(math.sqrt(numerator)*math.sqrt(denominator),
                                math.sqrt(numerator*denominator),abs_tol=1e-12)
            if denominator>0:
                assert math.isclose(math.sqrt(numerator)/math.sqrt(denominator),
                                    math.sqrt(numerator/denominator),abs_tol=1e-12)
            checked+=1
    assert math.isclose(math.sqrt(2)*math.sqrt(8),4)
    assert math.sqrt(16*25)==math.sqrt(16)*math.sqrt(25)==20
    assert math.sqrt(8)/math.sqrt(2)==math.sqrt(8/2)==2
    assert math.sqrt(25/16)==math.sqrt(25)/math.sqrt(16)==1.25
    assert 3*5==15 and 12/3==4 and math.sqrt(9)==3
    return checked


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episodes",nargs="*",type=int,choices=(1,2))
    episodes=parser.parse_args().episodes or (1,2)
    checked=verify_math()
    model=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4,local_files_only=True,
                      download_root=str(Path.home()/".cache/digital-lab-whisper"))
    for episode in episodes:
        root=ROOT/f"vdp{episode}"
        video=root/f"P1_MATHS_N3_SEM4_VDP{episode}.mp4"
        timeline=load(root/"timeline.json")
        original=load(SOURCE/f"n3-sem4-vdp{episode}-lesson.json")
        assert timeline==original
        assert [n for scene in timeline["scenes"] for n in scene["sourceSlides"]]==list(range(1,17))
        raw=subprocess.check_output(["ffmpeg","-v","error","-i",str(video),"-map","0:a:0",
                                     "-ac","1","-ar",str(RATE),"-f","f32le","-"])
        track=np.frombuffer(raw,dtype="<f4")
        offset=0
        report=[]
        for scene in timeline["scenes"]:
            source=PUBLIC/scene["audio"]
            receipt=load(Path(str(source)+".json"))
            assert receipt["voice"]=="05Y5uLueU3x8LrkGHu0H" and receipt["languageCode"]=="fr" and receipt["model"]=="eleven_v4"
            assert receipt["settings"]["speed"]==.94 and receipt["settings"]["stability"]==.45
            item={"scene":scene["id"],"encodedStartCorrelation":match_audio(track,samples(source,count=RATE),offset)}
            key=scene["id"].split("-",3)[-1]
            if key in ("propriete","exemple-1","exemple-2","vocabulaire"):
                waveform=track[offset:offset+scene["durationInFrames"]*(RATE//30)]
                converted=np.interp(np.arange(0,len(waveform)-1,1.5),np.arange(len(waveform)),waveform).astype(np.float32)
                segments,_=model.transcribe(converted,language="fr",beam_size=5,vad_filter=False,condition_on_previous_text=False)
                item["independentASR"]=" ".join(s.text.strip() for s in segments)
                print(scene["id"],item["independentASR"],flush=True)
            if scene.get("pronunciation"):
                syllables=[]
                for index in range(1,len(scene["beats"])-1):
                    a=scene["beats"][index]["from"]*(RATE//30)
                    b=scene["beats"][index+1]["from"]*(RATE//30)
                    spoken=track[offset+a:offset+b]
                    peak=float(np.abs(spoken).max())
                    assert peak>.015,(scene["id"],index,peak)
                    syllables.append({"beat":index,"peak":round(peak,4)})
                item["syllables"]=syllables
            report.append(item)
            offset+=scene["durationInFrames"]*(RATE//30)
        write={"samplePairsChecked":checked,"method":"Independent ASR without supplied transcript and encoded PCM correlation",
               "scenes":report}
        (root/"voice-review.json").write_text(json.dumps(write,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"VDP{episode}: {len(report)} scènes, 16 diapositives, PCM min {min(x['encodedStartCorrelation'] for x in report):.4f}",flush=True)


if __name__=="__main__":
    main()

