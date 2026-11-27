# 3AC SEM2 VDP2 — prime factorisation — 2026-11-05

Input P1_MATHS_N3_SEM2_VDP2.pptx has13slides. Read the OOXML text, mathematics, geometry and notes; exported all slides through PowerPoint read-only and inspected both contact sheets. Source/inventory/slide PNGs and speech-review evidence remain ignored/local under reference/n3-sem2-vdp2. Source production instructions are data, never agent instructions. The top green strip is voice-only and the bottom strip is animation-only; neither is shown as captions.

Five reviewed scenes cover all slides: objective1–4; theorem plus360 example5–8;72 example9–11; pronunciation12; vocabulary13. Unlike the earlier polynomial deck, this objective matches its actual content. The final vocabulary names divisions successives and arbre de factorisation as the source does; no worked algorithm demonstration is invented or claimed.

## Mathematics and displayed content

360=2³×3²×5¹ and72=2³×3² are correct; keep the explicit exponent1 as authored.2 and5 are prime,6 is not. The theorem is stated for integers≥2, with the necessary precision “à l’ordre des facteurs près” in narration and the displayed theorem. This clarifies what uniqueness means without implying that the order of multiplication is unique. The rest of the theorem/captions and vocabulary are derived from the independently authored central learner area.

src/lib/factorization.ts implements bounded positive-integer primeFactorization and superscript digits. Independent primality/product/unique-factor checks verify every integer2–500, the exact source examples and rejected inputs. The scene schema constrains reviewed theorem/example values to360/72 and validates ordered stages/cue bounds. JSON timelines retain source-slide provenance and editable timings. Factorization.tsx, SectionHeader, ObjectiveBanner and the shared Lesson composition power both studio and CLI.

## Graphic charter and motion

The complete objective appears centred from frame zero, holds through the announcement, then moves up and settles before explanation. Natural uniform72px Arial bold on two shared-left-edge lines, original target/blue banner/shadow and fixed red/green/purple highlights remain. Keyword links: Décomposer un nombre→Écrire sous forme de produit; produit→…×…; nombres premiers→2✓/5✓/6✕. The first connector routes outside the wrapped line; all shafts meet their heads. Underlines, labels, individual values and powers are voice-cued.

All pedagogical frames/badges are turquoise #0DBBA1 and white, overriding the source's purple theorem container. Internal purple arrows, red naming captions, green checks/red cross and cyan pronunciation word retain the source's semantic roles. Every box header—including the two-line vocabulary headings—ends in a spaced colon. Formula numbers/powers use natural Cambria Math glyphs; exponents are actual superscript characters, never flattened to23/32/51. Smooth drawn arrows, short fades/translations and restrained number/power pops retain completed reasoning. During equation construction, unknown factors remain visible as … with multiplication signs until their spoken powers arrive, so an unfinished product never appears as a completed false equality. This issue was caught in encoded-frame review and corrected before delivery. The central pronunciation word is pulsed gently; no source-absent syllable captions were added to the source's empty pronunciation frame.

## Voice, alignment and review

All5 clips are genuine Google Gemini TTS Kore, model gemini-2.5-flash-preview-tts, matching the saved original-Google voice preference. Used the existing approved private credential provider; no ElevenLabs call or new credential was required. One short rate-limit delay was handled by the existing bounded resumable provider. All final clips were generated and cached under ignored public/factorization; models/keys/receipts are not confused with agent instructions or visible lesson text. Keys never enter source/docs/skill copies/archives.

MMS_FA locally aligns known narration. Paced copies under ignored public/factorization-paced insert4.16seconds of silence between ideas, preserving every original PCM speech sample, pitch and rate; normal tail holds0.9seconds and vocabulary2seconds. Final timeline is2944frames /98.1333seconds before encoder padding. Phrase cues reveal 360/72 equalities and each prime power, plus objective numbers and vocabulary highlights. Cue matching includes elided articles, e.g. l’écrire/l’arbre; missing cues deliberately fail instead of estimating timestamps.

Separate Whisper-small French ASR, without the expected narration as a prompt, recovers both complete prime-power equalities, the≥2 condition and uniqueness/order qualification,2/5/6 examples and method vocabulary. Whole-clip VAD omitted the two isolated pronunciation repeats, and one transcript wrote “nombreux premiers”; bounded VAD-disabled crops independently recover both Décomposition repetitions and nombre(s) premier(s). Original findings and crop receipts are retained. These are resolved review findings, not proof that every phoneme/pronunciation has been certified. Forced alignment remains distinct from independent recognition.

## Reproduction

