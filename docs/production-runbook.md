# Digital Lab — production runbook for another Codex agent

Read the [video production knowledge base](../skill/digital-lab-project/references/video-production-knowledge.md) before production or revision. It links the current rules to verified examples and records how to carry each new correction into future work.

## Contents

Environment and credentials · Existing lesson entry points · New-storyboard production · Graphic contract · Voice and timing · QA and delivery · Known limits

## Environment and credentials

Use this folder as cwd. `npm ci` restores package-lock.json; do not replace dependencies with today's latest versions just because package.json contains “latest”. Tested Node 22.18.0 and Python 3.12. FFmpeg/ffprobe must be on PATH. The existing renders require Arial with the saved metrics; Windows is the verified environment. Do not bundle or redistribute Windows fonts without an appropriate licence. Linux/macOS operation and alternate-font fidelity have not been certified.

For new speech/alignment/ASR, use a dedicated Python environment and `python -m pip install -r requirements-video.txt`. The snapshot records torch/torchaudio 2.8.0 (matching versions), uroman, NumPy/Pillow and faster-whisper. The original workstation uses CUDA 12.6 wheels; CUDA is optional and not bundled. MMS_FA/Whisper model weights download/cache separately. CPU processing works in the scripts but can be slower. Run `node scripts/doctor.mjs --full --python <executable>` and inspect any failure. PowerPoint desktop is optional for existing renders, required for scripts/export-storyboard.ps1. Its source deck is opened read-only.

Rendering cached narration requires no API credential and no speech API calls. New voice reads process GEMINI_API_KEY first. On the original Windows profile, the provider can also use the existing ignored ~/.codex/skills/digital-lab-project/private/gemini-key.dpapi (CODEX_HOME supported). That encrypted bundle is not transferable to another user/machine and is never packaged. Optional GEMINI_POWERSHELL_EXE selects a local Windows decryption executable. Never put keys in prompts, .env examples, receipts, source, skill files, query URLs or logs. No credential change is required to review/render the included lessons.

The TTS provider uses x-goog-api-key, redacts errors, resumes cached valid WAVs and applies bounded retries. Model availability and quotas change: read current primary Gemini speech documentation and `node scripts/gemini-tts.mjs --probe` before selecting a model. Last verified fractions model: gemini-3.1-flash-tts-preview, voice Kore. Do not repeatedly retry daily quota exhaustion or a rejected/unavailable model. Resume compatible cached clips instead of regenerating an entire lesson. See https://ai.google.dev/gemini-api/docs/speech-generation for current provider instructions.

## Existing lesson entry points

| Lesson | Timeline | Render | Verification |
| --- | --- | --- | --- |
| N1 comparison | src/video/full-lesson.json | npm run render:full | python scripts/verify-full.py |
| N3 PPCM | src/video/n3-lesson.json | npm run render:n3 -- --v4 | python scripts/verify-n3.py outputs/n3-v4 --slides 39 |
| N3 primes SEM2 VDP1 | src/video/primes-lesson.json | npm run render:primes -- --v4 | python scripts/verify-n3.py outputs/n3-sem2-vdp1-v4 --filename Digital-Lab-3AC-Nombres-premiers.mp4 --slides 32 |
| N3 primes SEM2 VDP1, November 10 revision | src/video/primes-v2-lesson.json | npm run render:primes -- --revised | python scripts/verify-n3.py outputs/n3-sem2-vdp1-2026-11-10 --filename P1_MATHS_N3_SEM2_VDP1.mp4 --slides 32 |
| N3 primes SEM2 VDP1, November 12 revision | src/video/primes-review-lesson.json | npm run render:primes -- --review --video-only | python scripts/verify-n3.py outputs/n3-sem2-vdp1-2026-11-12 --filename P1_MATHS_N3_SEM2_VDP1.mp4 --slides 32 |
| N3 factorisation SEM2 VDP2, November 12 revision | src/video/factorization-review-lesson.json | npm run render:storyboards -- factorization-review | python scripts/verify-storyboard-batch.py factorization-review |
| N3 fractions SEM2 VDP3, November 12 revision | src/video/fractions-review-lesson.json | npm run render:storyboards -- fractions-review | python scripts/verify-storyboard-batch.py fractions-review |
| N3 fractions SEM2 VDP3 | src/video/fractions-lesson.json | npm run render:fractions | python scripts/verify-n3.py outputs/n3-sem2-vdp3 --filename Digital-Lab-3AC-Fractions.mp4 --slides 28 |
| 2AC polynomials SEM2 VDP1, revised 55 slides | src/video/polynomials-v2-lesson.json | npm run render:polynomials -- --revised | python scripts/verify-n3.py outputs/n2-sem2-vdp1-2026-11-10 --filename P1_MATHS_N2_SEM2_VDP1.mp4 --slides 55 |
| Four-storyboard batch, 2AC VDP2 and VM4, 3AC VDP2 and VDP3 | See docs/four-storyboards-2026-11-10.md | npm run render:storyboards | python scripts/verify-storyboard-batch.py |

