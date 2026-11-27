# −3 versus −2: review package, 2026-11-02

## Source and implementation

Source PPTX slides 9–14 and original MP4 interval 58–95 s. The 37-second reconstruction uses native editable SVG text, frames, arrows, sign outlines, emphasis, absolute values and progressive conclusion. Source pixels are used only in comparison artifacts, never as the generated video. A local reference narration excerpt is retained; the JSON narration is a descriptive summary, not an aligned transcript.

Open `outputs/comparison/side-by-side.mp4` for synchronized original-left/generated-right review. Standalone generated video is `outputs/comparison/generated.mp4`. `comparison-contact.png` compares original 72/85/94 s with generated 14/27/36 s. Individual full-resolution frames and amplified difference images are alongside them. Both panels use the same narration track to avoid doubled audio.

Timeline: `src/video/comparison.json`. Every event has editable from/to frames. Operands are structured, with validation requiring a < b < 0 for this specific template. Absolute values and final comparison are derived from the operands. This layout is calibrated for the reference's single-digit values; arbitrary long numbers require a layout check.

## Visual observations and validation gate

Compared all three rendered keyframes directly with corresponding originals. Frame positions, white background, turquoise headers/outlines, hierarchy and red comparison marks are closely matched. Remaining differences include glyph spacing, red shape details, font metrics and subsecond fades. Original font identity is not confirmed. Event timings were estimated from one-second contact sheets and use ten-frame fades, not original motion curves or automatic word alignment. No numerical fidelity score or exact-match claim is made.

The original visibly says “On na”; that typo is preserved for the fidelity review and should be corrected to “On a” before approved educational publication. It is not a mathematical assertion. The mathematical implication 3 > 2 ⇒ −3 < −2 is tested.

Human validation of charter and motion is pending. Do not continue the remaining video or mark the graphic charter approved until the user validates this comparison.

## Checks

- TypeScript, three tests, and production build passed.
- Browser check confirms the new example selector changes JSON and live SVG; desktop and mobile overflow checks passed.
- Generated MP4: 1920×1080, H.264, 30 fps, AAC, 37.013 s including encoder padding.
- Generated and comparison MP4 fully decoded with FFmpeg without errors.
- Audio measurement: mean −18.4 dB, sample peak −0.8 dB. This does not certify absence of source distortion or intersample peaks.
- Not yet implemented: automatic font/layout analysis, blank-frame detection, word alignment, general symbolic math checking, comprehensive export QC, or AI interpretation.

Reproduce with `node node_modules/tsx/dist/cli.mjs scripts/render-comparison.ts`, then extract original frames at 72, 85, 94 s and run `python scripts/compare-frames.py`. Source narration excerpt must exist at `public/reference/negative-comparison.wav` (FFmpeg: start 58 s, duration 37 s, PCM WAV).
