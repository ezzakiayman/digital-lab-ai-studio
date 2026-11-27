"""Reject silence insertion inside speech, including the reported VDP4 regression."""
from array import array
import math
from pathlib import Path
import runpy
import unittest
import wave

quiet_cut=runpy.run_path('scripts/speech_pause.py')['quiet_cut']


class SafePause(unittest.TestCase):
    def pcm(self,silence=None):
        rate=24000
        return array('h',(0 if silence and silence[0]<=i/rate<=silence[1]
            else round(.2*32767*math.sin(2*math.pi*220*i/rate)) for i in range(rate))).tobytes()

    def test_rejects_an_active_voice_boundary(self):
        self.assertIsNone(quiet_cut(self.pcm(),24000,2,1,.49,.51))

    def test_preserves_actual_quiet_gaps(self):
        cut=quiet_cut(self.pcm((.4,.6)),24000,2,1,.42,.58)
        self.assertIsNotNone(cut)
        self.assertAlmostEqual(cut/24000,.5,places=3)

    def test_real_reported_cut_is_rejected(self):
        p=Path('public/n3-sem3-elevenlabs-v5-vdp4/vdp4-prononciation-5.wav')
        with wave.open(str(p)) as w:
            params=w.getparams();pcm=w.readframes(w.getnframes())
        self.assertIsNone(quiet_cut(pcm,params.framerate,params.sampwidth,params.nchannels,6.135,6.155))


if __name__=='__main__':unittest.main()
