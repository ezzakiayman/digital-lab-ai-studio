"""Inspector's two corrections, preserving the original French and source video."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import runpy
import subprocess

import numpy as np

BASE = Path('src/video/n1-sem3-vdp1-lesson.json')
STEM = 'n1-sem3-vdp1-v2'
OUT = Path('outputs') / STEM
PUBLIC = Path('public')
AR = PUBLIC / STEM / 'objectif-ar.wav'
HELP = runpy.run_path('scripts/prepare-n1-sem3-vdp1.py')


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf8')


def prepare():
    write(Path('src/video') / (STEM+'-arabic-plan.json'), {'scenes': [{
        'id': STEM+'-objectif-ar', 'audio': AR.relative_to(PUBLIC).as_posix(),
        'narration': 'سَنَتَعَرَّفُ عَلَيْهَا خِلَالَ هَذِهِ الْحِصَّةِ.',
        'speechMode': 'verbatim', 'languageCode': 'ar', 'speed': .94, 'stability': .45,
    }]})


def build():
    before = load(BASE)
    after = copy.deepcopy(before)
    original = before['scenes'][0]
    old_audio = PUBLIC / original['audio']
    tag = load(Path(str(old_audio)+'.json'))
    alignment = load(old_audio.parent / 'alignment' / (original['id']+'.json'))
    start = tag['arabicStartSample']
    start += sum(g['frames'] for g in alignment['pauseEdits'] if g['sample'] <= start)
    original_pcm = HELP['pcm'](old_audio)
    old_ar = HELP['pcm'](Path(tag['parts'][1]))
    assert original_pcm[start*2:] == old_ar, 'Arabic must be the isolated final insert'
    new_ar = HELP['pcm'](AR)
    combined = AR.with_name('objectif.wav')
    HELP['save_wave'](combined, original_pcm[:start*2]+new_ar)
    ar_tag = load(Path(str(AR)+'.json'))
    tag.update(arabicStartSample=start, arabicSamples=len(new_ar)//2,
               arabicModel=ar_tag['model'], arabicVoice=ar_tag['voice'],
               arabicLanguageCode='ar', parts=[tag['parts'][0], AR.as_posix()],
               revision='Inspector: حصة; original French PCM retained exactly',
               sourceAudio=old_audio.relative_to(PUBLIC).as_posix())
    write(Path(str(combined)+'.json'), tag)
    intro = after['scenes'][0]
    hold = original['durationInFrames'] - math.ceil(len(original_pcm)/1600)
    intro.update(audio=combined.relative_to(PUBLIC).as_posix(),
                 durationInFrames=math.ceil((start*2+len(new_ar))/1600)+hold)
    vocab = after['scenes'][-1]
    formula = next(v for v in vocab['art'] if v['kind']=='algebra' and v['value']==HELP['SUMMARY'])
    # Only operation signs change; signed numbers and their signs retain their appearance.
    for token in formula['tokenColors']:
        token['color'] = HELP['INK']
    assert before['scenes'][1:-1] == after['scenes'][1:-1]
    assert before['scenes'][-1]['audio'] == vocab['audio']
    assert HELP['pcm'](combined)[:start*2] == original_pcm[:start*2]
    write(Path('src/video')/(STEM+'-lesson.json'), after)
    write(OUT/'revision-source.json', {
        'sourceTimeline': BASE.as_posix(), 'arabicStartSeconds': start/24000,
        'arabicDurationSeconds': len(new_ar)/48000,
        'frenchPcmUnchanged': True, 'unchangedAudioScenes': 6,
        'unchangedVisualScenes': 6, 'blackOperationIndex': HELP['operators'](HELP['SUMMARY'])[-1],
        'sourcePronunciationClipUnchanged': True,
        'originalArabicSha256': hashlib.sha256(old_ar).hexdigest(),
        'revisedArabicSha256': hashlib.sha256(new_ar).hexdigest(),
    })
    print('Revision ready:', sum(s['durationInFrames'] for s in after['scenes']), 'frames')


def check():
    """Audit the changed insert and all seven AAC scene starts, without ASR prompting."""
    helpers = runpy.run_path('scripts/check-n3-sem3-bilingual.py')
    before = load(BASE)
    after = load(OUT/'timeline.json')
    audit = load(OUT/'revision-source.json')
    video = OUT/'P1_MATHS_N1_SEM3_VDP1_V2.mp4'
    track = np.frombuffer(subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(video), '-ac', '1', '-ar', '24000', '-f', 'f32le', '-'
    ]), dtype='<f4')
    report = []
    offset = 0
    for i, (prior, scene) in enumerate(zip(before['scenes'], after['scenes'])):
        pcm = helpers['samples'](PUBLIC/scene['audio'])
        entry = {'scene': scene['id'], 'aacCorrelation': helpers['match_audio'](track, pcm[:24000], offset)}
        if i == 0:
            start = round(audit['arabicStartSeconds']*24000)
            original = helpers['samples'](PUBLIC/prior['audio'])
            assert np.array_equal(pcm[:start], original[:start])
            arabic = helpers['samples'](AR)
            assert np.array_equal(pcm[start:], arabic)
            entry.update(frenchPcmUnchanged=True,
                         correctedArabicAacCorrelation=helpers['match_audio'](track, arabic, offset+start))
        else:
            assert prior['audio'] == scene['audio']
        if i == 5:
            clip = next(v for v in scene['art'] if v['kind']=='clip')
            source = np.frombuffer(subprocess.check_output([
                'ffmpeg', '-v', 'error', '-i', str(PUBLIC/clip['value']), '-ac', '1', '-ar',
                '24000', '-f', 's16le', '-']), dtype='<i2')
            clip_start = clip['frame']*800
            assert np.array_equal(pcm[clip_start:clip_start+len(source)], source)
            entry['originalPronunciationAacCorrelation'] = helpers['match_audio'](track, source, offset+clip_start)
        report.append(entry)
        offset += scene['durationInFrames']*800
    write(OUT/'voice-verification.json', report)
    verification = load(OUT/'verification.json')
    tag = load(Path(str(AR)+'.json'))
    verification.update(audio='Gemini French narration, isolated ElevenLabs Arabic insert, original pronunciation clip; AAC',
                        arabicInsert={'provider': tag['provider'], 'voice': tag['voice'],
                                      'model': tag['model'], 'languageCode': tag['languageCode'],
                                      'startSeconds': audit['arabicStartSeconds']})
    write(OUT/'verification.json', verification)
    print('French PCM, original pronunciation and seven encoded scene starts verified')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'build', 'check'])
    {'prepare': prepare, 'build': build, 'check': check}[p.parse_args().action]()
