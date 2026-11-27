"""Check the corrected passage in encoded frames, including the former extra row."""
import json
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image

OUT = Path('outputs/n3-sem3-v6/vdp3')


def bands(indices):
    result = []
    for i in indices:
        if not result or i > result[-1][-1] + 1:
            result.append([int(i)])
        else:
            result[-1].append(int(i))
    return result


frame = np.asarray(Image.open(OUT / 'export-vdp3-fraction-1.png').convert('RGB'))
black = frame.max(axis=2) < 90
fraction = bands(np.where(black[435:515, 600:850].sum(axis=1) > 140)[0] + 435)
equals = bands(np.where(black[435:515, 850:990].sum(axis=1) > 55)[0] + 435)
assert len(fraction) == 1 and len(equals) == 2
bar = (fraction[0][0] + fraction[0][-1]) / 2
axis = sum((b[0] + b[-1]) / 2 for b in equals) / 2
assert abs(bar - axis) <= 1.5
samples = sorted(OUT.glob('export-*vdp3-fraction-1*.png'))
assert len(samples) >= 5
rows = []
for path in samples:
    pixels = np.asarray(Image.open(path).convert('RGB'))
    # Interior below all retained visuals; excludes the turquoise frame.
    ink = int((pixels[650:930, 250:1680].min(axis=2) < 150).sum())
    assert ink == 0, (path.name, ink)
    rows.append(dict(frame=path.name, unexpectedLowerRowPixels=ink))
timeline = json.loads((OUT / 'timeline.json').read_text('utf-8'))
scene = timeline['scenes'][5]
assert scene['id'] == 'vdp3-fraction-1'
start = sum(s['durationInFrames'] for s in timeline['scenes'][:5])
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(start / 30),
    '-i', str(OUT / 'P1_MATHS_N3_SEM3_VDP3_V6.mp4'),
    '-frames:v', str(scene['durationInFrames']),
    '-vf', 'crop=1430:280:250:650,scale=160:32', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'])
continuous = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 32, 160, 3)
assert len(continuous) == scene['durationInFrames']
assert continuous.min() >= 150, 'Unexpected ink in previous-row area during passage'
report = dict(fractionAxis=bar, equalsAxis=axis, deltaPixels=abs(bar-axis),
              lowerAreaEmptyInEncodedCheckpoints=rows,
              lowerAreaContinuousFramesChecked=len(continuous))
(OUT / 'encoded-layout-check.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f'Encoded math axes aligned ({abs(bar-axis):.1f} px); previous-row area empty in {len(rows)} checkpoints and {len(continuous)} continuous frames')
