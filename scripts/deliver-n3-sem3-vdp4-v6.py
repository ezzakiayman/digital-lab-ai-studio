"""Use the same verified Drive revision protocol for VDP4 V6."""
import argparse
from pathlib import Path
import runpy
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
module=runpy.run_path('scripts/deliver-n3-sem3-vdp4-v5.py')
module['main'].__globals__.update(OUT=Path('outputs/n3-sem3-v6/vdp4'),
    MOVIE=Path('outputs/n3-sem3-v6/vdp4/P1_MATHS_N3_SEM3_VDP4_V6.mp4'),VERSION=6)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('step',choices=['snapshot','deliver'])
module['main'](parser.parse_args().step)
