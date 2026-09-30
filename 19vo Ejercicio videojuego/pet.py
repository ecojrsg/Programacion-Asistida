import random


METER_MAX = 100
ROOM_DECAY = 10

ACTIONS = {
    "alimentar": {"label": "🍎 Alimentar", "stat": "well_fed"},
    "jugar": {"label": "🧶 Jugar", "stat": "happiness"},
    "dormir": {"label": "🛏️ Dormir", "stat": "energy"},
}

OFFER_CATALOG = {
    "alimentar": [
        {"name": "Croquetas", "price": 8, "restore": 25},
        {"name": "Comida casera", "price": 16, "restore": 45},
        {"name": "Salmón", "price": 24, "restore": 60},
    ],
    "jugar": [
        {"name": "Pelota", "price": 7, "restore": 20},
        {"name": "Cuerda", "price": 12, "restore": 35},
        {"name": "Puzzle", "price": 18, "restore": 50},
    ],
    "dormir": [
        {"name": "Cojín", "price": 8, "restore": 25},
        {"name": "Cama cómoda", "price": 15, "restore": 45},
        {"name": "Manta térmica", "price": 22, "restore": 60},
    ],
}


def new_pet() -> dict:
    return {stat: METER_MAX for stat in (action["stat"] for action in ACTIONS.values())}


def new_room_offers() -> dict:
    return {
        action: {**random.choice(options), "status": "pending"}
        for action, options in OFFER_CATALOG.items()
    }


def purchase_offer(state: dict, action: str) -> bool:
    offer = state["offers"][action]
    if offer["status"] != "pending" or state["gold"] < offer["price"]:
        return False

    state["gold"] -= offer["price"]
    stat = ACTIONS[action]["stat"]
    state["pet"][stat] = min(METER_MAX, state["pet"][stat] + offer["restore"])
    offer["status"] = "purchased"
    return True


def skip_offer(state: dict, action: str) -> bool:
    offer = state["offers"][action]
    if offer["status"] != "pending":
        return False
    offer["status"] = "skipped"
    return True


def decay_pet(pet: dict) -> None:
    for action in ACTIONS.values():
        stat = action["stat"]
        pet[stat] = max(0, pet[stat] - ROOM_DECAY)