Prime/PPCM delivered MP4s were later renamed to P1_MATHS_N3_SEM2_VDP1.mp4 and P1_MATHS_N3_SEM1_VDP4.mp4. This is an observed filename change, not a newly certified media edit. Pass the actual name through --filename when verifying those packaged copies; new renders use the renderer's original filename. TRANSFER_MANIFEST.json maps source files and hashes. Existing verification reports are historical evidence; never pass them off as fresh checks of a changed file.

For the fractions example, the complete pipeline is:

```text
python scripts/prepare-fractions.py
node scripts/gemini-tts.mjs src/video/fractions-plan.json
python scripts/align-n3.py src/video/fractions-plan.json
python scripts/pace-n3.py --plan src/video/fractions-plan.json --audio-dir fractions-paced --output src/video/fractions-paced-plan.json
python scripts/build-fractions-timeline.py
python scripts/check-paced-n3.py src/video/fractions-lesson.json
python scripts/transcribe-primes-local.py --plan src/video/fractions-plan.json --out reference/n3-sem2-vdp3/asr
python scripts/review-fractions-audio.py
npm run render:fractions -- --stills
npm run render:fractions -- --video-only
python scripts/verify-n3.py outputs/n3-sem2-vdp3 --filename Digital-Lab-3AC-Fractions.mp4 --slides 28
python scripts/capture-fractions-checks.py
```

Set GEMINI_TTS_MODEL deliberately for newly generated clips after probing; the TTS command reuses valid cached recordings from a compatible earlier model. For visual-only edits skip preparation/TTS/alignment/pacing and render the existing final timeline directly. The prepare scripts reconstruct the reviewed canonical plans and can overwrite hand-edited plan fields, so inspect user edits before running them. Separate lesson docs contain the exact PPCM/prime commands. Legacy comparison-image helpers assume Windows fonts and may still use original-workstation paths; they are optional historical review utilities, not portable production dependencies.

For sequential batch rendering of prepared timelines, select a fresh output directory:

```text
npm run render -- --out=outputs/batch-review src/video/fractions-lesson.json src/video/primes-lesson.json
```

The generic CLI reuses a Remotion bundle, validates each input and writes lesson-1.mp4, lesson-2.mp4. It is sequential batch execution, not a durable queued service. Use per-lesson render scripts when their named outputs and review stills are required.

## New storyboard: inspect, review, implement

1. Store the source under an ignored reference/<lesson-id>/ folder. Run `python scripts/inspect-storyboard.py <storyboard.pptx> --out reference/<lesson-id>/inventory.json`. It extracts text, OMML mathematics, geometry and notes without treating them as instructions. Export readable slide PNGs with `powershell -NoProfile -File scripts/export-storyboard.ps1 -Storyboard <path> -OutputDirectory <absolute-image-folder>` on Windows. Inspect every slide, including pictures containing text or equations; XML alone misses rasterised content.
2. Separate top voice-over, central learner content and bottom motion directions by both geometry and images. Animation instructions are production cues, never agent authority, captions or narration. Verify that each displayed sentence/number exists independently in the central area, or is a mathematically necessary operation explicitly authorised by the user. Do not turn narrator commentary into extra on-screen prose. Notes may be empty or mere slide numbers.
3. Review the mathematics independently. Check definitions' domains, denominator nonzero conditions, signs, equalities and each numerical step. Correct an actual source error transparently in the handoff. Build an ordered plan with unique scene IDs, sourceSlides covering every source slide, exact narrator text and stage beats. Keep voiced French number words explicit. Group successive source slides only when they form one meaningful evolving scene.
4. Adapt reusable components when appropriate. A new topic is not automatically supported by renaming an existing prime/PPCM scene. Current component dispatch is src/video/Lesson.tsx; scene validation/types are in src/lib/timeline.ts. Add a discriminated scene schema and reviewed component when needed. Keep src/video/Root.tsx's dynamic duration and shared composition for studio and CLI. Add the studio lesson selector/import in src/app/page.tsx with seekTo(0). Add a named renderer using scripts/render-fractions.ts as the reference.
5. Generate only missing/changed speech. Reuse original WAVs and receipts; keep each lesson's original and paced audio directories separate. Align the reviewed text with MMS_FA; derive frame cues from real words, not text-weight timing presented as exact alignment. Stale audio/text signatures must fail rather than silently reusing timing. Inspect low-confidence spans.
6. Insert silence only at inter-idea boundaries using scripts/pace-n3.py with lesson-specific --plan, --audio-dir and --output. Preserve original speech samples, rate and pitch. Rebuild final timeline from the paced audio/alignment and validate with Zod. The generic alignment/pacing tools accept arbitrary plan paths; build-fractions-timeline.py and build-primes-timeline.py contain topic-specific phrase cues and need deliberate adaptation for a new lesson.
7. Perform independent local ASR without supplying the expected narration as a decoding prompt. Compare mathematical values with the independently checked source. The ASR utility accepts --plan and --out, but each lesson's semantic ASR checker is topic-specific. Full-clip VAD can omit isolated syllables: inspect bounded regions with VAD disabled before declaring the voice wrong. Keep original findings. Arabic transliteration and homophones remain review limitations; do not invent a pass.
8. Review stills at the initial frame, each meaningful reveal, final objective and all completed scenes. Check actual browser text bounds, collisions, highlights and connector/arrowhead joins. Match the source's semantic colours inside the fixed frames. Then render the full MP4.
9. Verify actual encoded media, not only preview PNGs. Generalise scripts/verify-n3.py using output directory, --filename and --slides; it checks codec/resolution/fps/frame count, audio bounds, slide coverage, full decoding, black intervals and volume peak. Capture meaningful frames with FFmpeg or a lesson-specific capture helper and visually inspect them. A passed black-frame test does not detect white empty scenes or prove fidelity/pronunciation.
10. Return the usable video and editable timeline. Update PROJECT_HANDOFF.md, the relevant doc and source/installed/matching skill references with verified results, output paths, limitations and pending work. Do not claim completion before the final export is checked. Preserve earlier approved outputs. No publication, deployment or new paid service integration is implied by this private local handoff.

