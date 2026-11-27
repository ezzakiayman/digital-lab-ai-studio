# Mathematical typesetting

The user approved the second screenshot on 2026-11-10 as the visual reference for all Digital Lab mathematics videos. The exact supplied image is kept locally at `reference/math-typesetting/approved.png`.

The user later corrected the letter shapes in the four-storyboard batch. Use the dedicated Cambria Math bold italic glyphs 𝒙 and 𝒚 (U+1D499 and U+1D49A) in new algebra visuals. CSS italics on ordinary text letters have a different shape. Keep ASCII variables in editable data and map them to the mathematical glyphs at render time. `MathFormula` and `MathVariable` in `src/video/StoryboardVisuals.tsx` implement this rule.

- Use upright numbers, italic variables and a mathematical font with natural glyph proportions. Build exponents as smaller, raised glyphs, fractions with a horizontal bar and radicals with a correctly sized overbar.
- Use the proper symbols for the storyboard’s operations and relations. Examples include −, ×, ÷, ≤ and ≥. Preserve implied multiplication in terms such as 5x and keep signs attached to signed terms during highlights. Use clear space around binary operators.
- Keep operators neutral where the colours identify adjacent terms. In the approved example, 5x is blue, 3y³ is green and the plus sign is black. Apply purposeful semantic colour when the storyboard uses colour to teach an operation or relationship.
- Render editable mathematics from its structure. Check that exponents stay attached to the correct variables, minus signs and fractions are readable, and animation preserves the meaning of partial expressions.

The 55-slide polynomial revision uses `src/video/PolynomialMath.tsx` with structured coefficients and powers from `src/lib/polynomials.ts`. It renders bold Cambria with distinct number, variable, exponent and operator glyphs. This implementation handles the reviewed polynomial expressions. Use the existing fraction component for fractions and an appropriate math renderer for other notation.

