# Objective typography correction — 2026-11-03

The user reported that the opening objective still had inconsistent font sizes. Revision 3 used 72 px on the first line and 64 px on the second, with SVG textLength/spacingAndGlyphs fitting each phrase to a fixed width.

The shared preview/render component now uses one objectiveTitleFontSize of 72 px, Arial bold, for every title phrase on both lines. It renders natural glyph proportions without forced width or per-phrase shrinking. The second line is repositioned and its underline/highlight enlarged to the natural 1124 px text width. The blue target/banner, ordered coloured arrows and active highlights remain aligned.

Reusable rule: use the same font family, weight and size throughout an objective title. Wrap/reflow long text instead of reducing individual words or lines, and do not stretch glyphs to fit widths. Check actual browser text bounds against banner and connector positions.

Render: `npm run render:n3 -- --v4`. Output: `outputs/n3-v4/Digital-Lab-3AC-PPCM.mp4`. Existing paced narration/timeline are reused without API calls. Prior exports are retained. See the latest handoff for completed checks and media verification.

Verified final output: 217.6 s, 6528 frames, 1080p30 H.264/AAC; full decode passed, no black intervals, peak -2.8 dB. Ten unit tests, typecheck/build and browser font/bounds/mobile checks passed. Opening and final objective frames from the actual export reviewed. Timeline/audio references equal v3 and all fourteen later-scene preview PNGs are byte-identical. Both reusable skills validate and are synchronized locally; no GitHub publication.
