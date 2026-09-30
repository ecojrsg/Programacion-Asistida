from game import ExerciseGenerator, new_game, submit_answer, timeout


SETTINGS = {"n": 100, "x": 5, "z": 10, "starting_gold": 0, "rooms": 9}
CATALOG = {"difficulties": [{"name": "facil", "max_room": 9, "operations": ["sum"], "min": 1, "max": 2, "time_seconds": 15}]}


def test_game_rules():
    generator = ExerciseGenerator(CATALOG)
    state = new_game(SETTINGS, generator)
    assert state["health"] == 100
    assert submit_answer(state, state["exercise"].answer, SETTINGS, generator)
    state = new_game(SETTINGS, generator)
    timeout(state, SETTINGS, generator)
    assert state["health"] == 90
