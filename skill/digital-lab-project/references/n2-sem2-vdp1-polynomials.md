# 2AC SEM2 VDP1 — binôme, trinôme et polynôme — 2026-11-05

Latest voice revision: [restored original Google TTS](n2-google-voice.md), now selected by the user. The ElevenLabs delivery described below is preserved as history.

Input: P1_MATHS_N2_SEM2_VDP1.pptx, 34 slides. Read text, geometry, OMML inventory and slide-number-only notes; exported every slide through PowerPoint and inspected all contact sheets, with full-size checks of rasterised equations. Much of this deck's narration/math is rasterised, so XML alone is insufficient. Source and review evidence remain ignored/local under reference/n2-sem2-vdp1.

## Objective discrepancy

The original opening promises “Déterminer le degré d’un polynôme”, while slides 5/15/25 define binôme/trinôme/polynôme and the examples count terms. No degree-calculation lesson appears. For example 5x+3y³ has two terms and total degree3: the operations are distinct. Flagged this to the user and supplied a French message for the professor. Offered original versus content-matched wording; the user asked for the explanation/message and then instructed completion, without explicitly selecting an objective. The working video uses the announced content-matched wording “Reconnaître un binôme, un trinôme et un polynôme”. Professor validation of that editorial choice is not claimed. Preserve the original deck. prepare-polynomials.py --keep-original-objective can reconstruct its original opening if later requested; it does not add a degree lesson to the rest of the content.

## New permanent user design rules

The full objective banner begins at the vertical centre of the screen, remains visible from frame zero while announced, then slides smoothly to the top and settles before keyword explanations. src/lib/presentation.ts supplies objectiveEntrance: the standard banner's centre y=265 is translated by275 to y=540 initially; the smoothstep transition runs for33frames, ending3frames before the first explanation beat. Existing older exports are preserved; this motion is used in the new lesson and saved for future work.

Every box header ends with a spaced colon: “Exemple :”, “Définition 1 :”, “Synthèse :”, vocabulary-card titles, etc. headingLabel normalises existing terminal colons and SectionHeader renders consistent turquoise badges. The objective's full sentence remains a title, not an extra colon-ended section label. All frames/badges retain #0DBBA1/white. Source yellow/blue expression highlights and blue/green/purple mathematical terms remain semantic content within those frames.

The objective uses uniform natural72px Arial bold, blue outline/shadow and original target. Two lines share x=340; explained concepts lie on the second line and link to columns480/960/1440 in fixed red/green/purple order. Measured word positions keep ordinary French spacing and no gap before the comma: binôme448, trinôme852, polynôme1328. Active words use the arrow colour and a subtle highlight. The source's main concepts are reused in the edited opening; no extra degree explanation is invented.

## Scenes and mathematics

Thirteen scenes cover every source slide: objective1–3; binomial definition4–5; positive example6–9; negative example10–13; trinomial definition14–15; positive example16–19; negative example20–23; polynomial definition24–25; four-term example26–27; pronunciation28/29; synthesis30–33; final vocabulary34. Shared Remotion composition, Zod schema, editable plan/paced-plan/final timeline, Next selector and named renderer are implemented. All top green voice strips/bottom animation directions remain absent from learner-facing captions. Source read-aloud questions are not typed.

Examples checked: 5x+3y³ has2 unlike terms; x+2y+1 has3 and is not binomial; 2x²+4y−1 has3; x−3y has2 and is not trinomial; x³y²+xy³−x³+5 has4 distinct terms. Synthesis 2x+5y−4 has3; x+y−2z+1 has4. reducedTermCount combines equal exponent triples before counting nonzero coefficients; independent pairwise exponent checks and reduction/cancellation cases test the examples. No zero-polynomial degree claim is introduced.

Native editable expressions use Cambria Math for mathematical glyphs and Arial for teaching text. Source semantic colours preserved. Red circles draw/fade around the full signed term, then retire before the next; the negative sign belongs to −3y/−1. Arrows, counts, checks/crosses and classification labels follow the narrated stages. Definitions subtly emphasise the spoken keyword and term count. Synthesis keeps all three columns and source examples visible for review.

## Previous narration revision: ElevenLabs override (superseded by Google restoration)

The user supplied an ElevenLabs key and voice ID and explicitly requested completion with that voice, superseding Gemini for this lesson. All13 final recordings use voice e1kzF2oNiC1xDfUP7Yxo and eleven_multilingual_v2, stability0.65/similarity0.75/style0/speed1/speaker boost. The voice endpoint confirmed availability. The key is stored only in the installed skill's ignored private/elevenlabs-key.dpapi or supplied via process ELEVENLABS_API_KEY; it is never in source, docs, skill copies or transfer media. ELEVENLABS_VOICE_ID / ELEVENLABS_MODEL override the public settings. The current API instructions were checked at https://elevenlabs.io/docs/api-reference/text-to-speech/convert .

