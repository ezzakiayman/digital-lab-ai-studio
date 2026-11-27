# Objective declaration and motion revision — 2026-11-02

The user approved installing/reusing their presentation-video kit and supplied four explicit graphic references. Installed skill: presentation-video. Its entrypoint adapts the original kit to the existing Remotion/Gemini workflow; the complete supplied file is retained unchanged under references/original-kit.md. Digital Lab-specific rules are in references/digital-lab-objectives.md.

The first scene is now named “Déclaration de l’objectif”. It uses the exact target/dart PNG extracted from the provided storyboard, not the earlier simplified vector. White rounded banner, blue border, navy title and grey shadow follow the screenshot. The longer N3 title fits on one line so no descending arrow crosses other title text. This produces a smaller title font than the shorter N1 screenshot; native text remains above 40 px.

Keyword links are anchored to their real title spans, each with underline and downward arrow: red #E60012, green #0DBBA1, purple #7061AA. Fourth-colour rule is amber #D28B14; the N3 objective only has three actual explained phrases, so no artificial fourth item is added. Number examples stay blue, correct ticks green, invalid crosses red. The known-transcript timing reveals “Trouver”, Arabic terminology, valid examples, then invalid examples when spoken.

Inspected N3 storyboard theme and display-shape fills rather than copying narrator/production notes: definition #92D050, property theme accent2 #ED7D31, synthesis #00B050, multiples #0070C0. The red minimum circle and repeated red 72 are preserved. These semantic colours are separate from the ordered objective-link palette.

Replaced hard shows with eased 16-frame fades/short 8 px translations; arrows and the minimum ellipse draw progressively. Multiples 12, 24, 36 appear on aligned word onsets. The minimum is circled on its concluding spoken “douze”. Vocabulary receives gentle emphasis on its spoken cue, without hard flashing.

Local alignment adapted from the kit: Torch 2.8.0 + matching TorchAudio 2.8.0 CUDA, uroman and regex. The public MMS_FA model is cached once outside the repository. scripts/align-n3.py processed all fifteen existing Gemini recordings locally, without generating new voice or sending API requests. Cached word intervals and confidence scores are in ignored public/n3/alignment/. scripts/build-n3-timeline.py checks audio/transcript hashes and uses those intervals for beats and selected reveals. It rejects stale alignment instead of silently reusing it.

MMS_FA aligns the supplied transcript; it does not verify the transcript is what was actually spoken. Some French number words have low confidence, so exact-word precision and pronunciation are not certified. Representative timings inspected: objective “trouver” 8.904 s, Arabic phrase 12.706 s, “cinquante-huit” 18.509 s, zero 20.710 s; multiples 12/24/36 at 8.746/9.567/10.567 s and final 12 at 14.951 s, relative to those scenes.

Output revision lives in outputs/n3-v2/, retaining outputs/n3/ unchanged. Run `npm run render:n3 -- --revision`; verify with `python scripts/verify-n3.py outputs/n3-v2`. Source timeline, voice and mathematics remain editable. No captions, music, new narration or external deployment were added for this visual revision. See current project handoff for final checks.

Alignment API reference: [PyTorch 2.8 forced alignment](https://docs.pytorch.org/audio/2.8/tutorials/ctc_forced_alignment_api_tutorial.html). Keep Torch/TorchAudio matched; the API is deprecated in 2.8 and later versions require compatibility review.
