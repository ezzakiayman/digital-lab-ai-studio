"""Source membership, approved wording and independent mathematical checks."""
import copy
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import runpy
import unittest

M = runpy.run_path('scripts/revise-n3-sem3-vdp4-v5.py')


class RealNumbersSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = M['load'](Path('src/video/n3-sem3-vdp4-v5-lesson.json'))

    def test_exact_voice_and_narrow_approvals(self):
        M['audit'](self.data)
        self.assertNotIn('Voici quelques nombres', self.data['scenes'][0]['narration'])
        self.assertIn('Ce nombre est l’abscisse de ce point.', self.data['scenes'][11]['narration'])
        bad = copy.deepcopy(self.data)
        bad['scenes'][11]['narration'] = bad['scenes'][11]['narration'].replace('Ce nombre est', 'Ce point est')
        with self.assertRaises(AssertionError):
            M['audit'](bad)

    def test_entire_visible_source_and_reject_extra_previous_example(self):
        M['visible_audit'](self.data)
        bad = copy.deepcopy(self.data)
        bad['scenes'][3]['art'][3]['value'] = bad['scenes'][3]['art'][3]['value'].replace('sont deux ', '')
        with self.assertRaises(AssertionError):
            M['visible_audit'](bad)
        bad = copy.deepcopy(self.data)
        bad['scenes'][8]['art'].append(copy.deepcopy(bad['scenes'][7]['art'][-1]))
        with self.assertRaises(AssertionError):
            M['visible_audit'](bad)

    def test_previous_integer_example_disappears_before_new_one(self):
        s = self.data['scenes'][9]
        boundary = s['beats'][4]['from']
        for v in s['art']:
            if '234' in v['value']:
                self.assertLessEqual(v['toFrame']+9, boundary)
        bad = copy.deepcopy(self.data)
        bad['scenes'][9]['art'][3]['toFrame'] = boundary
        with self.assertRaises(AssertionError):
            M['visible_audit'](bad)

    def test_independent_numeric_prefixes_and_rational_examples(self):
        self.assertEqual(Fraction(225,100), Fraction('2.25'))
        self.assertEqual(Fraction(45,63), Fraction(5,7))
        self.assertEqual(Fraction(234,1),234)
        self.assertEqual(Fraction(-87,1),-87)
        with localcontext() as ctx:
            ctx.prec = 50
            self.assertTrue(str(Decimal(7).sqrt()).startswith('2.64575131106'))
            self.assertTrue(str(Decimal(2).sqrt()).startswith('1.4142135623'))
            self.assertTrue(str(Decimal(5)/7).startswith('0.7142857142857'))
            def atan(x):
                total = Decimal(0)
                for k in range(100):
                    total += (-1 if k%2 else 1)*x**(2*k+1)/(2*k+1)
                return total
            pi = 16*atan(Decimal(1)/5)-4*atan(Decimal(1)/239)
            actual = M['semantic'](self.data['scenes'][8]['art'][3]['value']).split('=')[1].replace('…','').replace(',','.')
            self.assertTrue(str(pi).startswith(actual))
            self.assertFalse(str(pi).startswith('3.14159265359'))

    def test_band_edge_cases_and_native_words(self):
        rows = M['source_rows']()
        self.assertTrue(any(s['role']=='student' and s['text'].startswith('√2=') for s in rows[41]['shapes']))
        self.assertTrue(any(s['role']=='student' and s['text']=='-4' for s in rows[40]['shapes']))
        for i in [1,2]:
            p = self.data['scenes'][i]['pronunciation']
            self.assertEqual(''.join(p['syllables']),p['word'])
        self.assertFalse(any(v['kind']=='clip' for s in self.data['scenes'] for v in s['art']))


if __name__ == '__main__':
    unittest.main()
