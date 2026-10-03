# @Author: Jonathan Serna
# @Date:   2026-09-28 16:41:21
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-02 11:20:56

"""Generate arithmetic exercises and update dictionary game state."""

from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass
from pathlib import Path

from pet import decay_pet, new_pet, new_room_offers


def load_json(path: str | Path) -> dict:
    """Read UTF-8 JSON, relative to the current working directory."""
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)


@dataclass
class Exercise:
    """Store an operation, answer, time limit, and difficulty."""

    text: str
    answer: int
    time_seconds: int
    difficulty: str


class ExerciseGenerator:
    """Generate exercises using configured room difficulty levels."""

    def __init__(self, catalog: dict) -> None:
        """Keep the difficulty levels in their configured order."""
        self.catalog = catalog["difficulties"]

    def rules_for(self, room: int) -> dict:
        """Return the first difficulty level covering this room."""
        return next(item for item in self.catalog if room <= item["max_room"])

    def generate(self, room: int) -> Exercise:
        """Generate an operation using the current room's rules."""
        rules = self.rules_for(room)
        operation = random.choice(rules["operations"])
        left = random.randint(rules["min"], rules["max"])
        right = random.randint(rules["min"], rules["max"])
        if operation == "sum":
            text, answer = f"{left} + {right}", left + right
        elif operation == "subtraction":
            left, right = max(left, right), min(left, right)
            text, answer = f"{left} - {right}", left - right
        elif operation == "multiplication":
            text, answer = f"{left} × {right}", left * right
        else:
            # Choose the quotient first to keep division exact.
            answer = random.randint(rules["min"], rules["max"])
            text = f"{answer * right} ÷ {right}"
        return Exercise(text, answer, rules["time_seconds"], rules["name"])


def _start_turn(state: dict, generator: ExerciseGenerator) -> None:
    """Start a timed exercise in the current room."""
    state["exercise"] = generator.generate(state["room"])
    state["started_at"] = time.time()


def new_game(settings: dict, generator: ExerciseGenerator) -> dict:
    """Create a game with configured health, gold, pet meters, and offers."""
    state = {
        "room": 1,
        "health": settings["n"],
        "gold": settings["starting_gold"],
        "finished": False,
        "pet": new_pet(),
        "offers": new_room_offers(),
    }
    _start_turn(state, generator)
    return state


def submit_answer(
    state: dict, value: int, settings: dict, generator: ExerciseGenerator
) -> bool:
    """Apply answer rewards or damage and return correctness.

    A correct answer decays pet meters once and refreshes offers on advancement.
    A new timed exercise starts unless the last room was completed.
    """
    correct = value == state["exercise"].answer
    if correct:
        decay_pet(state["pet"])
        state["gold"] += state["room"] * 10
        state["room"] += 1
        state["finished"] = state["room"] > settings["rooms"]
    else:
        state["health"] -= settings["x"]
    if not state["finished"]:
        if correct:
            state["offers"] = new_room_offers()
        _start_turn(state, generator)
    return correct


def timeout(state: dict, settings: dict, generator: ExerciseGenerator) -> None:
    """Apply timeout damage; start a turn only if health remains."""
    state["health"] -= settings["z"]
    if state["health"] > 0:
        _start_turn(state, generator)
