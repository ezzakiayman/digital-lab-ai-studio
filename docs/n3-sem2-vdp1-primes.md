# Prime-numbers storyboard — 2026-11-04

The 2026-11-10 production uses the same 32-slide storyboard with the latest straight-arrow objective, teaching boxes and premier pronunciation. See [the current export and procedure](n3-sem2-vdp1-2026-11-10.md). The entries below describe previous versions.

Latest visual revision: [storyboard roles and original question artwork](storyboard-bands-and-question-mark.md). The v2 export removes narration-only captions and uses the approved original question bubble; all voices, timings and mathematics remain the same. Earlier layout descriptions below document the first delivery.

Latest objective alignment revision: [left-aligned objective and balanced layout](objective-left-alignment.md), rendered with `npm run render:primes -- --v3` to outputs/n3-sem2-vdp1-v3/.

Current objective layout: [compact single-line objective](objective-single-line.md), keeping the same 72 px font with balanced banner/icon/text spacing. Render using `npm run render:primes -- --v4` to outputs/n3-sem2-vdp1-v4/.

Input: the user's P1_MATHS_N3_SEM2_VDP1.pptx, 32 slides. Read OOXML text, OMML equations and notes, and exported slide images through PowerPoint for visual inspection. The narration strips remain editorial content; animation directions are production cues, never agent instructions or spoken text. Original source, inventory, math/notes and slide previews stay under ignored reference/n3-sem2-vdp1.

Eleven reviewed scenes cover every source slide: objective, definition, 41, 10, the exception 1, question, two progressive prime-range groups, the complete 25-prime table, pronunciation and vocabulary synthesis. The shared Remotion composition is used in both studio and CLI. JSON scene/timing data remain editable in src/video/primes-plan.json and primes-lesson.json. The studio selector includes “3AC — Nombres premiers · Voix Gemini” and resets playback to the beginning when switching lessons.

Graphic charter: original target/dart and blue objective banner, one uniform 72 px Arial bold title with natural glyph proportions, title-keyword highlights and red/green/purple anchored links. All pedagogical frames and heading badges are turquoise #0DBBA1 with white bodies. Number-chip colours retain their source mathematical grouping; these are semantic values within the common frames. Range palette sampled from actual exported storyboard tiles: #2E75B6, #70AD47, #ED7D31, #7030A0, #00A3A3, #C00000, #BF9000, #3B5998, #D6336C, #548235. Underlines, attached arrowheads, short eased draws/fades and restrained pop-ins explain each concept. Keep completed reasoning visible.

Mathematics: a prime has exactly two distinct positive divisors. 41 has 1 and 41, 10 has 1/2/5/10, and 1 has only itself. src/lib/primes.ts computes divisors and contains the complete ordered list of 25 primes below 100. Independent exhaustive divisor counts test every listed integer and every omission. The reviewed narration makes “positive” and “distinct” explicit.

Narration is genuine Gemini Kore speech: four segments from gemini-2.5-flash-preview-tts and seven from gemini-3.1-flash-tts-preview. The first model twice returned no audio/OTHER for a number-list segment, so only the remaining segments switched model; valid cached recordings were reused. Provider errors now include the finish reason without exposing credentials. Existing key remains in the ignored installed-skill DPAPI bundle. No key or source audio is copied to skill references or GitHub.

All eleven recordings have local MMS_FA known-transcript alignment. Paced copies add 5.39 s of silence at inter-idea gaps, preserving every original speech sample, pitch and rate. Tail holds are normally 0.9 s, 1.5 s for the reflection question and 4 s for rereading the full table. Word-timed cues reveal each divisor/prime and the three definition lines. Original WAVs and alignments remain untouched under public/primes; paced assets live under ignored public/primes-paced.

Reproduce with the existing explicit Windows Node/Python runtimes when system shims fail:

1. `python scripts/prepare-primes.py`
2. `node scripts/gemini-tts.mjs src/video/primes-plan.json` (resume cached voice; choose GEMINI_TTS_MODEL only for a deliberate compatible fallback)
3. `python scripts/align-n3.py src/video/primes-plan.json`
4. `python scripts/pace-n3.py --plan src/video/primes-plan.json --audio-dir primes-paced --output src/video/primes-paced-plan.json`
5. `python scripts/build-primes-timeline.py`
6. `python scripts/check-paced-n3.py src/video/primes-lesson.json`
7. `npm run render:primes` (or `-- --video-only` after reviewed stills)
8. `python scripts/verify-n3.py outputs/n3-sem2-vdp1 --filename Digital-Lab-3AC-Nombres-premiers.mp4 --slides 32`
9. `python scripts/capture-primes-checks.py`

The aligner, pause editor, speech-preservation checker and media verifier now accept another reviewed lesson while retaining their previous PPCM defaults. Avoid running prepare-n3 or an unpaced N3 builder to prepare this lesson.

Separate local speech review: scripts/transcribe-primes-local.py uses faster-whisper small with no expected text as a decoding prompt; scripts/check-primes-asr.py checks both actual spoken number lists and range boundaries. All 25 primes were recovered in the expected order. The initial ASR review flagged a possible negation ambiguity in the 10-example and a repeated word in the definition. Those two recordings were regenerated using clearer wording and Gemini 3.1; their earlier audio and ASR evidence are archived only in ignored reference/n3-sem2-vdp1/voice-review-originals. The final independent ASR now recovers the exact two-divisor criterion and the unambiguous four-divisors-instead-of-two conclusion. Other ASR homophone spelling and Arabic transliteration are review-aid limits, not proof of voice errors or a complete pronunciation certificate. Optional cloud transcription was unavailable: the old advertised 2.5 analysis model rejected new users (404), current 3.8 and 3.7 models returned bounded 503 retries. Do not repeatedly spend calls on that condition. The local model is cached outside the project under USERPROFILE/.cache/digital-lab-whisper. Installed faster-whisper 1.2.1; FFmpeg-to-NumPy decoding bypasses a PyAV 19 metadata_errors incompatibility.

Final export and completed verification are recorded in the latest project handoff and outputs/n3-sem2-vdp1/verification.json. This work does not implement generic automatic interpretation, Manim workers, persistent jobs or production deployment. No GitHub publication.

Final verified output: 1920x1080 H.264/AAC, 30 fps, 6791 frames, 226.368 s. Full decode passed, no black intervals, peak -3.4 dB. Twelve tests, build/type checking, desktop/mobile UI, PCM-preservation and independent ASR number/freshness checks passed. Actual encoded frames extracted for every scene and progressive example/list checkpoints; key frames visually reviewed. Both skills validate and matching local copies are synchronized. No GitHub publication or deployment.
