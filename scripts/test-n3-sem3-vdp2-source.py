"""Reject the previous narration rewrites, missing visible words and altered comparisons."""
import copy
from pathlib import Path
import runpy
import unittest

M=runpy.run_path('scripts/revise-n3-sem3-vdp2-v5.py')


class ComparisonSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=M['load'](M['PLAN'])
        cls.data=M['load'](Path('src/video/n3-sem3-vdp2-v5-lesson.json'))
        cls.spelling=M['load'](M['OUT']/'visible-source-audit.json')['spellingCorrectionExplicitlyApproved']

    def test_source_voice_and_only_documented_exceptions(self):
        M['audit'](self.plan)
        self.assertEqual(len(self.plan['scenes']),6)
        self.assertEqual(self.plan['scenes'][1]['beats'][0]['text'],
                         'Avant de passer à la propriété de cette séance écoutons d’abord la lecture du mot : Comparer.')
        for s in self.plan['scenes']:
            self.assertEqual((s['languageCode'],s['speed'],s['stability']),('fr',.94,.45))

    def test_previous_unapproved_voice_rewrites_fail(self):
        bad=copy.deepcopy(self.plan)
        bad['scenes'][2]['narration']=bad['scenes'][2]['narration'].replace('nombres positifs','nombres positifs ou nuls')
        with self.assertRaises(AssertionError):M['audit'](bad)
        bad=copy.deepcopy(self.plan)
        bad['scenes'][-1]['narration']='Voici les expressions de cette séance.'
        with self.assertRaises(AssertionError):M['audit'](bad)

    def test_complete_property_words_and_signs_are_checked_separately(self):
        M['visible_audit'](self.data,self.spelling)
        bad=copy.deepcopy(self.data)
        bad['scenes'][2]['art'][2]['value']=bad['scenes'][2]['art'][2]['value'].replace('alors ','')
        with self.assertRaises(AssertionError):M['visible_audit'](bad,self.spelling)
        bad=copy.deepcopy(self.data)
        bad['scenes'][3]['art'][1]['value']='>'
        with self.assertRaises(AssertionError):M['visible_audit'](bad,self.spelling)

    def test_native_pronunciation_and_domain_error_are_unambiguous(self):
        pron=self.data['scenes'][1]
        self.assertEqual(''.join(pron['pronunciation']['syllables']),'Comparer')
        self.assertEqual(pron['pronunciation']['style'],'simplifier')
        self.assertFalse(any(v['kind']=='clip' for s in self.data['scenes'] for v in s['art']))
        marker=self.data['scenes'][4]['art'][-1]
        self.assertEqual((marker['kind'],marker['value'],marker['at']),('status','Faux',2))
        self.assertTrue(marker['repeatPulse'])


if __name__=='__main__':unittest.main()
