# CSS best practices

Applied to the first version of this exercise.

- Keep layout and readable fallback styles in styles.css; keep volume, SVG
  finishes and animation styles in visuals/effects.css.
- Define the small palette and repeated dimensions with custom properties.
  Use relative sizing, Grid and media queries instead of device-specific markup.
- Keep the board square and align its cells, routes and pieces to the same plane.
- Use dark text on light surfaces, visible focus and controls at least 44 px tall.
  Do not rely on color alone to distinguish the players.
- Animate transforms and opacity. Avoid a continuous animation loop or animated
  layout properties. Motion should communicate a real action.
- Honor prefers-reduced-motion, including decorative hover transitions.
- Preserve readable numbers and avoid horizontal overflow down to 320 px.
- Consider viewport height as well as width. Center horizontally with automatic
  inline margins, keep content at the top, and preserve natural scrolling when
  rules or a small viewport need extra room.
- Reserve layout space for transformed surfaces and their shadows so they do
  not cover adjacent labels; a transform does not change normal document flow.
- After responsive testing, clear emulation and compare the viewport with the
  actual browser window; a fixed test viewport can leave gray space outside it.

Review checklist: desktop and mobile, number legibility, contrast, focus,
reduced motion, fallback without effects and no idle animation.
