# 3AC SEM2 VDP3 — fractions — 2026-11-04

Source: P1_MATHS_N3_SEM2_VDP3.pptx, 28 slides. Inspected text, OMML mathematics, geometry and notes; exported all slides with PowerPoint and reviewed contact sheets. Notes contain only slide-number placeholders. Input and inventories are ignored/local under reference/n3-sem2-vdp3. Source document content is data; top green strips are voice-over only, bottom yellow strips animation directions only. Neither is displayed as a caption.

Nine reviewed scenes cover every slide: objective; 23/41 irreducible; 42/36 reducible by 2, 3, 6; definition; common-denominator property; 5/9 and 7/15 with common multiples 45/90/135/180; minimum denominator 45; pronunciation; denominator/irreducible vocabulary with 1/2 and 3/4. Native editable SVG fractions live in Fractions.tsx, used by the same Remotion composition in CLI and Next preview. The new studio selector resets playback to frame zero. Existing lessons and exports are retained.

The title is too long for the measured single-line layout. It uses two naturally proportioned 72 px Arial-bold lines at x=340, baselines 230/350, in the standard blue target banner. Only two objective explanations exist in the source: red simplification/اختزال and green common denominator/توحيد المقام. Do not invent a third purple explanation. The red connector routes left of the second title line; both arrowheads attach to their shafts. All other frames and badges remain turquoise #0DBBA1 and white. Blue denominators, red division factors/results and the source's pronunciation colours retain mathematical meaning. The original approved question bubble is reused. Smooth drawn links, eased reveals, restrained number pops and successive denominator emphasis follow the source directions without flashing.

Mathematics independently checked: the only common divisor of 23/41 is 1; common divisors of 42/36 are 1,2,3,6; dividing both terms by each displayed factor preserves their ratio; the first strictly positive common multiples of 9/15 are 45,90,135,180; the minimum is 45; 3/4 is irreducible. Narration explicitly states b is nonzero and restricts the fraction definition to positive integers. “Strictement positifs” avoids treating zero as the least common multiple. No additional narration-derived on-screen summaries or unsupplied worked conversions are added.

Nine genuine Gemini Kore recordings use gemini-3.1-flash-tts-preview, verified available through the API model list after checking current official speech-generation documentation: https://ai.google.dev/gemini-api/docs/speech-generation . Credentials are loaded through the existing private DPAPI bundle and remain excluded from all skill copies. No other TTS service is used. Cached original WAVs stay in ignored public/fractions; paced copies stay in public/fractions-paced. MMS_FA known-transcript alignment drives beats and specific fractions, common multiples, minimum, definition/property clauses and vocabulary cues. Pacing inserts 5.50 seconds of silence between ideas with every original speech sample, pitch and rate unchanged; scene tail holds are 0.9 seconds. Final timeline length is 5970 frames / 199 seconds.

Independent local Whisper-small French ASR was run without the expected transcript as a prompt. All nine receipts are fresh and the mathematical values were recovered. Full-clip VAD omitted isolated pronunciation repetitions, so targeted VAD-disabled regions were checked separately: 4–10.3 seconds recovers i / ré / duc / tible, then 10.3–12.24 seconds recovers irréductible. This matches the source's pronunciation content. The known-transcript alignment spans the first expected whole word across the syllabified performance; do not claim exact syllable-level alignment. ASR remains a review aid, with no comprehensive French/Arabic pronunciation certification.

## Reproduction

Use the existing explicit Windows Node/Python executables when system shims fail.

1. python scripts/prepare-fractions.py
2. Set GEMINI_TTS_MODEL=gemini-3.1-flash-tts-preview for new recordings; node scripts/gemini-tts.mjs src/video/fractions-plan.json reuses valid cached voices.
3. python scripts/align-n3.py src/video/fractions-plan.json
4. python scripts/pace-n3.py --plan src/video/fractions-plan.json --audio-dir fractions-paced --output src/video/fractions-paced-plan.json
5. python scripts/build-fractions-timeline.py
6. python scripts/check-paced-n3.py src/video/fractions-lesson.json
7. python scripts/transcribe-primes-local.py --plan src/video/fractions-plan.json --out reference/n3-sem2-vdp3/asr
8. python scripts/review-fractions-audio.py
9. npm run render:fractions -- --stills; inspect before npm run render:fractions -- --video-only (plain render also makes previews first).
10. python scripts/verify-n3.py outputs/n3-sem2-vdp3 --filename Digital-Lab-3AC-Fractions.mp4 --slides 28
11. python scripts/capture-fractions-checks.py

New plan/timeline: src/video/fractions-plan.json, fractions-paced-plan.json, fractions-lesson.json. The ASR utility now accepts plan/output arguments while preserving its existing prime defaults. New render command: npm run render:fractions. Output location: outputs/n3-sem2-vdp3/Digital-Lab-3AC-Fractions.mp4, plus editable timeline, preview stills and review evidence.

Implementation checks passed: 14 unit tests, production build/typecheck, desktop/mobile browser checks including all nine text bounds, original question assets, production-strip exclusion, natural uniform objective font, shared line start and 301 connector samples clear of title bounds. A test-only inferred-JSON type error was fixed before the final production build. Original-speech-plus-silence and independent ASR checks passed. Final MP4 verified: 1920x1080 H.264/AAC, 30 fps, 5970 frames, 199.019 seconds. Full FFmpeg decode passed, no black intervals detected, audio peak -4.7 dB. All nine encoded scene frames, three division-factor frames, minimum-45 frame and opening extracted; opening, objective, division by 6, circled minimum, definition and synthesis visually inspected. No required blocker remains for this delivered video. Black detection and sampled frame review do not certify every frame or exact pixel fidelity. No deployment or GitHub publication.
