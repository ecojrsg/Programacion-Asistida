# -*- coding: utf-8 -*-
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-02 18:40:22

"""Check game rules and the Spanish Streamlit interface."""

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from game import ExerciseGenerator, load_json, new_game, submit_answer, timeout
from wordle import (
    ABSENT,
    CORRECT,
    MAX_ATTEMPTS,
    MAX_WORD_LENGTH,
    MIN_WORD_LENGTH,
    PRESENT,
    SPANISH_WORDS,
    evaluate_guess as evaluate_wordle_guess,
    new_game as new_wordle_game,
    submit_guess as submit_wordle_guess,
)


SETTINGS = {"n": 100, "x": 5, "z": 10, "starting_gold": 0, "rooms": 9}
CATALOG = {
    "difficulties": [
        {
            "name": "facil",
            "max_room": 9,
            "operations": ["sum"],
            "min": 1,
            "max": 2,
            "time_seconds": 15,
        }
    ]
}
APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def click_app_button(app: AppTest, label: str) -> None:
    """Click a Streamlit button by its visible label."""
    for button in app.button:
        if button.label == label:
            button.click().run()
            return
    raise AssertionError(f"Button not found: {label}")


def start_wordle_app() -> AppTest:
    """Start a game and open its Wordle joker."""
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    click_app_button(app, "Comenzar partida")
    click_app_button(app, "🃏 Usar comodín: Wordle")
    return app


def test_load_json() -> None:
    """Read configuration using both string and Path inputs."""
    path = Path("config/settings.json")
    assert load_json(str(path)) == load_json(path)
    assert SETTINGS.keys() <= load_json(path).keys()


def test_new_game() -> None:
    """Create independent games with the configured initial values."""
    generator = ExerciseGenerator(CATALOG)
    with patch("game.time.time", return_value=100):
        state = new_game(SETTINGS, generator)
        other = new_game(SETTINGS, generator)
    assert state["room"] == 1
    assert state["health"] == SETTINGS["n"]
    assert state["gold"] == SETTINGS["starting_gold"]
    assert not state["finished"]
    assert state["started_at"] == 100
    assert state is not other
    assert state["exercise"] is not other["exercise"]


def test_correct_answer() -> None:
    """Reward the current room and start the next timed exercise."""
    generator = ExerciseGenerator(CATALOG)
    state = new_game(SETTINGS, generator)
    state["room"] = 3
    exercise = state["exercise"]
    with patch("game.time.time", return_value=200):
        assert submit_answer(state, exercise.answer, SETTINGS, generator)
    assert state["room"] == 4
    assert state["gold"] == 30
    assert state["health"] == SETTINGS["n"]
    assert state["exercise"] is not exercise
    assert state["started_at"] == 200
    assert not state["finished"]


def test_wrong_answer() -> None:
    """Deduct answer damage without changing the room or gold."""
    generator = ExerciseGenerator(CATALOG)
    state = new_game(SETTINGS, generator)
    exercise = state["exercise"]
    with patch("game.time.time", return_value=200):
        assert not submit_answer(
            state, exercise.answer + 1, SETTINGS, generator
        )
    assert state["health"] == SETTINGS["n"] - SETTINGS["x"]
    assert state["room"] == 1
    assert state["gold"] == SETTINGS["starting_gold"]
    assert state["exercise"] is not exercise
    assert state["started_at"] == 200


def test_wrong_answer_defeat() -> None:
    """Preserve the turn reset after a fatal wrong answer."""
    generator = ExerciseGenerator(CATALOG)
    state = new_game(SETTINGS, generator)
    state["health"] = SETTINGS["x"]
    exercise = state["exercise"]
    with patch("game.time.time", return_value=200):
        submit_answer(state, exercise.answer + 1, SETTINGS, generator)
    assert state["health"] == 0
    assert state["exercise"] is not exercise
    assert state["started_at"] == 200
    assert not state["finished"]


def test_timeout() -> None:
    """Apply timeout damage and restart the current room's timer."""
    generator = ExerciseGenerator(CATALOG)
    state = new_game(SETTINGS, generator)
    exercise = state["exercise"]
    with patch("game.time.time", return_value=200):
        timeout(state, SETTINGS, generator)
    assert state["health"] == SETTINGS["n"] - SETTINGS["z"]
    assert state["room"] == 1
    assert state["gold"] == SETTINGS["starting_gold"]
    assert state["exercise"] is not exercise
    assert state["started_at"] == 200


def test_timeout_defeat() -> None:
    """Keep the last exercise when timeout damage leaves no health."""
    generator = ExerciseGenerator(CATALOG)
    for health in (SETTINGS["z"], SETTINGS["z"] - 1):
        state = new_game(SETTINGS, generator)
        state["health"] = health
        exercise, started_at = state["exercise"], state["started_at"]
        timeout(state, SETTINGS, generator)
        assert state["health"] == health - SETTINGS["z"]
        assert state["exercise"] is exercise
        assert state["started_at"] == started_at


