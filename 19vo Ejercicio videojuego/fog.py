from __future__ import annotations

import random
import time

SPIN_SECONDS = 2.4
PASS = "Pase libre"
ENEMY = "Enemigo"


def check_room_event(state: dict, room: int, rng=None) -> dict:
    """Roll once per room and keep the result in the game's session state."""
    events = state.setdefault("fog_events", {})
    key = str(room)
    if key not in events:
        rng = random if rng is None else rng
        events[key] = {"status": "offered" if rng.randrange(3) == 0 else "none"}
    return events[key]


def start_roulette(state: dict, room: int, rng=None, now: float | None = None) -> bool:
    event = state.setdefault("fog_events", {}).get(str(room))
    if not event or event["status"] != "offered":
        return False

    rng = random if rng is None else rng
    event.update(
        status="spinning",
        result=rng.choice((PASS, ENEMY)),
        started_at=time.time() if now is None else now,
    )
    return True


def resolve_roulette(
    state: dict,
    room: int,
    settings: dict,
    generator,
    now: float | None = None,
) -> str | None:
    event = state.setdefault("fog_events", {}).get(str(room))
    if not event or event["status"] != "spinning":
        return None

    now = time.time() if now is None else now
    if now - event["started_at"] < SPIN_SECONDS:
        return None

    result = event["result"]
    event["status"] = "passed" if result == PASS else "enemy"
    event["resolved_at"] = now
    state["started_at"] = now

    if result == PASS:
        state["fog_notice"] = {"room": room, "result": PASS}
        state["room"] = room + 1
        state["finished"] = state["room"] > settings["rooms"]
        if not state["finished"]:
            state["exercise"] = generator.generate(state["room"])

    return result
