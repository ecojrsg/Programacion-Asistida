# Third partial - Rock, Paper, Scissors

Author: Jonathan Serna.

A minimal Python/Streamlit game for exercise 5. Choose a move, play against
the computer's random move, and see the result and the three session scores.
The interface is Spanish; source and technical documentation are English.

## Requirements and installation

Python 3.14+ and [uv](https://docs.astral.sh/uv/). From this directory:

```powershell
uv sync --locked
uv run streamlit run app.py
```

Open the local URL printed by Streamlit. Stop with `Ctrl+C`.

Streamlit 1.65.0 is the only application dependency. pytest is a development
dependency. `uv.lock` records the exact versions.

## Use

1. Choose **Piedra**, **Papel**, or **Tijera**.
2. Click **Jugar ronda**. The computer chooses randomly once per click.
3. Read both moves, the result, and **Tus victorias**, **Computadora**,
   and **Empates**.

Changing the selector does not play another round. The last round and scores
survive widget reruns. Scores belong to one browser session; reloading the
page, closing the session, or restarting the server can reset them.

## Tests

```powershell
uv run python -m pytest -v
```

- `tests/test_game.py`: all nine legal pairs and ten invalid-input cases.
- `tests/test_app.py`: each outcome, exactly one point per click, selector
  changes without scoring, repeated rounds, and separate sessions.
- Actual red/green output and unchanged test hashes are in `docs/evidence/`.

## Structure

| Path | Purpose |
| --- | --- |
| `game.py` | Valid moves and `determine_winner`. |
| `app.py` | Native Streamlit controls and session state. |
| `tests/` | Contract and interface checks. |
| `docs/design.md` | Design approved before implementation. |
| `docs/flowchart.mmd`, `docs/flowchart.svg` | Mermaid source and render. |
| `docs/conversation/` | Labeled illustrative dialogue about the exercise. |
| `docs/evidence/` | Real test output and browser screenshots. |
| `docs/verification.md` | Checked requirements and delivery limitations. |

## Troubleshooting

If `streamlit` or `pytest` cannot be found, run `uv sync --locked` and use
the `uv run` commands above. If the port is busy, add `--server.port 8502`
to the Streamlit command. No database or API key is needed to play.
