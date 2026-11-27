"""The latest source decision overrides earlier proposed property rewrites."""
import copy
import runpy
import unittest

M=runpy.run_path('scripts/revise-n3-sem3-vdp4-v6.py')


class SourceDecision(unittest.TestCase):
    def test_verbatim_property_and_reject_earlier_rewrite(self):
        data=M['load'](M['DEST'])
        M['source_check'](data)
        bad=copy.deepcopy(data)
        bad['scenes'][11]['narration']=M['load'](M['BASE'])['scenes'][11]['narration']
        with self.assertRaises(AssertionError):M['source_check'](bad)

    def test_protected_other_scenes_and_pronunciation_words(self):
        data=M['load'](M['DEST'])
        M['delta_check'](data)
        bad=copy.deepcopy(data)
        bad['scenes'][4]['art'].pop()
        with self.assertRaises(AssertionError):M['delta_check'](bad)
        bad=copy.deepcopy(data)
        bad['scenes'][1]['narration']+=' Ajout.'
        with self.assertRaises(AssertionError):M['delta_check'](bad)


if __name__=='__main__':unittest.main()
