# Objective typography and compact banner — 2026-11-04

User requested a better mise en page after viewing the two-line objective. The current prime objective now reads as one continuous sentence on a single baseline. This removes the broken reading flow, the large empty area in the former banner and connectors travelling between title words.

The text remains 72 px Arial bold, with natural glyph proportions and normal word spacing. All five title runs share baseline y=285, starting at x=220. Browser-measured right bound is x=1862.109375. The blue rounded banner is x=32, y=150, width=1856, height=220. Original target artwork is scaled proportionally to width=132 and vertically centred at y=260. Its left padding is 30 px, the text's right padding is 25.890625 px, and the gap after the icon is 26 px. The title therefore fills the available space without a smaller font or forced SVG width.

Each explained keyword keeps its underline and matching highlight in the fixed red/green/purple order. Connectors descend beneath the single title line and bend gently towards columns x=480/960/1440. They no longer travel through word spaces inside a wrapped sentence. The symmetric example-number cluster, all later content, original question bubble, voice-only storyboard-strip rule and narration timings remain.

Reusable layout guidance: first measure the complete objective at the approved font size. Prefer one clear line when it fits with balanced icon/text padding. Adapt banner height and icon scale to the content while preserving the charter's artwork, colours, typography, border, corners and shadow. If the title genuinely needs wrapping, keep a common left edge and balanced line spacing; route connectors outside the reading area. Do not impose old hard-coded indentation or a two-line layout when a clear single line fits.

Implementation: ObjectiveBanner now has an opt-in single-line layout; the standard default keeps existing PPCM geometry. Current prime scene uses the single-line variant. Studio and renderer share the same composition.

Render: `npm run render:primes -- --v4` (add `--video-only` after reviewing stills). Output: outputs/n3-sem2-vdp1-v4/Digital-Lab-3AC-Nombres-premiers.mp4. Prior exports are retained. Browser checks verify a common baseline, natural font size, balanced inner margins, icon gap, text bounds, clear connectors, attached heads, all eleven scenes and mobile overflow. See latest handoff for completed media and audio-identity checks.

Final media verified: 1920x1080 H.264/AAC, 30 fps, 6791 frames, 226.368 s; full decode passed, no black intervals, peak -3.4 dB. Actual encoded opening and fully explained objective frames reviewed. Complete timeline and AAC audio hash match v3 exactly. Both skills validate and are synchronized locally; no GitHub publication.
