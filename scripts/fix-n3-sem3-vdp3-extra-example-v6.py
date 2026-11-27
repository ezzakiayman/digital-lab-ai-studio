"""Remove only the unrequested previous example; preserve every audio and timing."""
import argparse
import copy
import hashlib
from pathlib import Path
import runpy
import subprocess

BASE = Path('src/video/n3-sem3-vdp3-v5-lesson.json')
DEST = Path('src/video/n3-sem3-vdp3-v6-lesson.json')
OUT = Path('outputs/n3-sem3-v6/vdp3')
HELP = runpy.run_path('scripts/revise-n3-sem3-vdp3-v5.py')
load, write = HELP['load'], HELP['write']


def source_check(data):
    """Check all visuals against this passage's slides, never an earlier example."""
    scene = next(s for s in data['scenes'] if s['id'] == 'vdp3-fraction-1')
    rows = HELP['source_rows']()
    start = [s['text'] for s in rows[15]['shapes'] if s['role'] == 'student']
    final = ' '.join(s['text'] for s in rows[16]['shapes'] if s['role'] == 'student')
    art = scene['art']
    assert len(art) == 3, 'Unexpected visual in slides 16–17; no previous-example reminder allowed'
    assert [v['kind'] for v in art] == ['math', 'text', 'math']
    equal = lambda a, b: HELP['compact'](a) == HELP['compact'](b)
    assert equal(HELP['semantic'](art[0]['value']), start[0])
    assert equal(art[1]['value'], start[1])
    assert equal(HELP['semantic'](art[2]['value']), final)
    assert art[0]['toFrame'] == art[2]['frame']
    return dict(sourceSlides=[16, 17], visualCount=3,
                finalEquationMatchesOwnSlide=True, noPreviousExample=True)


def delta_check(before, data):
    expected = copy.deepcopy(before)
    scene = next(s for s in expected['scenes'] if s['id'] == 'vdp3-fraction-1')
    assert len(scene['art']) == 4
    removed = scene['art'].pop()
    assert HELP['compact'](HELP['semantic'](removed['value'])) == '225/10^2=2,25'
    assert expected == data, 'Change exceeds authorized removal'


def prepare():
    before = load(BASE)
    data = copy.deepcopy(before)
    scene = next(s for s in data['scenes'] if s['id'] == 'vdp3-fraction-1')
    scene['art'].pop()
    delta_check(before, data)
    gate = source_check(data)
    HELP['audit'](data)
    write(DEST, data)
    write(OUT / 'revision-source.json', dict(
        sourceTimeline=BASE.as_posix(), sourceTimelineSha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
        userApprovedRemoval=True, correctedScene=scene['id'], removedVisualIndex=3,
        narrationUnchanged=True, allTenAudioFilesUnchanged=True, durationUnchanged=True,
        otherNineScenesIdentical=True, remainingVisualsUnchanged=True, sourceGate=gate))
    print('Only extra visual removed; all ten audio files, durations and nine other scenes unchanged')


def check():
    data = load(OUT / 'timeline.json')
    delta_check(load(BASE), data)
    source_check(data)
    HELP['audit'](data)
    tracks = []
    for folder, name in [('n3-sem3-v5', 'V5'), ('n3-sem3-v6', 'V6')]:
        movie = Path('outputs') / folder / 'vdp3' / f'P1_MATHS_N3_SEM3_VDP3_{name}.mp4'
        tracks.append(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(movie),
                       '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', '-']))
    assert tracks[0] == tracks[1], 'Encoded AAC changed'
    write(OUT / 'voice-verification.json', dict(
        narrationUnchanged=True, allTenAudioFilesUnchanged=True,
        encodedAacByteIdenticalToV5=True, aacSha256=hashlib.sha256(tracks[1]).hexdigest(),
        otherNineScenesIdentical=True, remainingVisualsUnchanged=True,
        sourceGate=source_check(data)))
    print('Complete encoded AAC byte-identical to V5; source membership and exact deletion verified')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step', choices=['prepare', 'check'])
    dict(prepare=prepare, check=check)[parser.parse_args().step]()