def test_game_rules() -> None:
    """Complete every room without creating a turn after victory."""
    generator = ExerciseGenerator(CATALOG)
    state = new_game(SETTINGS, generator)
    for room in range(1, SETTINGS["rooms"] + 1):
        assert state["room"] == room
        exercise, started_at = state["exercise"], state["started_at"]
        assert submit_answer(state, exercise.answer, SETTINGS, generator)
    assert state["finished"]
    assert state["room"] == SETTINGS["rooms"] + 1
    assert state["health"] == SETTINGS["n"]
    assert state["gold"] == 10 * sum(range(1, SETTINGS["rooms"] + 1))
    assert state["exercise"] is exercise
    assert state["started_at"] == started_at


def test_difficulty() -> None:
    """Select the configured level at both ends of each room range."""
    generator = ExerciseGenerator(load_json("config/exercises.json"))
    room = 1
    for level in generator.catalog:
        assert generator.rules_for(room) is level
        assert generator.rules_for(level["max_room"]) is level
        room = level["max_room"] + 1


def test_generated_operations() -> None:
    """Generate correct expressions for all four operations."""
    cases = (
        ("sum", [6, 2], "6 + 2", 8),
        ("subtraction", [2, 6], "6 - 2", 4),
        ("multiplication", [6, 2], "6 × 2", 12),
        ("division", [6, 2, 3], "6 ÷ 2", 3),
    )
    for operation, values, text, answer in cases:
        level = dict(CATALOG["difficulties"][0], operations=[operation], max=6)
        generator = ExerciseGenerator({"difficulties": [level]})
        with patch("game.random.randint", side_effect=values):
            exercise = generator.generate(1)
        assert exercise.text == text
        assert exercise.answer == answer
        assert exercise.time_seconds == level["time_seconds"]
        assert exercise.difficulty == level["name"]


def test_wordle_rules() -> None:
    """Check Spanish target lengths, guesses, and six-attempt outcomes."""
    assert SPANISH_WORDS
    assert all(
        MIN_WORD_LENGTH <= len(word) <= MAX_WORD_LENGTH
        for word in SPANISH_WORDS
    )
    with patch("wordle.random.choice", return_value="biblioteca"):
        assert new_wordle_game()["target"] == "biblioteca"
    assert len(new_wordle_game("arbol")["target"]) == MIN_WORD_LENGTH
    assert len(new_wordle_game("biblioteca")["target"]) == MAX_WORD_LENGTH

    checks = TestCase()
    with checks.assertRaisesRegex(ValueError, "entre 5 y 10"):
        new_wordle_game("gato")
    with checks.assertRaisesRegex(ValueError, "entre 5 y 10"):
        new_wordle_game("abcdefghijk")

    game = new_wordle_game("papel")
    with checks.assertRaisesRegex(ValueError, "5 letras"):
        submit_wordle_guess(game, "animal")
    with checks.assertRaisesRegex(ValueError, "lista"):
        submit_wordle_guess(game, "xxxxx")
    assert game["guesses"] == []

    winning_game = new_wordle_game("papel")
    assert submit_wordle_guess(winning_game, "papel") == [CORRECT] * 5
    assert winning_game["status"] == "won"

    losing_game = new_wordle_game("papel")
    for attempt in range(MAX_ATTEMPTS):
        submit_wordle_guess(losing_game, "barco")
        expected = "lost" if attempt == MAX_ATTEMPTS - 1 else "playing"
        assert losing_game["status"] == expected
    assert len(losing_game["guesses"]) == MAX_ATTEMPTS
    with checks.assertRaisesRegex(ValueError, "ya terminó"):
        submit_wordle_guess(losing_game, "papel")


def test_wordle_feedback() -> None:
    """Check duplicate-aware feedback and Spanish accent normalization."""
    assert evaluate_wordle_guess("papel", "palpa") == [
        CORRECT, CORRECT, PRESENT, PRESENT, ABSENT,
    ]
    assert evaluate_wordle_guess("perro", "rrrra") == [
        ABSENT, ABSENT, CORRECT, CORRECT, ABSENT,
    ]

    game = new_wordle_game("arbol")
    assert submit_wordle_guess(game, "ÁRBOL") == [CORRECT] * 5
    assert game["status"] == "won"
    enye_game = new_wordle_game("montaña")
    assert submit_wordle_guess(enye_game, "montaña") == [CORRECT] * 7
    assert enye_game["status"] == "won"


