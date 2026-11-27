# Four storyboard exports — 2026-11-10

| Input | Scenes | Output directory | Timeline stem |
| --- | ---: | --- | --- |
| P1_MATHS_N2_SEM2_VDP2 (3).pptx, 27 slides | 7 | outputs/n2-sem2-vdp2 | like-terms |
| P1_MATHS_N3_SEM2_VDP2 (1).pptx, 13 slides | 5 | outputs/n3-sem2-vdp2-2026-11-10 | factorization-v2 |
| P1_MATHS_N3_SEM2_VDP3 (1).pptx, 28 slides | 9 | outputs/n3-sem2-vdp3-2026-11-10 | fractions-v2 |
| P1_MATHS_N2_SEM2_VM4.pptx, 47 slides | 8 | outputs/n2-sem2-vm4 | polynomial-subtraction |

All decks were exported through PowerPoint in read-only mode. The two 3AC inputs match their previously reviewed decks byte for byte. Their new exports use the latest title, arrow, box and pronunciation rules, with separate timelines and output folders. The source decks, slide images and narration review remain under ignored reference folders. Production strips supply audio and animation cues.

## Editorial and mathematical review

- The 27-slide 2AC VDP2 deck teaches reduction by grouping like terms. It opens with 2𝒙 + 8𝒙 = 10𝒙 and distinguishes 2𝒙³ from 8𝒙. The main example expands 5𝒙𝒚 and 4𝒙𝒚 to show that each variable has exponent 1. Slides 14 and 20 contain inconsistent superscripts. The rendered counterexample uses the worked pair 𝒙³𝒚 and 𝒙²𝒚 consistently and shows 3 ≠ 2. On slide 26 the audio text says 7y and the learner illustration says 7x. The voice and recap both use 3𝒙 and 7𝒙, a valid pair of like terms. Semblables is split into two spoken syllables, sem–blables, with the final written e silent.
- Prime factorisation keeps the uniqueness qualifier « à l’ordre des facteurs près » and the products of 360 and 72. Pending factors remain ellipses until their spoken cue, with multiplication signs visible. The vocabulary segment builds dé–com–po–si–tion before reading the whole word.
- Fractions retains the 23/41 and 42/36 examples, reductions by 2, 3 and 6, and the positive common multiples 45, 90, 135 and 180. It highlights 45 as the least common denominator for 5/9 and 7/15. The approved question asset remains in both question stages. The vocabulary segment displays ir–ré–duc–tible over the spoken syllables. Encoded review caught the missing second r from the initial i–ré split. The adjusted written split restores both r letters in the joined word.
- VM4 teaches both methods for (8𝒙 + 7𝒚) − (6𝒙 + 4𝒚). The horizontal method adds the opposite, removes parentheses, groups like terms and calculates. The vertical method places −6𝒙 − 4𝒚 beneath 8𝒙 + 7𝒚 and aligns variables in columns. Several source diagrams in slides 36–39 switch operands and partial results. The video keeps the original operands and shows 8 − 6 = 2 and 7 − 4 = 3 in the respective columns, so both methods yield 2𝒙 + 3𝒚. A pending value uses an ellipsis and the task preview reuses the approved question artwork.

## Shared presentation and narration

The new objective component measures one-line navy titles in Arial Bold and attaches the vertical link at each underline’s midpoint. Banner sizes are 54 px for like terms, 56 px for factorisation, 47 px for fractions and 64 px for subtraction. All open in the centre. The badge and frame ease into position before the teaching elements, and headings use the spaced colon. Professional math type uses upright digits, positioned exponents, neutral operators and dedicated Cambria Math bold italic 𝒙 and 𝒚. This is the glyph correction requested during the batch. The logical equations remain ASCII-variable data for editing and checks.

All narration uses Google Kore. Like terms and the three new pronunciation clips use the existing Gemini 3.1 workflow. The four reused factorisation clips and eight reused fractions clips match the earlier source narration. VM4 uses Gemini 3.8 Flash Lite TTS. That model spoke the legacy instructions before the lesson in the initial clips. The cleaned audio removes those prefixes at independently located speech boundaries and retains the lesson samples. The vertical sign-change clip was regenerated from transcript-only input with a clearer reading of y. The optional scene field `speechMode: "verbatim"` keeps that cache distinct. Independent Whisper review recovered the operands, signs, result and cleared the instruction-prefix check on all final 2AC clips. The review of isolated syllables used bounded regions and verified voiced energy in every aligned interval. Short nonword ASR results can be ambiguous, including on décomposition. Timings use MMS_FA separately from recognition.

## Reproduction

- Prepare the plans with `python scripts/prepare-vdp2.py` and `python scripts/prepare-fractions-subtraction.py`.
- Reuse the reviewed audio when editing visuals. Generate changed lines with `scripts/gemini-tts.mjs` and the scene plan. For fresh 3.8 Flash Lite audio, inspect the transcript for spoken instructions before alignment. The trim tool accepts the VM plan and a private raw-voice archive path. Preserve the raw audio and recheck the trimmed clips independently.
- Run `scripts/align-n3.py` and `scripts/pace-n3.py` for each stem. Use the corresponding stem with a `-paced` audio directory. Build the revised factorisation and fractions timelines with `--revised`. Run `scripts/build-algebra-vdp2-timeline.py` with each of the two algebra stems.
- Run `python scripts/check-storyboard-batch.py`, then `npm run render:storyboards -- --stills`. For an algebra glyph proof only, add `--math-proof like-terms polynomial-subtraction`.
- Render with `npm run render:storyboards`. Pass specific timeline stems to render a subset. Use `python scripts/verify-storyboard-batch.py` with the same stems for full decode and checkpoint extraction.


## Verified exports

| Lesson | Duration | Frames | Audio peak | MP4 |
| --- | ---: | ---: | ---: | --- |
| 2AC VDP2 | 181.376 s | 5,441 | -4.4 dB | outputs/n2-sem2-vdp2/P1_MATHS_N2_SEM2_VDP2.mp4 |
| 3AC VDP2 | 105.067 s | 3,152 | -4.6 dB | outputs/n3-sem2-vdp2-2026-11-10/P1_MATHS_N3_SEM2_VDP2.mp4 |
| 3AC VDP3 | 198.912 s | 5,967 | -4.7 dB | outputs/n3-sem2-vdp3-2026-11-10/P1_MATHS_N3_SEM2_VDP3.mp4 |
| 2AC VM4 | 211.733 s | 6,352 | -4.2 dB | outputs/n2-sem2-vm4/P1_MATHS_N2_SEM2_VM4.mp4 |

All four are 1920 × 1080 at 30 fps with H.264/AAC and Google Kore. Full decode passed with no unexpected black intervals. The final timelines, verification receipts and encoded checkpoint images are alongside the MP4s. The batch covers 115 source slides in 29 scenes. The 18 unit tests, production build and desktop and mobile studio checks passed. Independent checks covered source order, arithmetic, narration samples, exact variable glyphs, straight arrow joins, scene text bounds, colon headings and joined vocabulary spelling. Inspected the encoded algebra glyphs, vertical and horizontal results, pending factor placeholder, fraction result and the corrected joined word irréductible.
