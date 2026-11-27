"""Fidelity and arithmetic regressions for the approved decimal-fraction revision."""
import copy
from fractions import Fraction
from pathlib import Path
import runpy
import unittest

M=runpy.run_path('scripts/revise-n3-sem3-vdp3-v5.py')


class DecimalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=M['load'](Path('src/video/n3-sem3-vdp3-v5-lesson.json'))

    def test_source_words_and_precise_negative_fraction_approval(self):
        M['audit'](self.data)
        self.assertIn('moins cinq sur dix à la puissance zéro',self.data['scenes'][6]['narration'])
        bad=copy.deepcopy(self.data)
        bad['scenes'][6]['narration']=bad['scenes'][6]['narration'].replace('moins cinq sur dix à la puissance zéro','un sur dix à la puissance trois')
        with self.assertRaises(AssertionError):M['audit'](bad)
        bad=copy.deepcopy(self.data);bad['scenes'][9]['narration']='Reprenons les mots de cette séance.'
        with self.assertRaises(AssertionError):M['audit'](bad)

    def test_entire_visible_sentences_and_equations(self):
        M['visible_audit'](self.data)
        bad=copy.deepcopy(self.data);bad['scenes'][7]['art'][1]['value']=bad['scenes'][7]['art'][1]['value'].replace('s’écrit ','')
        with self.assertRaises(AssertionError):M['visible_audit'](bad)
        bad=copy.deepcopy(self.data);bad['scenes'][5]['art'][2]['value']=bad['scenes'][5]['art'][2]['value'].replace('001','01')
        with self.assertRaises(AssertionError):M['visible_audit'](bad)

    def test_math_correctness_and_no_premature_false_equality(self):
        self.assertEqual(Fraction(225,10**2),Fraction('2.25'))
        self.assertEqual(Fraction(1,10**3),Fraction('0.001'))
        self.assertEqual(Fraction(-5,10**0),-5)
        self.assertEqual(Fraction(2985,1000),Fraction('2.985'))
        self.assertEqual(Fraction(2985,10**3),Fraction('2.985'))
        stages=self.data['scenes'][4]['art']
        self.assertEqual(stages[2]['value'],'225')
        self.assertEqual(stages[0]['toFrame'],stages[-1]['frame'])
        self.assertEqual(stages[0]['x'],stages[-1]['x'])

    def test_native_words_and_shared_equation_columns(self):
        for n,word in [(1,'Illimité'),(2,'Périodique')]:
            p=self.data['scenes'][n]['pronunciation'];self.assertEqual(''.join(p['syllables']),word)
            self.assertEqual(p['style'],'simplifier')
        self.assertFalse(any(v['kind']=='clip' for s in self.data['scenes'] for v in s['art']))
        rows=self.data['scenes'][5]['art'][2:]
        self.assertEqual(rows[0]['x'],rows[1]['x']);self.assertEqual(rows[0]['size'],rows[1]['size'])
        self.assertIn('=',rows[0]['value']);self.assertIn('=',rows[1]['value'])


if __name__=='__main__':unittest.main()