def test_app_answers() -> None:
    """Submit correct and incorrect answers through the Spanish form."""
    settings = load_json("config/settings.json")
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    assert app.title[0].value == "🏰 Castillo Matemático"
    app.button[0].click().run()
    app.number_input[0].set_value(app.session_state["game"]["exercise"].answer)
    app.button[0].click().run()
    assert app.session_state["game"]["room"] == 2
    assert app.session_state["game"]["gold"] == settings["starting_gold"] + 10
    app.number_input[0].set_value(
        app.session_state["game"]["exercise"].answer + 1
    )
    app.button[0].click().run()
    assert app.session_state["game"]["health"] == settings["n"] - settings["x"]
    assert app.session_state["game"]["room"] == 2
    assert not app.exception


def test_app_controls() -> None:
    """Restart a changed game and then return to the welcome screen."""
    settings = load_json("config/settings.json")
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    click_app_button(app, "Comenzar partida")
    app.session_state["game"]["health"] = 1
    app.session_state["game"]["gold"] = 80
    click_app_button(app, "Reiniciar partida")
    assert app.session_state["game"]["health"] == settings["n"]
    assert app.session_state["game"]["gold"] == settings["starting_gold"]
    assert app.session_state["game"]["room"] == 1
    click_app_button(app, "Salir de la partida")
    assert app.session_state["game"] is None
    assert app.button[0].label == "Comenzar partida"
    assert not app.exception


def test_app_timeout() -> None:
    """Apply expired-turn damage until the interface shows defeat."""
    settings = load_json("config/settings.json")
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    app.button[0].click().run()
    state = app.session_state["game"]
    state["started_at"] -= state["exercise"].time_seconds + 1
    app.run()
    assert state["health"] == settings["n"] - settings["z"]
    assert state["room"] == 1
    state["health"] = settings["z"]
    state["started_at"] -= state["exercise"].time_seconds + 1
    app.run()
    assert state["health"] == 0
    assert not app.number_input
    assert app.error[0].value == (
        "Has quedado sin vida. El castillo te derrotó."
    )
    assert not app.exception


def test_app_end_states() -> None:
    """Render defeat and victory without showing an answer form."""
    settings = load_json("config/settings.json")
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    app.button[0].click().run()
    state = app.session_state["game"]
    state["health"] = 0
    app.run()
    assert app.error[0].value == (
        "Has quedado sin vida. El castillo te derrotó."
    )
    assert not app.number_input
    state["health"] = settings["n"]
    state["room"] = settings["rooms"] + 1
    state["finished"] = True
    app.run()
    assert app.success[0].value == (
        f"¡Victoria! Reuniste {state['gold']} monedas."
    )
    assert not app.number_input
    assert not app.exception


def test_app_wordle_pause_and_cancel() -> None:
    """Pause combat time while Wordle is open and resume on cancellation."""
    settings = load_json("config/settings.json")
    app = start_wordle_app()
    state = app.session_state["game"]
    state["started_at"] = 1000
    app.session_state["wordle_started_at"] = 1005

    with patch("time.time", return_value=1010):
        app.run()
        assert app.session_state["wordle_active"]
        assert state["started_at"] == 1000
        assert state["health"] == settings["n"]
        click_app_button(app, "Cancelar comodín y volver al castillo")

    assert state["started_at"] == 1005
    assert state["health"] == settings["n"]
    assert not app.session_state["wordle_active"]
    assert app.session_state["wordle_game"] is None
    assert "wordle_started_at" not in app.session_state
    assert not app.exception


def test_app_wordle_win_and_loss_returns() -> None:
    """Show Wordle outcomes and return to the castle from both states."""
    for outcome in ("won", "lost"):
        app = start_wordle_app()
        game = app.session_state["wordle_game"]
        game["target"] = "papel"
        guesses = (
            ("papel",)
            if outcome == "won"
            else ("barco",) * MAX_ATTEMPTS
        )
        for guess in guesses:
            app.text_input[0].set_value(guess)
            click_app_button(app, "Probar palabra")

        assert game["status"] == outcome
        if outcome == "won":
            assert app.success[0].value == (
                "¡Adivinaste! La palabra era **papel**."
            )
        else:
            assert app.error[0].value == (
                "Se acabaron los intentos. La palabra era **papel**."
            )
        click_app_button(app, "Volver al castillo")
        assert not app.session_state["wordle_active"]
        assert app.session_state["wordle_game"] is None
        assert not app.exception


def main() -> None:
    """Run regression checks with the existing dependencies."""
    checks = (
        test_load_json,
        test_new_game,
        test_correct_answer,
        test_wrong_answer,
        test_wrong_answer_defeat,
        test_timeout,
        test_timeout_defeat,
        test_game_rules,
        test_difficulty,
        test_generated_operations,
        test_wordle_rules,
        test_wordle_feedback,
        test_app_answers,
        test_app_controls,
        test_app_timeout,
        test_app_end_states,
        test_app_wordle_pause_and_cancel,
        test_app_wordle_win_and_loss_returns,
    )
    for check in checks:
        check()
    print(f"{len(checks)} regression checks passed.")


if __name__ == "__main__":
    main()
