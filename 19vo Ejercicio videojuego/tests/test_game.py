# -*- coding: utf-8 -*-
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-02 10:59:44

"""Check game rules and the Spanish Streamlit interface."""

from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from game import ExerciseGenerator, load_json, new_game, submit_answer, timeout
from pet import OFFER_CATALOG
from .test_pet import (
    test_new_pet_and_room_offers_have_all_meters_and_actions,
    test_purchase_deducts_once_restores_related_meter_and_caps_at_100,
    test_unaffordable_offer_stays_pending_and_can_be_skipped,
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


def find_button(app: AppTest, label: str):
    """Return the first app button with the given label."""
    return next(button for button in app.button if button.label == label)


def test_load_json() -> None:
    """Read configuration using both string and Path inputs."""
    path = Path("config/settings.json")
    assert load_json(str(path)) == load_json(path)
    assert SETTINGS.keys() <= load_json(path).keys()


def test_new_game() -> None:
    """Create independent games with configured values and offers."""
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
    assert set(state["pet"].values()) == {100}
    assert set(state["offers"]) == {"alimentar", "jugar", "dormir"}
    for action, offer in state["offers"].items():
        priced_offer = {
            key: offer[key] for key in ("name", "price", "restore")
        }
        assert priced_offer in OFFER_CATALOG[action]
        assert offer["status"] == "pending"


def test_correct_answer() -> None:
    """Reward and advance a room while decaying the pet once."""
    generator = ExerciseGenerator(CATALOG)
    state = new_game(SETTINGS, generator)
    assert state["health"] == 100
    assert set(state["pet"].values()) == {100}
    assert set(state["offers"]) == {"alimentar", "jugar", "dormir"}
    offers = state["offers"]
    state["room"] = 3
    exercise = state["exercise"]
    with patch("game.time.time", return_value=200):
        assert submit_answer(state, exercise.answer, SETTINGS, generator)
    assert state["room"] == 4
    assert state["gold"] == 30
    assert state["health"] == SETTINGS["n"]
    assert state["exercise"] is not exercise
    assert state["started_at"] == 200
    assert set(state["pet"].values()) == {90}
    assert not state["finished"]
    assert state["offers"] is not offers
    assert all(
        offer["status"] == "pending" for offer in state["offers"].values()
    )


def test_pet_decays_once_per_cleared_room_but_not_on_wrong_answers() -> None:
    """Decay meters only on room clears and keep offers during timeouts."""
    generator = ExerciseGenerator(CATALOG)
    state = new_game(SETTINGS, generator)
    offers = state["offers"]

    assert not submit_answer(
        state, state["exercise"].answer + 1, SETTINGS, generator
    )
    assert set(state["pet"].values()) == {100}
    assert state["offers"] is offers

    timeout(state, SETTINGS, generator)
    assert set(state["pet"].values()) == {100}
    assert state["offers"] is offers

    for expected_meter in (90, 80):
        previous_offers = state["offers"]
        assert submit_answer(state, state["exercise"].answer, SETTINGS, generator)
        assert set(state["pet"].values()) == {expected_meter}
        assert state["offers"] is not previous_offers
        assert all(
            offer["status"] == "pending"
            for offer in state["offers"].values()
        )


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


def test_app_answers() -> None:
    """Submit correct and incorrect answers through the Spanish form."""
    settings = load_json("config/settings.json")
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    assert app.title[0].value == "🏰 Castillo Matemático"
    app.button[0].click().run()
    app.number_input[0].set_value(app.session_state["game"]["exercise"].answer)
    find_button(app, "Atacar").click().run()
    assert app.session_state["game"]["room"] == 2
    assert app.session_state["game"]["gold"] == settings["starting_gold"] + 10
    app.number_input[0].set_value(
        app.session_state["game"]["exercise"].answer + 1
    )
    find_button(app, "Atacar").click().run()
    assert app.session_state["game"]["health"] == settings["n"] - settings["x"]
    assert app.session_state["game"]["room"] == 2
    assert not app.exception


def test_app_pet_offers() -> None:
    """Keep offers stable on timeout and process pet actions in the UI."""
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    app.button[0].click().run()
    state = app.session_state["game"]
    original_offers = {
        action: offer.copy() for action, offer in state["offers"].items()
    }
    original_pet = state["pet"].copy()
    state["started_at"] -= state["exercise"].time_seconds + 1
    app.run()
    assert state["offers"] == original_offers
    assert state["pet"] == original_pet
    assert not app.exception

    state["gold"] = 7
    state["pet"]["well_fed"] = 50
    state["pet"]["happiness"] = 50
    state["offers"].update(
        {
            "alimentar": {
                "name": "Croquetas",
                "price": 8,
                "restore": 25,
                "status": "pending",
            },
            "jugar": {
                "name": "Pelota",
                "price": 12,
                "restore": 20,
                "status": "pending",
            },
            "dormir": {
                "name": "Cojín",
                "price": 16,
                "restore": 25,
                "status": "pending",
            },
        }
    )
    app.run()
    buy_button = find_button(app, "Comprar · 8 🪙")
    assert buy_button.proto.disabled
    state["gold"] = 8
    app.run()
    find_button(app, "Comprar · 8 🪙").click().run()
    assert state["gold"] == 0
    assert state["pet"]["well_fed"] == 75
    assert state["offers"]["alimentar"]["status"] == "purchased"
    find_button(app, "Omitir").click().run()
    assert state["offers"]["jugar"]["status"] == "skipped"
    assert state["pet"]["happiness"] == 50
    assert not app.exception


def test_app_controls() -> None:
    """Restart a changed game and then return to the welcome screen."""
    settings = load_json("config/settings.json")
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    app.button[0].click().run()
    app.session_state["game"]["health"] = 1
    app.session_state["game"]["gold"] = 80
    find_button(app, "Reiniciar partida").click().run()
    assert app.session_state["game"]["health"] == settings["n"]
    assert app.session_state["game"]["gold"] == settings["starting_gold"]
    assert app.session_state["game"]["room"] == 1
    find_button(app, "Salir de la partida").click().run()
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
        test_new_pet_and_room_offers_have_all_meters_and_actions,
        test_purchase_deducts_once_restores_related_meter_and_caps_at_100,
        test_unaffordable_offer_stays_pending_and_can_be_skipped,
        test_pet_decays_once_per_cleared_room_but_not_on_wrong_answers,
        test_app_answers,
        test_app_pet_offers,
        test_app_controls,
        test_app_timeout,
        test_app_end_states,
    )
    for check in checks:
        check()
    print(f"{len(checks)} regression checks passed.")


if __name__ == "__main__":
    main()
