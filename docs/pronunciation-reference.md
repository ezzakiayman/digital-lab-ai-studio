# Pronunciation sections — approved simplifier reference

User clarification, 2026-11-10. Follow the simplifier.mp4 reference for vocabulary pronunciation. Reveal correctly spelled syllables as they are spoken with short pauses, then fade the separators and smoothly join the full word as it is pronounced naturally. For premier, show pre and mier joining into premier. Phonetic guides such as « Prononciation : preu-mié » belong in voice preparation only and are excluded from on-screen text.

Permanent user rule,2026-11-05: future word-pronunciation sections must follow the animation and spoken-pronunciation pattern in the supplied simplifier.mp4. This supersedes earlier whole-word pulses/repeats or static syllable rows for these sections. Existing delivered videos are unchanged by this workflow update.

## Master and verified observations

Keep the supplied clip as the local audiovisual master: reference/pronunciation-simplifier/simplifier.mp4 (original Downloads/simplifier.mp4). SHA256 a62abbf0ebc676f30cdc9e649d694e5a0e956352c9df2ee01bdd366cf7cff0f2. It is1920×1080,24fps,212video frames,8.857seconds with AAC audio. Project exports remain1080p30; adapt timing by seconds, not reference frame numbers. Media/evidence stay ignored/local, outside saved skills and public repositories; include this master in future private project transfers.

Decoded contact sheet and full-resolution samples show:

1. Plain white background; one large bold lowercase word line in the central reading area. Reserve the final line's position/width so earlier syllables do not jump to a new centre as the word grows. Do not add a pedagogical box/header inside this pronunciation insert merely to reuse the old template.
2. Reveal progressively from left to right: sim- in blue, then pli in green and its blue separator, then fier in red. Earlier parts remain visible. The appearance is a horizontal reveal through the letters, rather than a whole-word pulse, bouncing letters or three disconnected rows.
3. Hold the coloured sim-pli-fier long enough for syllable reading. Fade the blue hyphens, smoothly change all letters to the same blue, then close the inter-part gaps so the line becomes the single correctly spelled word simplifier, centred in place. Hold that joined word for the full-word reading and reflection.
4. Indicative source phases: first part around0.5–1s; second around2.5–3s; last around3.75–4.25s; hyphen/colour transition around5.25–5.75s; joining around5.75–6.5s; complete word held to the end. These are reference observations, not automatic onset timestamps or a universal duration for every word. Recheck the actual clip when implementing.

Dominant decoded flat colours approximate blue #087ABA, green #21A972 and red #E60000. Compression creates neighbouring shades; these samples do not certify original vector values. Use this blue→green→red pronunciation palette, distinct from the objective-arrow red→green→purple palette. For other words retain linguistically correct segmentation and any explicit storyboard semantic colours, adapting the number of parts without forcing exactly three syllables. Keep natural letter proportions and large readable type; match the master visually rather than claiming an unmeasured original font.

## Voice and synchronisation

Use the same teaching delivery: clearly articulate each actual French syllable separately, with short silent gaps, then pronounce the joined word naturally. Speak sounds, not letter names, punctuation or hyphens. For simplifier the written segmentation is sim / pli / fier and the pronunciation is /sɛ̃.pli.fje/; do not voice final r as an isolated consonant or turn the first syllable into literal letter names. Review the segmentation and pronunciation for each new mathematical word.

The latest provider/voice preference remains Google Gemini TTS Kore. This example defines the required pronunciation/cadence and motion; it is not a completed speaker-cloning implementation. Generate controlled syllable delivery and a natural full-word pass; retain clean recordings and real syllable-boundary cues separately from editable visual timing. Reveals should track their spoken parts and joining should support the natural whole-word pass. Adjust reflection pauses without stretching speech/pitch. Do not blindly reuse this clip's8.857s duration for longer words.

The user now explicitly authorises syllable spelling derived from the pronunciation target as learner content in these pronunciation sections. This narrow exception does not authorise transcript captions from the top voice-over strip or display of bottom production instructions. Do not add unrelated narrative text.

## Review and current implementation limit

Before delivering a future lesson, compare the new insert with the master: progressive reveal, retained parts, colour order, separator fade, smooth colour unification/join, final spelling, natural type, syllable audio and full-word pass. Inspect intermediate encoded frames and review bounded audio regions. A forced-alignment whole-word span cannot establish individual syllable onsets; use actual syllable evidence/cues and resolve ambiguous speech before claiming a match.

Local independent Whisper-small recognition without an expected prompt recovered syllable-like “Sam, pli, fié” and full-word “simplifié”; these phonetic/homophone transcriptions do not change the displayed infinitive simplifier or certify precise pronunciation/timbre. Contact sheet, sampled frames, extracted audio, ASR and visual-evidence.json are retained beside the ignored master. The PyAV decoder mismatch was bypassed using FFmpeg PCM input. No speech API calls were made.

The shared `PronunciationWord` component supports binôme, trinôme, polynôme and premier. Each insert uses separate spoken syllables within its narration clip, timed reveals and the joined full-word reading. For premier, the screen shows pre and mier while the speech preparation uses Preu and Mié. Extend the measured word data and review the speech for additional words. See the revised polynomial and prime lesson references for the encoded checks.

The four-storyboard batch extends the same component to sem–blables, dé–com–po–si–tion and ir–ré–duc–tible. It pairs each displayed part with its aligned spoken interval and joins the full word. The displayed ir preserves the first r while its sound cue is i. Verify the joined spelling when written and spoken boundaries differ. The two-part semblables follows spoken French with a silent final e. See the batch reference for the bounded audio checks and ambiguity limits.
