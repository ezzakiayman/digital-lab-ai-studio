"""Prepare French Kore audio and slide cues for the revised 2AC week 1 monomial lesson.

Supply the reviewed 33-slide PPTX locally. Between prepare and timing, run the project's
Gemini TTS and MMS alignment commands on voice-plan.json from the project root.
"""
import argparse
import hashlib
import json
import math
import re
import wave
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from speech_pause import quiet_cut

ROOT = Path(__file__).resolve().parents[1]
LESSON = 'n2-sem1-vdp4-v2'
SOURCE_SHA256 = '4a70f4f3267284922bb9257f7060f622f8d63f6c16a8aff0523b88cbef3fba56'
FPS = 30
HOLD = 0.55
NAMESPACES = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}
SCENES = [
    ('objectif', 1, 3), ('definition-monome', 4, 5),
    ('exemple-monome', 6, 9), ('contre-exemple', 10, 13),
    ('coefficient-variables', 14, 18), ('definition-degre', 19, 20),
    ('calcul-degre', 21, 26), ('mot-monome', 27, 27),
    ('mot-degre', 28, 28), ('vocabulaire', 29, 33),
]
# These lines continue directly into the next slide, mid-sentence.
JOINED_SLIDES = {7, 11, 15, 17}
STYLE = (
    "Diction enseignante naturelle du français de France, calme, chaleureuse et intelligible. "
    "Prononcer les lettres et les nombres en français dans leur contexte mathématique. "
    "Laisser de courtes respirations entre les idées. Respecter la continuité grammaticale à l'intérieur des phrases."
)
VOCABULARY = {
    27: (['Mo.', 'Nôme.', 'Monôme.'],
         "Énoncer distinctement chaque partie du mot français monôme avec le timbre de la syllabe du mot, "
         "puis le mot entier naturellement. Faire une courte pause entre les parties."),
    28: (['De.', 'Gré.', 'Degré.'],
         "Énoncer distinctement chaque partie du mot français degré, de comme le mot français « de », "
         "gré comme le mot français « gré », puis le mot degré naturellement. Faire une courte pause entre les parties."),
}


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def source_bands(source):
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("This plan requires the reviewed 33-slide PPTX. A changed deck requires a new source review.")
    bands = {}
    with zipfile.ZipFile(source) as deck:
        for number in range(1, 34):
            slide = ET.fromstring(deck.read(f'ppt/slides/slide{number}.xml'))
            candidates = []
            for shape in slide.findall('./p:cSld/p:spTree/p:sp', NAMESPACES):
                offset = shape.find('./p:spPr/a:xfrm/a:off', NAMESPACES)
                if offset is None or int(offset.get('y')) >= 750000:
                    continue
                paragraphs = shape.findall('./p:txBody/a:p', NAMESPACES)
                text = ' '.join(''.join(t.text or '' for t in p.iter() if t.tag.endswith('}t'))
                                for p in paragraphs).strip()
                if text:
                    candidates.append(text)
            if len(candidates) != 1:
                raise ValueError(f'Expected one reviewed voice band on slide {number}.')
            bands[number] = candidates[0]
    return bands


def prepare(source, out):
    bands = source_bands(source)
    scenes = []
    for name, first, last in SCENES:
        numbers = list(range(first, last + 1))
        units = [dict(slide=number, role='sourceVoice', text=bands[number]) for number in numbers]
        style = STYLE
        kind = 'teaching'
        if first in VOCABULARY:
            parts, instructions = VOCABULARY[first]
            roles = ['syllable1', 'syllable2', 'joinedWord']
            units.extend(dict(slide=first, role=role, text=text) for role, text in zip(roles, parts, strict=True))
            style += ' ' + instructions
            kind = 'pronunciation'
        scenes.append(dict(id=name, sourceSlides=numbers, kind=kind, languageCode='fr-FR',
                           speechStyle=style, speechMode='verbatim', audio=f'{LESSON}-raw/{name}.wav',
                           narration=' '.join(u['text'] for u in units), units=units))
    write_json(out / 'voice-plan.json', dict(sourceSha256=SOURCE_SHA256, scenes=scenes))


def collect_units(scene, words, pcm, rate):
    units = []
    cuts = []
    cursor = 0
    for i, unit in enumerate(scene['units']):
        tokens = [re.sub(r'[^\wً-ْٰ]', '', token) for token in unit['text'].split()]
        tokens = [token for token in tokens if token]
        stop = cursor + len(tokens)
        span = words[cursor:stop]
        if not span or [word['word'] for word in span] != tokens:
            raise ValueError(f"Unexpected aligned words for {scene['id']}, slide {unit['slide']}.")
        if i and scene['units'][i-1]['slide'] not in JOINED_SLIDES:
            left, right = words[cursor-1]['end'], span[0]['start']
            gap = right - left
            target = 0.50 if scene['kind'] == 'pronunciation' else 0.58
            if 0 <= gap < target - 0.08:
                sample = quiet_cut(pcm, rate, 2, 1, left, right)
                if sample is not None:
                    cuts.append((sample, round((target-gap)*rate)))
        units.append(dict(**unit, startWordIndex=cursor, endWordIndex=stop-1,
                          start=span[0]['start'], end=span[-1]['end']))
        cursor = stop
    if cursor != len(words):
        raise ValueError(f"Unassigned words in {scene['id']}.")
    return units, cuts


