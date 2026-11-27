# Fixed chart and teaching rhythm — 2026-11-02, latest rules

Typography correction, 2026-11-03: v3's mixed 72/64 px below is superseded by uniform 72 px Arial bold and natural glyph proportions. Read [objective-typography-v4.md](objective-typography-v4.md).

User prioritizes constant graphic charter over source chapter-box colours. All content frames/badges (definition, property, example, verification, synthesis, others) are turquoise #0DBBA1 with white bodies. Keep the approved objective banner blue. This supersedes v2 green/orange/green section-frame decisions. Preserve meaningful colours inside mathematics separately.

Objective title is now large: 72 px first line, 64 px second, with active phrase coloured and softly highlighted to match its red/green/purple arrow. Keep target/dart, blue outline, navy inactive text and shadow. Wrap rather than shrink long titles. A curved connector can route around lower-line text without crossing it.

Reusable explanation rule: when explaining any acronym, emphasize/animate its actual letter and connect an arrow from that letter directly to its corresponding word. Current P/P/C/M columns connect to Plus/Petit/Commun/Multiple; arrow and word-initial colours match. Do not place decorative arrows that originate from unrelated empty space. Use subtle number/equation pop-ins only to support the reasoning.

Teaching rhythm: small reflection pauses between ideas and after important results. Preserve voice pitch and natural spoken rate, align reveals to the paced audio, and hold completed steps before transitions. Current implementation inserts silence only into original aligned gaps, targeting 0.85–1 s, leaving already adequate ≥1.2 s gaps, and holds scenes an extra 0.9 s. Source Gemini recordings remain untouched. Script verifies every speech sample is preserved exactly.

Pipeline: scripts/pace-n3.py → scripts/build-n3-timeline.py --paced → npm run render:n3 -- --v3. Output outputs/n3-v3/Digital-Lab-3AC-PPCM.mp4, 217.6 seconds, 6528 frames, 1080p30 H.264/AAC, full decode passed, no black intervals, sample peak −2.8 dB. Added 6.18 s inside speech gaps plus increased scene holds. Original/v2 media retained. Paced WAVs/alignment under ignored public/n3-paced. No API generation in this revision.

Ten tests, production build/typecheck and UI common-container/letter-arrow/preview/mobile checks passed. Original-speech-plus-silence verification passed for all fifteen recordings. Objective/acronym and box previews plus actual exported frames inspected. Graphic charter in src/lib/charter.ts; layout in ObjectiveDeclaration.tsx; meaningful acronym animations in Ppcm.tsx. See workspace docs/pacing-charter-v3.md and latest PROJECT_HANDOFF.md. No deployment or GitHub publication; installed/source/matching local skill copies synchronized.