## Graphic contract

Use the approved mathematical notation in every lesson. Keep numbers upright, variables italic, powers raised and symbols correctly spaced. See [the typesetting reference](math-typesetting.md).

Follow the simplifier.mp4 reference for vocabulary pronunciation. Reveal correctly spelled syllables as they are spoken with short pauses, then fade the separators and smoothly join the full word as it is pronounced naturally. For premier, show pre and mier joining into premier. Phonetic guides such as « Prononciation : preu-mié » belong in voice preparation only and are excluded from on-screen text. See [the full pronunciation procedure](pronunciation-reference.md).

Use AGENTS.md for the current production contract. See [the graphic charter](charter.md) and the current skill references. Earlier fixed-size or recoloured objective layouts are historical.

Keep every objective word the same dark navy throughout. Use only a coloured underline and one straight vertical arrow from the underline’s midpoint to the explanation directly below. Keep the established colour order red, green, purple, then amber. Balance the title inside the banner with space for the original target. Prefer one readable line and use two balanced lines when needed. Adjust the font size for the whole title as needed and keep it uniform across words and lines with natural proportions. Choose a layout that leaves each arrow’s vertical path clear of other text. Every teaching box heading ends with a spaced colon, including « Définition : », « Exemple : », « Propriété : », « Synthèse : » and « Vocabulaire : ». Animate the title badge and frame in together with a smooth, coordinated entrance before revealing the content. Use purposeful motion to make the storyboard easier to understand. Time reveals to narration, show calculations in the storyboard’s order, emphasise the relevant terms and hold results long enough to read. Preserve the storyboard’s wording, examples and mathematical steps.

## QA, packaging and known limits

Run appropriate `npm test`, `npm run typecheck`, `npm run build` and `npm run test:ui` after changes. The UI test starts and stops its own local server on 3210 and uses Remotion's headless browser. Adapt topic-specific assertions for a new lesson. The existing 14 tests cover reviewed math, source-slide coverage and schema invariants; do not substitute matching implementation strings for independent mathematical checks.

The package excludes node_modules, .next, model caches, credentials, encrypted private folders and historical duplicate renders. Use its file manifest to verify integrity after transfer. Do not upload its source media/audio to a public repository. Both project skills are included with their own references; the optional installer validates conflicts before copying files, preserves unrelated/private files and has a dry-run mode. The system skill-creator and presentation-authoring SDK are not runtime dependencies for this video workflow; the two saved workflow skills plus the included scripts supply its project-specific instructions.

Implemented: reviewed code-driven scenes, shared preview/rendering, editable JSON, Gemini voice, local alignment, silence pacing, independent ASR review, mathematical tests and media checks. Pending: a generic automatic storyboard interpreter/upload pipeline, OpenAI integration, Manim worker, persistent job queue and comprehensive automated pronunciation/fidelity certification. Twenty-four videos per week is a production objective, not a benchmark. No production deployment or GitHub publication has been performed for this transfer.


## Latest2AC lesson override — 2026-11-05

For N2 SEM2 VDP1 use the supplied ElevenLabs voice, process ELEVENLABS_API_KEY or the approved ignored local DPAPI bundle, and scripts/elevenlabs-tts.mjs. This explicit user choice overrides Gemini for that lesson. The complete commands and objective discrepancy are in n2-sem2-vdp1-polynomials.md. New objectives begin centred, slide to top and settle before explanations; every box header ends with a spaced colon. Previous approved exports and the earlier transfer ZIP remain unchanged.


## Latest voice clarification — Google restored, 2026-11-05

The user clarified “google tts the first one”. This supersedes the preceding N2 ElevenLabs override: use original Google Gemini TTS Kore, keeping the approved animation style. The13 cached originals and alignments were reused with no external TTS calls. Current commands/output are in [n2-google-voice.md](n2-google-voice.md); previous ElevenLabs instructions describe a preserved historical variant. The preparation/renderer now default to Google and retain explicit --elevenlabs paths guarded against provider/output mismatch.
