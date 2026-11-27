"""Reject a correct formula displayed in the wrong storyboard passage."""
import copy
import runpy
import unittest

M = runpy.run_path('scripts/fix-n3-sem3-vdp3-extra-example-v6.py')


class SceneMembership(unittest.TestCase):
    def test_rejects_previous_example_even_when_mathematically_correct(self):
        old = M['load'](M['BASE'])
        with self.assertRaises(AssertionError):
            M['source_check'](old)
        fixed = M['load'](M['DEST'])
        M['source_check'](fixed)
        M['delta_check'](old, fixed)
        bad = copy.deepcopy(fixed)
        bad['scenes'][5]['art'][2]['value'] = old['scenes'][5]['art'][3]['value']
        with self.assertRaises(AssertionError):
            M['source_check'](bad)

    def test_rejects_omission_or_unrelated_change(self):
        fixed = M['load'](M['DEST'])
        bad = copy.deepcopy(fixed)
        bad['scenes'][5]['art'].pop(1)
        with self.assertRaises(AssertionError):
            M['source_check'](bad)
        bad = copy.deepcopy(fixed)
        bad['scenes'][0]['narration'] += ' Ajout.'
        with self.assertRaises(AssertionError):
            M['delta_check'](M['load'](M['BASE']), bad)


if __name__ == '__main__':
    unittest.main()
