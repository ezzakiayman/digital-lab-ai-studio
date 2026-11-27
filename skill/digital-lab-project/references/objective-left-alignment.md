# Objective layout — left alignment and balance — 2026-11-04

Historical v3 layout. The current prime objective uses a compact single line at the same font size; see [current objective layout](objective-single-line.md). The shared-left-edge guidance still applies when a longer objective genuinely needs wrapping.

User requested left alignment and a balanced, symmetric layout for the opening objective declaration. The current prime lesson now uses one common left edge at x=360 for both title lines, after the original target asset. Baselines remain y=235 and y=345; every word stays 72 px Arial bold with natural glyph proportions. The first and second line widths are approximately 760 and 860 px, giving balanced wrapping without the previous staggered indentation.

The three explanation columns end at x=480, 960 and 1440, equally spaced around the frame centre. Title-keyword underlines/highlights retain the fixed red/green/purple order. Their connectors are rerouted to the actual words and their arrowheads; no title glyph is crossed. The prime-example bubble cluster is balanced around x=1440: top pair at 1320/1560, middle at 1440, bottom pair at 1380/1500. Narration-only text remains excluded and the original approved question asset is retained.

Reusable preference: multi-line objective titles use a shared left edge with consistent line spacing after the target. Arrange explanatory groups on a balanced grid. Route connectors through clear space and check their geometry against actual rendered text; do not change font size or stretch letters to force alignment.

Implementation: src/video/Primes.tsx. Browser checks verify both line left edges, equally spaced explanation endpoints, arrowhead attachment and 201 samples per connector against title text bounds with a 2 px guard. Typecheck/build and the full studio checks pass.

Render: `npm run render:primes -- --v3` (add `--video-only` after reviewing stills). Output: outputs/n3-sem2-vdp1-v3/Digital-Lab-3AC-Nombres-premiers.mp4. Earlier exports are retained. No new narration is generated; final timeline/audio identity and media verification are recorded in the latest handoff.

Final export verified: 1920x1080 H.264/AAC, 30 fps, 6791 frames, 226.368 s; full decode passed, no black intervals, peak -3.4 dB. Actual encoded opening and completed-objective frames reviewed. AAC audio and complete timeline are identical to v2. Both reusable skills validate and are synchronized locally; no GitHub publication.
