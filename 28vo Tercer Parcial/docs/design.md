# Rock, Paper, Scissors - design for review

Author: Jonathan Serna. Date: 2026-11-06.
Status: approved by the student on 2026-11-06 before writing Python source.

## Goal and scope

Implement exercise 5 of the third partial exam: a Python/Streamlit game that
plays one round against a random computer move and keeps player wins,
computer wins, and ties during the browser session. The interface is Spanish;
identifiers and technical documentation are English.

The chosen solution is two Python modules with Streamlit's native widgets.
A console application would miss the UI requirement; a database or a custom
frontend would add work without meeting another requirement.

## Contract

`determine_winner(player_move: str, computer_move: str) -> str`

- Valid inputs are exactly `piedra`, `papel`, and `tijera`.
- Equal moves return `tie`.
- Rock beats scissors, scissors beats paper, and paper beats rock.
- Return `player` for a player win and `computer` otherwise.
- Raise `ValueError` when either move is invalid. Do not normalize inputs.

## Interface and state

One screen contains a title, a horizontal radio selector, a **Jugar ronda**
button, the last round's two moves and result, and three score metrics.
Use `random.choice` for the computer, only when the button is clicked.
Keep the score and last round in `st.session_state`; changing the selector
does not play a round or clear the result. Reloading/closing the session
starts a new score. There is no database, login, history, export, or animation.

## Files and responsibilities

| Path | Purpose |
| --- | --- |
| `game.py` | Pure winner function and valid moves. |
| `app.py` | Streamlit UI, random choice, and session score. |
| `tests/test_game.py` | Parametrized tests for nine valid pairs and invalid inputs. |
| `tests/test_app.py` | Built-in Streamlit AppTest for score and rerun behavior. |
| `pyproject.toml`, `uv.lock` | Python version and reproducible dependencies. |
| `README.md` | Install, run, test, and known session limitation. |
| `docs/flowchart.mmd`, `docs/flowchart.svg` | Mermaid source and rendered flowchart. |
| `docs/conversation/` | Labeled illustrative dialogue about the exercise. |
| `docs/evidence/` | Actual red/green output, test source snapshot, UI screenshots. |

All implementation and supporting material stay inside this exercise.
The final report will follow the PDFs ejercicios cover style and remain
uncommitted until the student approves it.

## Dependencies

Use Python 3.14, already installed in the repository environment.
Streamlit 1.65.0 is already installed in exercise 21 and is required by the exam.
Propose pytest as the sole additional development dependency, because the
course uses its parametrization and exception assertions. Do not install it
or create dependency manifests before approval. PDF tools belong to the
authoring environment and are not game dependencies.

## Implementation and evidence plan

1. Obtain actual approval of this design and the pytest development dependency.
2. Write the tests from the contract and a `NotImplementedError` stub. Run
   pytest and preserve the real failing output, source, and screenshots.
3. Implement the smallest winner function without changing expected values.
   Preserve the passing output and screenshots. Verify test-file hashes.
4. Add the Streamlit screen. Test each outcome, score persistence, changing
   selection without scoring, and isolation between sessions.
5. Capture the running UI and render the Mermaid diagram.
6. Commit and push the working project using git with gh authentication.
7. Create the Spanish PDF with diagram, illustrative dialogue, actual TDD and
   UI screenshots, source link, setup instructions, and verification results.
   Present it for approval before the second commit.

## Delivery integrity

The simulated dialogue is an illustrative summary of prompts, decisions,
and outcomes, explicitly labeled as such.
Do not invent student approvals, tool use, test runs, or screenshots.
The exam's email address is a delivery instruction for the student; this task
does not authorize sending email.
