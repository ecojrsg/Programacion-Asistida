from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent


def load_json(path: str | Path) -> dict:
    path = Path(path)
    with path.open(encoding="utf-8") as file:
        return json.load(file)


@dataclass
class Exercise:
    text: str
    answer: int
    time_seconds: int
    difficulty: str


class ExerciseGenerator:
    def __init__(self, catalog: dict):
        self.catalog = catalog["difficulties"]

    def rules_for(self, room: int) -> dict:
        return next(item for item in self.catalog if room <= item["max_room"])

    def generate(self, room: int) -> Exercise:
        rules = self.rules_for(room)
        operation = random.choice(rules["operations"])
        a = random.randint(rules["min"], rules["max"])
        b = random.randint(rules["min"], rules["max"])
        if operation == "sum":
            text, answer = f"{a} + {b}", a + b
        elif operation == "subtraction":
            a, b = max(a, b), min(a, b)
            text, answer = f"{a} - {b}", a - b
        elif operation == "multiplication":
            text, answer = f"{a} × {b}", a * b
        else:
            answer = random.randint(rules["min"], rules["max"])
            text = f"{answer * b} ÷ {b}"
        return Exercise(text, answer, rules["time_seconds"], rules["name"])


def new_game(settings: dict, generator: ExerciseGenerator) -> dict:
    state = {"room": 1, "health": settings["n"], "gold": settings["starting_gold"], "finished": False}
    state["exercise"] = generator.generate(1)
    state["started_at"] = time.time()
    return state


def submit_answer(state: dict, value: int, settings: dict, generator: ExerciseGenerator) -> bool:
    correct = value == state["exercise"].answer
    if correct:
        state["gold"] += state["room"] * 10
        state["room"] += 1
        state["finished"] = state["room"] > settings["rooms"]
    else:
        state["health"] -= settings["x"]
    if not state["finished"]:
        state["exercise"] = generator.generate(state["room"])
        state["started_at"] = time.time()
    return correct


def timeout(state: dict, settings: dict, generator: ExerciseGenerator) -> None:
    state["health"] -= settings["z"]
    if state["health"] > 0:
        state["exercise"] = generator.generate(state["room"])
        state["started_at"] = time.time()
