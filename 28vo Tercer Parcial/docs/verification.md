# Verification and delivery record

Author: Jonathan Serna. Date: 2026-11-06.

## Requirements checked

| Exam item | Evidence |
| --- | --- |
| Design before code | `design.md`. |
| Mermaid flowchart | `flowchart.mmd`, `flowchart.svg`, `flowchart.png`. |
| Python and Streamlit | `game.py`, `app.py`, locked project dependencies. |
| Play one random round and show both moves/result | `evidence/ui-player.png`, `ui-computer.png`, `ui-tie.png`. |
| Three session counters | All UI screenshots and `tests/test_app.py`. |
| Required winner function and ValueError | `tests/test_game.py`: nine valid pairs and ten invalid cases. |
| TDD red then green | Actual `tdd-red.txt` (19 failed) and `tdd-green.txt` (19 passed). |
| Test code and execution screenshots | `evidence/tdd-red.png` and `tdd-green.png` show unchanged source and saved real output. |
| Requested simulation | `conversation/illustrative-dialogue.md`, labeled as an example. |
| Working source link | Repository link recorded in the PDF after the first push. |

## Results

The complete suite passed: 22 tests, including three Streamlit AppTest cases.
The TDD contract test has the same SHA-256 in both stages. The implementation
changed; no expected value, `skip`, or `xfail` was introduced to make it pass.
The final readability pass preserves the same public contract.

Actual random browser play reached all three results in eight rounds.
Screenshots were taken from the running application without forcing outcomes.
`browser-rounds.txt` preserves the observed results and scoreboard values.
The TDD screenshots are browser views of the actual saved pytest output,
not photographs of a native terminal. The complete original text is included.

## Limits and outstanding delivery actions

- The scoreboard is intentionally per session, without persistence.
- The illustrative dialogue is a teaching example.
- The PDF is produced after the first project push and requires student
  approval before its second commit.
- No email has been sent. The exam mentions email submission; the user asked
  for the document and repository work, not sending email.

## Sources consulted

- The supplied third partial exam, exercise 5, page 5.
- The supplied module 6 slides: specification-based tests and red/green/refactor.
- Existing exercise PDFs for the cover and evidence-oriented report format.
- [Streamlit session state](https://docs.streamlit.io/develop/concepts/architecture/session-state).
- [Streamlit AppTest](https://docs.streamlit.io/develop/concepts/app-testing/cheat-sheet).
- [Mermaid rendering API](https://mermaid.js.org/config/usage.html).
