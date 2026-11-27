"""Regression checks against previously observed source loss and unauthorized rewriting."""
import copy
import runpy
import unittest

MOD=runpy.run_path('scripts/revise-n3-sem3-vdp1-v5.py')


class SourceFidelity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=MOD['source_rows']()
        cls.data=MOD['load'](MOD['PLAN'])

    def test_math_radical_and_source_condition_survive_extraction(self):
        self.assertIn('√a',MOD['normalized'](self.rows[6]['voice']))
        main=' '.join(MOD['normalized'](s['text']) for s in self.rows[16]['shapes'] if s['role']=='student')
        self.assertIn('Pour tout nombre positif a',main)

    def test_refuses_previous_definition_rewrite(self):
        altered=copy.deepcopy(self.data)
        altered['scenes'][2]['narration']=altered['scenes'][2]['narration'].replace('nombre positif dont','nombre positif ou nul dont')
        with self.assertRaises(AssertionError): MOD['audit'](self.rows,altered)

    def test_refuses_silent_grammar_edit_or_omission(self):
        altered=copy.deepcopy(self.data)
        altered['scenes'][3]['narration']=altered['scenes'][3]['narration'].replace('je chercher','je cherche')
        with self.assertRaises(AssertionError): MOD['audit'](self.rows,altered)
        altered=copy.deepcopy(self.data)
        altered['scenes'][-1]['narration']='Le carré de la racine carrée de a est égal à a.'
        with self.assertRaises(AssertionError): MOD['audit'](self.rows,altered)

    def test_only_selected_lesson_native_fr_profile_and_approved_exceptions(self):
        MOD['audit'](self.rows,self.data)
        self.assertEqual(len(self.data['scenes']),9)
        self.assertEqual(self.data['scenes'][0]['beats'][1]['text'],'Reconnaître, c’est savoir.')
        for s in self.data['scenes']:
            self.assertTrue(s['id'].startswith('vdp1-'))
            self.assertEqual((s['languageCode'],s['speed'],s['stability']),('fr',.94,.45))


if __name__=='__main__':unittest.main()
