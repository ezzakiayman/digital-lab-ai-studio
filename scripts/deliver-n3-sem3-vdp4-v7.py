"""Publish the approved visual-only V7 revision on the same Drive file."""
import argparse
from pathlib import Path
import runpy
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
module=runpy.run_path('scripts/deliver-n3-sem3-vdp4-v5.py')
module['main'].__globals__.update(OUT=Path('outputs/n3-sem3-v7/vdp4'),
    MOVIE=Path('outputs/n3-sem3-v7/vdp4/P1_MATHS_N3_SEM3_VDP4_V7.mp4'),VERSION=7)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('step',choices=['snapshot','deliver'])
module['main'](parser.parse_args().step)
