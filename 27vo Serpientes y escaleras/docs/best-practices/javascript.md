# JavaScript best practices

Applied to the first version of this exercise.

- Keep pure rules and the board data in game.js, DOM interaction in script.js,
  and decorative behavior in visuals/effects.js.
- Use one board map for the rules and SVG. Receive a die value in the rule
  function so tests can reproduce complete turns without random results.
- Keep functions small and names descriptive. Avoid classes, event buses,
  dependencies and abstractions that this game does not need.
- Validate die values and reject turns before starting or after winning.
  Return a new state instead of mutating the previous state.
- Block concurrent actions while a turn is being presented. Always restore the
  controls, even if the optional visual layer fails or times out.
- Keep the recovery deadline longer than the complete die-and-piece sequence;
  after cancellation, check the animation generation before changing the pose.
- Reveal a die result only after its visual roll settles; retain a final-state
  fallback when the optional effect fails, is absent or exceeds its deadline.
- Use textContent and native DOM methods. Keep decorative SVG numeric and local.
- Respect reduced motion and remove any animation when it finishes or expires.
- Leave a small deterministic, runnable check for the rules. Test behavior and
  edge cases, not private implementation details.

Review checklist: exact victory, overshoot, jumps, alternation, reset, invalid
turns, double clicks, visual failure and console errors.
