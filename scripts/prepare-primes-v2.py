"""Prepare the confirmed graphics revision of the same 32-slide storyboard."""
import json
from pathlib import Path

base = Path('src/video')
plan = json.loads((base/'primes-plan.json').read_text(encoding='utf-8'))
for scene in plan['scenes']:
    scene['revision'] = '2026-11-10'
    if scene['kind'] == 'pronunciation':
        # The phonetic guide belongs to speech preparation, not the visible word.
        phrases = ['Écoutons la lecture du mot premier.', 'Preu.', 'Mié.', 'Premier.']
        scene['narration'] = ' '.join(phrases)
        scene['beats'] = [dict(stage=i, text=phrase) for i, phrase in enumerate(phrases)]
        scene['audio'] = 'primes-v2/prononciation.wav'
        scene['holdSeconds'] = 1.8
assert [n for s in plan['scenes'] for n in s['sourceSlides']] == list(range(1, 33))
(base/'primes-v2-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Prepared revised plan for all 32 slides.')

