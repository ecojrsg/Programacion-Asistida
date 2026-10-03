# MVP Plan: Castillo Matemático

## Goal

Build a simple educational Streamlit game in which an adventurer explores a
castle, defeats enemies by solving arithmetic exercises, and collects gold.
The interface stays in Spanish; identifiers and technical documentation use
English.

## Implemented Rules

- The player starts with `n` health points and the configured starting gold.
- Each room contains an enemy and a timed exercise.
- A correct answer awards `room * 10` gold and advances to the next room.
- A wrong answer deducts `x` health points and replaces the current exercise.
- An expired timer deducts `z` health points. A new timed exercise starts in the
  same room if the player still has health.
- Victory occurs after the last room; zero or negative health shows defeat.
- Difficulty increases according to the room ranges in the exercise catalog.
- Subtraction stays nonnegative, and division uses an integer quotient.
- The pet starts with three meters at 100; clearing a room lowers each by 10.
- Each room offers one randomized, priced item per pet action. A pending offer
  can be bought once when affordable or skipped once; offers stay stable during
  wrong answers, timeouts, and reruns in the same room.

## Editable Configuration

- `config/settings.json`: `n` is starting health, `x` is wrong-answer damage,
  `z` is timeout damage, `starting_gold` is initial gold, and `rooms` is the
  number of rooms.
- `config/exercises.json`: difficulty labels, room boundaries, allowed
  operations, number ranges, and time limits. Keep levels ordered and ensure
  they cover all configured rooms.
- Both files are read at the start of each Streamlit script run. A new game
  uses the current settings; existing progress stays in `st.session_state`.

## Existing File Responsibilities

- `app.py`: `main()` loads configuration and routes the session. Small render
  functions handle the welcome screen, timer, status, pet offers, answer form,
  and controls.
- `game.py`: `Exercise` stores an exercise, `ExerciseGenerator` creates it,
  and `new_game()`, `submit_answer()`, and `timeout()` update dictionary state,
  including pet meters and room offers. The private `_start_turn()` helper
  replaces the exercise and resets its timer without changing pet state.
- `tests/test_game.py`: focused regression checks for rules and interface flows.

## Run

Use Python 3.11 or later and run these commands from this exercise directory:

```bash
uv sync
uv run streamlit run app.py
```

## Regression Checks

Use the existing Streamlit testing API and Python's standard library; an
additional test runner is not required:

```bash
uv run python -B -m tests.test_game
```

The checks cover initial state, independent games, answer damage and rewards,
timeouts, fatal damage, victory, difficulty boundaries, all four operations,
pet meters and purchases, stable room offers, and starting, answering,
restarting, exiting, and ending a game in Streamlit. Pet and interface checks
run as part of this same command.

## Possible Future Improvements

Visual combat, treasure types, empty rooms, persistent scores, and more
operations. These are ideas, not part of the current implementation.
