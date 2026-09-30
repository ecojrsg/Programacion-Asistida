from fog import ENEMY, PASS, SPIN_SECONDS, check_room_event, resolve_roulette, start_roulette


class CountingRng:
    def __init__(self, value):
        self.value = value
        self.calls = 0

    def randrange(self, stop):
        assert stop == 3
        self.calls += 1
        return self.value


class OutcomeRng:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    def choice(self, options):
        self.calls += 1
        assert self.result in options
        return self.result


class Generator:
    def __init__(self):
        self.rooms = []

    def generate(self, room):
        self.rooms.append(room)
        return f"exercise-{room}"


def test_fog_chance_is_one_in_three_and_event_is_rolled_once_per_room():
    state = {"room": 1}
    offered_rng, first_none_rng, second_none_rng = (CountingRng(value) for value in (0, 1, 2))

    offered = check_room_event(state, 1, rng=offered_rng)
    assert offered["status"] == "offered"
    assert check_room_event(state, 1, rng=CountingRng(2)) is offered
    assert check_room_event(state, 2, rng=first_none_rng)["status"] == "none"
    assert check_room_event(state, 3, rng=second_none_rng)["status"] == "none"
    assert offered_rng.calls == first_none_rng.calls == second_none_rng.calls == 1


def test_roulette_outcome_survives_reruns_without_rerolling():
    state = {"room": 1}
    chance_rng = CountingRng(0)
    outcome_rng = OutcomeRng(ENEMY)

    event = check_room_event(state, 1, rng=chance_rng)
    assert event["status"] == "offered"
    assert start_roulette(state, 1, rng=outcome_rng, now=100)
    assert not start_roulette(state, 1, rng=OutcomeRng(PASS), now=101)

    assert check_room_event(state, 1, rng=chance_rng) is event
    assert event["result"] == ENEMY
    assert chance_rng.calls == 1
    assert outcome_rng.calls == 1


def test_pass_advances_exactly_one_room_without_combat_gold():
    generator = Generator()
    state = {
        "room": 2,
        "health": 100,
        "gold": 30,
        "finished": False,
        "exercise": "exercise-2",
        "started_at": 100,
        "fog_events": {"2": {"status": "spinning", "result": PASS, "started_at": 100}},
    }

    assert resolve_roulette(state, 2, {"rooms": 5}, generator, now=100 + SPIN_SECONDS + 1) == PASS
    assert state["room"] == 3
    assert state["gold"] == 30
    assert state["exercise"] == "exercise-3"
    assert state["fog_events"]["2"]["status"] == "passed"
    assert generator.rooms == [3]

    assert resolve_roulette(state, 2, {"rooms": 5}, generator, now=110) is None
    assert state["room"] == 3
    assert state["gold"] == 30
    assert generator.rooms == [3]


def test_pass_from_final_room_finishes_the_game():
    state = {
        "room": 5,
        "health": 100,
        "gold": 30,
        "finished": False,
        "exercise": "exercise-5",
        "started_at": 100,
        "fog_events": {"5": {"status": "spinning", "result": PASS, "started_at": 100}},
    }

    assert resolve_roulette(state, 5, {"rooms": 5}, Generator(), now=100 + SPIN_SECONDS + 1) == PASS
    assert state["room"] == 6
    assert state["finished"] is True
    assert state["gold"] == 30


def test_enemy_result_starts_normal_room_encounter_without_advancing():
    generator = Generator()
    exercise = "existing-room-4-exercise"
    state = {
        "room": 4,
        "health": 100,
        "gold": 20,
        "finished": False,
        "exercise": exercise,
        "started_at": 100,
        "fog_events": {"4": {"status": "spinning", "result": ENEMY, "started_at": 100}},
    }
    resolved_at = 100 + SPIN_SECONDS + 1

    assert resolve_roulette(state, 4, {"rooms": 5}, generator, now=resolved_at) == ENEMY
    assert state["fog_events"]["4"]["status"] == "enemy"
    assert state["room"] == 4
    assert state["exercise"] == exercise
    assert state["gold"] == 20
    assert state["started_at"] == resolved_at
    assert generator.rooms == []
