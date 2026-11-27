# 3AC PPCM video with Gemini narration — 2026-11-02

Input: Downloads/P1_MATHS_N3_SEM1_VDP4.pptx, 39 slides. Local copies, ordinary text inventory, OMML equations and notes inventory are under reference/n3/ and ignored. Notes only contained slide numbers in the inspected samples. PowerPoint authoring directions were treated as content cues and excluded from spoken narration.

Delivered: outputs/n3/Digital-Lab-3AC-PPCM.mp4, 1920×1080, 30 fps, H.264/AAC, 6140 frames, 204.672 seconds. Fifteen manually reviewed, editable scenes cover all 39 source slides. Narration is genuinely Gemini-generated, not the previous reference narration. Twelve segments use gemini-2.5-flash-preview-tts; the final three use gemini-3.1-flash-tts-preview after the 2.5 daily quota was exhausted. All request the Kore voice. The API key is stored only in a Windows DPAPI encrypted bundle under the installed skill's ignored private/ directory; never copy that bundle to source, references or GitHub.

The user selected Gemini instead of ElevenLabs for this and future narration. Use GEMINI_API_KEY from the process environment if configured, otherwise the local DPAPI bundle. The provider script sends the credential in the x-goog-api-key header, not the URL. It redacts returned errors, honors short rate-limit delays, stops on daily quotas, bounds temporary-service retries, and caches audio with a provider/model/voice/text signature. Reusing valid cached narration does not spend more API calls. Use --force only for intentional regeneration.

Pipeline:

1. `python scripts/prepare-n3.py` creates the reviewed narration/scene plan.
2. `npm run tts:gemini` generates or resumes audio. GEMINI_TTS_MODEL selects an available compatible generateContent TTS model; model discovery is `node scripts/gemini-tts.mjs --probe`.
3. `python scripts/build-n3-timeline.py` reads real WAV durations and adds 0.45 s scene padding.
4. `npm run render:n3` renders stills, editable JSON and MP4.
5. `python scripts/verify-n3.py` verifies the delivered media.

Timeline src/video/n3-lesson.json; editorial narration src/video/n3-plan.json. Scene durations are derived from actual audio. Intra-scene beat starts are estimated by text weighting, not forced word alignment. Renderer uses deterministic SVG elements, circled minimum, arrows, progressive values and product verification. No AI-generated formula imagery. The previous calibrated Digital Lab palette/frames are reused; exact font and After Effects parity are not certified.

Mathematical checks: PPCM(6,4)=12, PGCD(6,4)=2, 72=8×9, PPCM(72,8)=72, and PPCM×PGCD=a×b for all positive integer pairs up to 40. Seven tests, TypeScript, production build and browser selection/preview/overflow checks passed. All fifteen representative scene stills inspected; actual exported video frame also inspected. Full FFmpeg decoding passed, no black intervals detected, audio peak −2.9 dB. Black detection does not detect white blank frames or establish speech correctness.

Optional sampled audio transcription was attempted separately: old analysis model rejected with 404, current analysis model returned overload and ultimately timed out. No transcript-level pronunciation verification is claimed. Generated audio remains available for human listening review. Full automatic interpretation, word alignment, Manim and persistent queues remain pending. No deployment or GitHub publication.

Implementation references: [Gemini TTS](https://ai.google.dev/gemini-api/docs/speech-generation), [audio understanding](https://ai.google.dev/gemini-api/docs/generate-content/audio). Current API model availability is probed rather than assumed from documentation alone.