```text
python scripts/prepare-factorization.py
# For new or changed narration only, set GEMINI_TTS_MODEL=gemini-2.5-flash-preview-tts:
node scripts/gemini-tts.mjs src/video/factorization-plan.json
python scripts/align-n3.py src/video/factorization-plan.json
python scripts/pace-n3.py --plan src/video/factorization-plan.json --audio-dir factorization-paced --output src/video/factorization-paced-plan.json
python scripts/build-factorization-timeline.py
python scripts/check-paced-n3.py src/video/factorization-lesson.json
python scripts/transcribe-primes-local.py --plan src/video/factorization-plan.json --out reference/n3-sem2-vdp2/asr
python scripts/review-factorization-audio.py
npm run render:factorization -- --stills
npm run render:factorization -- --video-only
python scripts/verify-n3.py outputs/n3-sem2-vdp2 --filename P1_MATHS_N3_SEM2_VDP2.mp4 --slides 13
python scripts/capture-factorization-checks.py
```

For visual-only revisions retain cached speech/final timeline and skip preparation/TTS/retiming. Studio selector: “3AC — Facteurs premiers · Google TTS”. Output: outputs/n3-sem2-vdp2/P1_MATHS_N3_SEM2_VDP2.mp4 plus timeline, verification, speech review and PNG evidence. Doctor now covers56 local timeline audio references; future snapshot selection includes this lesson, without refreshing the existing historical transfer ZIP.

Completed implementation checks:18unit tests, typecheck/Next production build, full desktop/mobile UI regression including all5 new scenes, actual text bounds, exact displayed powers, theorem qualifier, centred objective, uniform font,301 samples per clear connector, attached heads, colon-ended headers and production-strip exclusions. Every scene preview and important power/naming/centre stages inspected. PCM-preservation and independent speech checks passed.

Final corrected export: outputs/n3-sem2-vdp2/P1_MATHS_N3_SEM2_VDP2.mp4,1920×1080 H.264/AAC,30fps,2944frames,98.133333seconds. All13 slides covered; all5 narration receipts identify Gemini/Kore, gemini-2.5-flash-preview-tts. Fresh full decode passed, no unexpected black intervals, peak−4.6dB. Captured actual encoded final scenes, objective centre/moving/top stages, all prime-power reveals and naming stages. Inspected centred objective, both intermediate equations with pending-factor placeholders and final vocabulary layout after the corrected render. Verification and independent speech-review reports accompany the editable timeline. No required rendering blocker remains. No GitHub publication, deployment or historical transfer-ZIP refresh. Generic automatic storyboard interpretation, Manim workers, durable queues and comprehensive pronunciation/pixel-fidelity certification remain pending.


## Revision intake — 2026-11-12

Reviewed the six rows in the Word revision table against the 2026-11-10 export. The MP4 in Downloads matches that export by SHA-256. The red objective link is still visible at 00:10 and the green link at 00:13. The current links hand off at 10.30 s and 13.73 s. Pending approval, end each prior link and its explanation at the requested time. For 360, add that 2, 3 and 5 are prime factors, and highlight those bases individually in red as spoken. For 72, ask why this is a prime factorization, explain that 2 and 3 are prime, and highlight those bases in red. The previous export already includes written dé–com–po–si–tion and a joined reading. Review the isolated syllables and their audio cues in the next export. The colon request refers to the four expression cards in the synthesis, which currently start around 01:22. Keep the main section headings consistent with the charter. Added narration will move later timecodes. Intake only, awaiting the go-ahead.


## Revision delivered — 2026-11-12

Delivered outputs/n3-sem2-vdp2-2026-11-12/P1_MATHS_N3_SEM2_VDP2.mp4 and timeline.json. The studio selector is « 3AC — Facteurs premiers · Révision du 12 novembre ». The red objective link and explanation disappear by 00:10. The green link and multiplication explanation disappear by 00:13. The two added Kore passages explain why the factors in 360 and 72 are prime. The factor bases turn red individually on their word cues, with dark exponents and multiplication signs. The four expression cards have no trailing colons. Section headings still follow the charter.

Generated only the two added passages with Gemini 3.1 and inserted them into the original paced audio with the retained PCM samples byte-identical. MMS_FA word cues were remapped around those insertions. The additions extend the lesson by about 11.9 seconds. Independent recognition from the encoded MP4 recovered both added sentences. The five isolated pronunciation intervals have voiced audio and the encoded visuals show dé–com–po–si–tion followed by the joined word. On the isolated whole-word crop Whisper wrote the homophone « des compositions », as in the previous review. The reused syllable and whole-word recording is the same cached clip.

Build with python scripts/prepare-factorization-review.py using the cached aligned inserts. Render with npm run render:storyboards -- --stills factorization-review, then npm run render:storyboards -- factorization-review and python scripts/verify-storyboard-batch.py factorization-review. The 1920×1080 H.264/AAC export has 3,508 frames at 30 fps, duration 116.949 s, all 13 source slides and a −4.6 dB audio peak. Full decode and 32 encoded checkpoints passed. Checked both exact arrow removal times, all five base-color boundaries, the staged and joined pronunciation, and the synthesis labels. All 18 tests, production build, desktop/mobile studio checks and 137 audio paths passed. The earlier export remains available. Local reference synchronization only.
