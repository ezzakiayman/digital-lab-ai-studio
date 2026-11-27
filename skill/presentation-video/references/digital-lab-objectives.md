# Digital Lab objective declaration

Current user rules, 2026-11-10. Keep every objective word the same dark navy throughout. Use only a coloured underline and one straight vertical arrow from the underline’s midpoint to the explanation directly below. Keep the established colour order red, green, purple, then amber. Balance the title inside the banner with space for the original target. Prefer one readable line and use two balanced lines when needed. Adjust the font size for the whole title as needed and keep it uniform across words and lines with natural proportions. Choose a layout that leaves each arrow’s vertical path clear of other text. Every teaching box heading ends with a spaced colon, including « Définition : », « Exemple : », « Propriété : », « Synthèse : » and « Vocabulaire : ». Animate the title badge and frame in together with a smooth, coordinated entrance before revealing the content. The complete objective still starts centred and slides to the top before the explanations. The approved first screenshot is saved locally in reference/objective-2026-11-10/approved.png.

User instructions, 2026-11-02, supported by four supplied reference screenshots:

- Name the first section “Déclaration de l’objectif”.
- Top green storyboard strip = voice-over only; never display it or convert voice-only wording into captions or on-screen questions/summaries. Bottom strip = animation directions only; never display or narrate it. Use the main student-content area for visuals. A title/definition also independently authored in that area remains valid even if spoken in the top strip. Do not confuse production strips with legitimate coloured learning containers.
- Every question icon uses the blue bubble supplied on 2026-11-12. Reuse the 1254×1254 RGBA PNG at public/brand/question-mark.png through src/video/QuestionMark.tsx. The component accounts for transparent margins and keeps the artwork’s proportions.
- Keep the white rounded objective banner, blue outline, grey drop shadow, dark navy title and blue target with orange dart.
- Measure the title and its actual text bounds before choosing a line break or a uniform font size. Place each explanation under its keyword and keep the vertical path clear.
- Match the underline to the actual keyword span. Attach the vertical shaft at its midpoint and align the arrowhead and explanation on that same x coordinate.
- Fixed explanation order: first red #E60012, second green/turquoise #0DBBA1, third purple #7061AA. For a fourth explanation use a distinct fourth colour, currently amber #D28B14. With only one or two explanations use the first one or two colours; never reorder or rotate them.
- This sequence applies to keyword-explanation links. It does not override semantic colours elsewhere, such as correct/incorrect examples, mathematical emphasis or chapter colours.
- Do not add extra explanations, keywords or mathematical content to fill a palette. Use the storyboard's real concepts.
- Follow storyboard motion cues: progressive numbers, circling a selected value, arrows showing an implication and emphasis while the vocabulary is spoken. Keep author/director directions out of narration.
- Use smooth eased fades, short translations and drawn strokes. Avoid abrupt appearance, distracting movement and hard flashing. Preserve already-visible mathematical steps as the explanation develops.
- All pedagogical containers and heading badges (definition, property, example, verification, synthesis and other content boxes) use the same turquoise #0DBBA1 as the approved example/verification design, with white bodies. This latest user rule overrides the earlier green/orange source-section fills. The blue objective banner remains the reference exception. Preserve semantic colours inside mathematics, e.g. blue multiples/red minimum circle, separately from container styling.
- Keep the font family, weight, size and dark navy colour uniform throughout each title. Fit the complete title without stretching glyphs.
- When explaining an acronym, animate and emphasize the actual letter as it is explained; draw its arrow from that letter to its corresponding full word. Keep letter/arrow/word-initial colours consistent. This is a reusable rule for all acronym explanations, not a decoration under an unrelated centered acronym.
- Add short reflection pauses between ideas and after important results, without changing pitch or unnecessarily slowing spoken words. Preserve existing adequate pauses, retain aligned timings after inserting silence and hold the completed reasoning before transition. Small purposeful number/equation pop-ins are allowed; avoid distracting bounce or motion without pedagogical meaning.
- Prioritize student comprehension: readable text, one explained idea at a time, no arrow crossing the title, matching audio/reveal cues and enough hold time for equations.

Earlier implementation used 72 px type and routed connectors. For the next requested video, verify text fit, straight connector paths and heading entrances in the shared preview and actual render.


Historical fractions export from 2026-11-04 used two 72 px lines and two explanations in red and green. Its verification is in the Digital Lab project reference n3-sem2-vdp3-fractions.md.
