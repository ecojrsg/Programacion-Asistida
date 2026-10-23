# HTML best practices

Applied to the first version of this exercise.

- Use semantic landmarks, one main heading, native buttons and a native details
  element for the rules. Set the document language to Spanish.
- Keep the board in numerical DOM order, using CSS to place its serpentine path.
  Cells are information, not keyboard controls.
- Label the board, players, die result and game status. Announce complete turns
  through one polite live region, not through animation frames.
- Use text labels and piece numbers alongside color. Decorative SVG and die art
  must be hidden from assistive technology.
- Load local classic scripts with defer, in dependency order. No network request,
  module loader or build step should be necessary to open the game.
- Use textContent for game messages. Do not insert user input as HTML.
- Verify keyboard operation, visible focus, disabled states and small-screen fit.

Review checklist: language, landmarks, labels, script order, local paths,
keyboard behavior and live announcements.