def time_scene(scene, public):
    audio = public / scene['audio']
    raw_bytes = audio.read_bytes()
    transcript = scene['narration'].encode('utf-8')
    receipt = load_json(Path(str(audio) + '.json'))
    alignment = load_json(audio.parent / 'alignment' / (scene['id'] + '.json'))
    if alignment['signature'] != hashlib.sha256(raw_bytes + transcript).hexdigest():
        raise ValueError(f"Stale alignment for {scene['id']}.")
    if (receipt.get('provider'), receipt.get('voice'), receipt.get('languageCode'), receipt.get('speechStyle')) != (
        'gemini', 'Kore', 'fr-FR', scene['speechStyle']
    ):
        raise ValueError(f"Wrong voice profile for {scene['id']}.")
    with wave.open(str(audio), 'rb') as wav:
        params = wav.getparams()
        pcm = wav.readframes(wav.getnframes())
    if (params.framerate, params.nchannels, params.sampwidth) != (24000, 1, 2):
        raise ValueError(f"Expected 24 kHz mono PCM16 for {scene['id']}.")
    rate = params.framerate
    words = alignment['words']
    units, cuts = collect_units(scene, words, pcm, rate)
    chunks = []
    last = 0
    for sample, extra in cuts:
        chunks.extend([pcm[2*last:2*sample], bytes(2*extra)])
        last = sample
    chunks.append(pcm[2*last:])
    final_pcm = b''.join(chunks)

    def shifted(t):
        return round(t + sum(n / rate for sample, n in cuts if sample/rate <= t), 3)

    for unit in units:
        unit.update(start=shifted(unit['start']), end=shifted(unit['end']))
        unit['frame'] = round(unit['start'] * FPS)
    for word in words:
        word.update(start=shifted(word['start']), end=shifted(word['end']))

    output = public / LESSON / (scene['id'] + '.wav')
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(final_pcm)
    alignment['signature'] = hashlib.sha256(output.read_bytes() + transcript).hexdigest()
    write_json(output.parent / 'alignment' / (scene['id'] + '.json'), alignment)
    write_json(Path(str(output) + '.json'), {**receipt, 'sourceAudio': scene['audio'],
               'sourceSha256': hashlib.sha256(raw_bytes).hexdigest(), 'quietPauseEdits': cuts})
    seconds = len(final_pcm) / 2 / rate
    return dict(id=scene['id'], kind=scene['kind'], sourceSlides=scene['sourceSlides'],
                narration=scene['narration'], audio=output.relative_to(public).as_posix(),
                units=units, words=words, audioSeconds=round(seconds, 5), holdSeconds=HOLD,
                durationInFrames=math.ceil((seconds+HOLD)*FPS), quietPauseEdits=cuts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    stages = parser.add_subparsers(dest='stage', required=True)
    prep = stages.add_parser('prepare', help='Read the exact local PPTX and prepare its TTS manifest.')
    prep.add_argument('--source', required=True, type=Path, help='Path to the privately supplied 33-slide PPTX.')
    timing = stages.add_parser('timing', help='Read generated WAVs and MMS alignment, write timed clips and cues.')
    timing.add_argument('--public-dir', type=Path, default=ROOT/'public', help='Input and output audio asset root.')
    for stage in (prep, timing):
        stage.add_argument('--output-dir', type=Path, default=ROOT/'outputs'/LESSON, help='Folder containing the manifests.')
    args = parser.parse_args()
    if args.stage == 'prepare':
        prepare(args.source, args.output_dir)
        print(f"Prepared {len(SCENES)} French voice blocks in {args.output_dir / 'voice-plan.json'}.")
    else:
        manifest = load_json(args.output_dir / 'voice-plan.json')
        if manifest.get('sourceSha256') != SOURCE_SHA256:
            raise ValueError("Unexpected source signature in voice plan.")
        results = [time_scene(scene, args.public_dir) for scene in manifest['scenes']]
        write_json(args.output_dir / 'voice-timing.json', dict(fps=FPS, sourceSha256=SOURCE_SHA256, scenes=results))
        print(f"Prepared {len(results)} timed clips in {args.public_dir / LESSON}.")


if __name__ == '__main__':
    main()
