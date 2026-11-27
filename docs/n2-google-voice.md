# Restored original Google TTS voice — 2026-11-05

Latest user clarification: “i mean google tts the first one”. This supersedes the intervening ElevenLabs voice request and the earlier interpretation of “use TTS” as a generic synthesis-method preference. Restore Google Gemini TTS, Kore, as the selected voice. This is the original Gemini speech workflow, not a newly added Google Cloud Text-to-Speech integration. No credential, provider quota or external voice API was accessed for this restoration.

All13 original Google recordings were already cached in public/polynomials. Their text/model/voice signature receipts match the restored reviewed plan exactly; every original audio/text alignment signature is valid. Nine clips use gemini-3.1-flash-tts-preview and four use gemini-2.5-flash-preview-tts, all Kore. Reused these exact files rather than regenerating speech. The explicit-variable-name and shortened-conclusion edits made specifically for ElevenLabs remain in that archived variant. The restored Google transcript is the original corresponding French script, with identical mathematics and on-screen content.

The previous ElevenLabs MP4 remains at outputs/n2-sem2-vdp1/P1_MATHS_N2_SEM2_VDP1.mp4. Its plan/paced plan/final timeline were copied to ignored reference/n2-sem2-vdp1/elevenlabs-*.json. New Google delivery lives separately at outputs/n2-sem2-vdp1-google/P1_MATHS_N2_SEM2_VDP1.mp4. Current studio/timeline use the restored Google voice. The preparation script defaults to Google; --gemini remains explicit, --elevenlabs selects the preserved alternative. The renderer defaults to the Google output, with --elevenlabs selecting the older directory only if the active timeline actually contains ElevenLabs audio. This guard prevents accidentally overwriting one voice variant with the other.

Paced Google copies under public/polynomials-paced insert8.60seconds of silence between ideas, preserving every original PCM speech sample/rate/pitch. All13 final timings/cues rebuilt from the validated cached alignments. Timeline is7262frames /242.0667seconds before AAC padding. The current animation components, centred-to-top objective, uniform72px Arial, palette, headers with colons, mathematics and source-strip exclusions are retained. All13 completed-scene preview PNGs are byte-identical to the ElevenLabs revision; only narration and its timing were changed. This compares final visual states, not every intermediate frame.

Independent cached Whisper-small ASR receipts are fresh for all13 restored original WAVs. The whole-clip four-term example transcript represented spoken multiplication symbolically as x/adjacency. An independently decoded first-sentence crop (0–13.3seconds), with VAD disabled and no expected-transcript prompt, recovered the exact multiplication wording and ordered expression x³y² + xy³ − x³ +5. Original finding and new crop receipt retained. Semantic coefficient/exponent/term-count/classification/synthesis checks pass. Known-transcript alignment remains a timing operation, and ASR is not comprehensive pronunciation certification.

## Reproduction

```text
python scripts/prepare-polynomials.py --gemini
# Reuse the matching cached audio; do not call TTS for a visual-only edit.
python scripts/pace-n3.py --plan src/video/polynomials-plan.json --audio-dir polynomials-paced --output src/video/polynomials-paced-plan.json
python scripts/build-polynomials-timeline.py
python scripts/check-paced-n3.py src/video/polynomials-lesson.json
python scripts/review-polynomials-audio.py
npm run render:polynomials -- --stills --keyframes
npm run render:polynomials -- --video-only
python scripts/verify-n3.py outputs/n2-sem2-vdp1-google --filename P1_MATHS_N2_SEM2_VDP1.mp4 --slides 34
python scripts/capture-polynomials-checks.py outputs/n2-sem2-vdp1-google
```

If changing narration in future, generate/review the changed Google clips and realign them before pacing; current restoration needed neither generation nor a new forced-alignment inference. The ASR reviewer infers provider and checks the correct corresponding receipts; optional --out and --asr-dir support explicit review folders. --keyframes reduces duplicate visual-only revision stills while keeping all13 completed scenes plus objective centre/move/top checkpoints.

Typecheck/production build, full desktop/mobile UI checks, restored Google audio paths, actual title/scene bounds, colon-ended headers, all source-slide/math checks and PCM preservation passed. Original ElevenLabs export preserved. Final Google MP4 verified:1920x1080 H.264/AAC,30fps,7262frames,242.069seconds. All34 slides covered and all13 narration receipts are Gemini/Kore. Full FFmpeg decode passed, no black intervals, peak−3.5dB. Actual encoded centre/moving/top objective, completed objective, signed-term highlights and synthesis captured; centre/objective/5x highlight/synthesis frames visually inspected. No required rendering blocker remains. The original source objective/content discrepancy remains as previously documented; professor approval of the content-matched objective is not implied by this voice change. No GitHub publication, deployment or historical transfer-ZIP refresh.
