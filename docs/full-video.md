# Full lesson reconstruction — 2026-11-02

User explicitly requested generating the full video after receiving the comparison. This authorizes continuing beyond the earlier review checkpoint; it does not certify exact charter or animation parity.

Full lesson: `src/video/full-lesson.json`, 5400 frames at 30 fps (180 seconds), eight editable sequences. Source is the 27-slide PPTX and 180.013-second MP4. Remotion reconstructs visuals using SVG/text; only the original narration is reused, from the local `public/reference/full-narration.wav`. There is no original-video layer in the composition.

| Interval | Content |
| --- | --- |
| 0–28 s | Objective, Arabic terminology and numerical examples |
| 28–42 s | Reading and syllables of “comparer” |
| 42–48 s | Property 1 introduction |
| 48–58 s | Negative-number comparison property |
| 58–95 s | Worked comparison of −3 and −2 |
| 95–134 s | Property 2, signs and comparison of −5 and 1 |
| 134–170 s | Number line, placement and −3 < −2 |
| 170–180 s | Smaller to the left, greater to the right summary |

Corrected source-video error “−5 > 1” to “−5 < 1”, and “On na” to “On a”. Source and generated keyframe pairs are in `outputs/full/reference-comparison.png`. The target icon is a vector reconstruction; font metrics, timing, fades and outlines remain approximations rather than a pixel-perfect After Effects reproduction. Narration timing follows the original track with manually authored events, not automatic alignment.

The initial full-render pass was stopped when visual comparison caught UTF-8 text being read using the Windows default encoding. JSON loading now explicitly uses UTF-8; regression tests check both accented titles.

Run `npm run render:full`. It exports the MP4, timeline JSON and nine native 1080p stills under outputs/full. The UI selector “Vidéo complète — 3 min” loads the same timeline. Tests cover total duration, scene boundaries, one audio track, accents and invalid event bounds, in addition to the earlier mathematical comparison tests.

See project handoff for final media verification. AI interpretation, generated TTS, automatic alignment, general symbolic QA, Manim and persistent jobs remain pending. No production deployment, paid API calls or GitHub publication.
