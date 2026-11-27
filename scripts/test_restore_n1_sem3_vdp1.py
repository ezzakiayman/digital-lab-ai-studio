"""Guard against the actual content changes identified in the source PPTX audit."""
import copy
import runpy
import unittest

restore = runpy.run_path('scripts/restore-n1-sem3-vdp1.py')


class SourceFidelity(unittest.TestCase):
    def setUp(self):
        self.rows, self.scenes = restore['prepared']()

    def test_all_23_source_bands_and_visible_definitions_are_accepted(self):
        restore['audit'](self.rows, self.scenes)
        self.assertEqual(sum(len(s['sourceSlides']) for s in self.scenes), 23)

    def test_old_rewritten_definition_is_rejected(self):
        scenes = copy.deepcopy(self.scenes)
        scenes[1]['narration'] = scenes[1]['narration'].replace(
            'Toute suite d’additions de nombres s’appelle : expression numérique',
            'Une suite d’additions de nombres est une expression numérique')
        with self.assertRaises(AssertionError):
            restore['audit'](self.rows, scenes)

    def test_removing_the_source_repetition_is_rejected(self):
        scenes = copy.deepcopy(self.scenes)
        scenes[0]['narration'] = scenes[0]['narration'].replace(
            'c’est une nouvelle notion c’est une nouvelle notion', 'c’est une nouvelle notion')
        with self.assertRaises(AssertionError):
            restore['audit'](self.rows, scenes)

    def test_adding_des_to_the_visible_terms_definition_is_rejected(self):
        scenes = copy.deepcopy(self.scenes)
        scenes[3]['art'][1]['value'] = 's’appellent des termes.'
        with self.assertRaises(AssertionError):
            restore['audit'](self.rows, scenes)


if __name__ == '__main__':
    unittest.main()
