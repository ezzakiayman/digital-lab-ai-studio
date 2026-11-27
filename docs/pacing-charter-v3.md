# Pacing and fixed charter — revision 3

Typography update, 2026-11-03: v3's mixed 72/64 px below is superseded by uniform 72 px Arial bold with natural glyph proportions. See [objective typography v4](objective-typography-v4.md).

User's latest permanent rules supersede the earlier interpretation of different source chapter-box colours. All pedagogical frames and heading badges now use example/verification turquoise #0DBBA1 with white bodies, centralized in src/lib/charter.ts. Mathematical colours remain meaningful; the blue objective banner remains unchanged in identity.

Objective title increased from 42 px to 72 px for its first line and 64 px for its second. The current phrase is coloured and softly highlighted in its arrow colour. Reflow keeps all title text visible and avoids connector/text crossings: the second connector uses a smooth elbow around the lower title line. Original target/dart asset, border, shadow and explanation order remain.

The acronym scene now displays individual P/P/C/M letters. Each highlighted letter gently scales, its arrow starts directly beneath it, and its corresponding word appears on the spoken word cue. The word initial uses the same colour. This is saved as a general acronym-teaching rule in both installed skills. Number/equation pop-ins use restrained 0.94→1.025→1 scaling with a fade rather than a large bounce.

Audio: scripts/pace-n3.py adds zero-valued PCM samples only in aligned gaps between ideas. Speech rate and pitch are untouched. It targets short 0.85–1.0 s reflection gaps, adds at least 0.25 s when a gap is short, and leaves gaps already ≥1.2 s alone. Across fifteen scenes, 6.18 s was inserted inside narration. Scene holds increased from 0.45 to 0.9 s. scripts/check-paced-n3.py verifies that every speech sample is unchanged and only inserted silence separates the original chunks. Original Gemini recordings remain under public/n3; paced copies/alignment/receipts are under ignored public/n3-paced.

The waveform edits shift the cached known-transcript word intervals by exact inserted durations. The paced scene builder then rebuilds all word/beat cues. No new Gemini generation or re-alignment is needed. Confidence limitations of the original alignment still apply; this is not independent speech-content verification.

Reproduce:

1. `python scripts/pace-n3.py`
2. `python scripts/build-n3-timeline.py --paced`
3. `python scripts/check-paced-n3.py`
4. `npm run render:n3 -- --v3`
5. `python scripts/verify-n3.py outputs/n3-v3`

Output is under outputs/n3-v3, preserving v1/v2 exports. Current timeline represents 217.6 seconds. Check project handoff for final export verification. No new narration, added music/captions, deployment or GitHub publication in this revision.
