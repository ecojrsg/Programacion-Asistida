# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-06 01:23:54
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-06 01:33:54
"""Check the actual Streamlit screen and its session score."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


@pytest.mark.parametrize("computer_move, result, message", [
    ("tijera", "player", "Ganaste la ronda."),
    ("papel", "computer", "La computadora ganó la ronda."),
    ("piedra", "tie", "La ronda terminó en empate."),
])
def test_round_and_session_score(monkeypatch, computer_move, result, message):
    """Score once per click and preserve the last round across reruns."""
    monkeypatch.setattr("random.choice", lambda moves: computer_move)
    app = AppTest.from_file(str(APP_PATH)).run()
    assert not app.exception
    assert [metric.value for metric in app.metric] == ["0", "0", "0"]

    app.button[0].click().run()
    assert not app.exception
    assert app.info[0].value == message
    assert app.session_state.last_round == ("piedra", computer_move, result)
    assert app.session_state.scores[result] == 1
    assert sum(app.session_state.scores.values()) == 1
    assert any(
        computer_move.capitalize() in text.value for text in app.markdown
    )

    app.radio[0].set_value("papel").run()
    assert app.session_state.scores[result] == 1
    assert sum(app.session_state.scores.values()) == 1
    assert app.session_state.last_round == ("piedra", computer_move, result)
    app.radio[0].set_value("piedra").run()
    app.button[0].click().run()
    assert app.session_state.scores[result] == 2
    assert sum(app.session_state.scores.values()) == 2
    assert [metric.value for metric in app.metric].count("2") == 1

    other_session = AppTest.from_file(str(APP_PATH)).run()
    assert not other_session.exception
    assert sum(other_session.session_state.scores.values()) == 0
    assert other_session.session_state.last_round is None