scripts/elevenlabs-tts.mjs sends xi-api-key in a header, redacts errors, bounds transient retries and caches by text/voice/model/settings. Original mp3_44100_128 responses decode to mono24kHz PCM WAV for the existing alignment/pacing pipeline. Cache-compatible clips resume without generation. Existing Gemini attempts stay separate under ignored public/polynomials and reference review copies; the final timeline contains only polynomials-elevenlabs-paced audio. Earlier Gemini daily quota/connection failures do not justify further quota retries. No Higgsfield call was made.

Independent Whisper-small ASR flagged isolated-variable ambiguity. French spoken names are now explicit: ix, i grec, zède. Six math clips were regenerated; one repeated binomial conclusion was subsequently shortened to “cette expression” after a remaining ASR disagreement. Original audio and review findings are preserved locally and are not treated as proven voice mistakes. All13 final ASR receipts are fresh, without expected-transcript prompts; semantic checks recover reviewed coefficients, exponents, term counts/classifications and synthesis examples. ASR remains a review aid, not a comprehensive pronunciation certificate.

MMS_FA aligns the final13 original WAVs. Paced copies add12.28seconds of silence at inter-idea gaps; every original decoded PCM speech sample, pitch and rate is preserved. Scene holds are normally0.9seconds,2seconds for synthesis/final vocabulary. Final timeline:6857frames,228.5667seconds before AAC padding. This replaces the timing of the earlier Gemini and initial ElevenLabs clips.

## Commands

```text
python scripts/prepare-polynomials.py --elevenlabs
node scripts/elevenlabs-tts.mjs --probe
node scripts/elevenlabs-tts.mjs src/video/polynomials-plan.json
python scripts/align-n3.py src/video/polynomials-plan.json
python scripts/pace-n3.py --plan src/video/polynomials-plan.json --audio-dir polynomials-elevenlabs-paced --output src/video/polynomials-paced-plan.json
python scripts/build-polynomials-timeline.py
python scripts/check-paced-n3.py src/video/polynomials-lesson.json
python scripts/transcribe-primes-local.py --plan src/video/polynomials-plan.json --out reference/n2-sem2-vdp1/asr-elevenlabs
python scripts/review-polynomials-audio.py
npm run render:polynomials -- --elevenlabs --stills
npm run render:polynomials -- --elevenlabs --video-only
python scripts/verify-n3.py outputs/n2-sem2-vdp1 --filename P1_MATHS_N2_SEM2_VDP1.mp4 --slides 34
python scripts/capture-polynomials-checks.py
```

For visual-only corrections reuse the final timeline/voices and skip preparation/TTS/retiming. --objective-only updates just objective previews. Google/Gemini is now the default again after the user’s clarification. Use --elevenlabs only to deliberately reproduce this historical voice variant. Verification now derives provider/voice from receipts rather than hard-coding Gemini/Kore.

Output: outputs/n2-sem2-vdp1/P1_MATHS_N2_SEM2_VDP1.mp4, with editable timeline.json and audio-review.json. Seventeen tests, production build/typecheck, desktop/mobile browser checks for all13 scenes, centred initial objective,72px type, colon-ended headers, text bounds and supplied-voice audio paths passed. All scene previews and key objective/term/synthesis stills visually inspected. PCM-preservation and independent-ASR checks passed. Final MP4 verified:1920x1080 H.264/AAC,30fps,6857frames,228.587seconds. All34 source slides covered. Full FFmpeg decode passed, no black intervals detected, audio peak−5.2dB. All13 encoded final scenes, centred/moving/top objective states and signed-term checkpoints captured; actual encoded objective motion, the −1 term highlight and synthesis visually inspected. No rendering blocker remains. The edited objective still awaits professor validation, as noted above.

The earlier transfer ZIP is a historical snapshot and is not silently refreshed by this lesson. Relevant installed/source/matching local project skills are maintained separately. No production deployment or GitHub publication. General AI storyboard interpretation, Manim workers, durable job queues and comprehensive pronunciation/pixel-fidelity certification remain pending.


Earlier TTS interpretation, 2026-11-05 (superseded by the later Google-specific clarification): preserve the approved animation style demonstrated by the completed 2AC polynomial video and use text-to-speech (TTS) for voice-over. The delivered narration already uses ElevenLabs TTS with the supplied voice. “Use TTS” is a synthesis-method preference, not a request to switch providers or regenerate unchanged audio. Retain the selected voice/provider unless the user changes them. Animation approval does not resolve the separately flagged objective wording/professor review.
