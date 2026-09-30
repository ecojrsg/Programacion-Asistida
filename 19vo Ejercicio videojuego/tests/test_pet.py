from pet import ACTIONS, new_pet, new_room_offers, purchase_offer, skip_offer


def test_new_pet_and_room_offers_have_all_meters_and_actions():
    assert set(new_pet().values()) == {100}

    offers = new_room_offers()
    assert set(offers) == set(ACTIONS)
    assert all(offer["status"] == "pending" for offer in offers.values())


def test_purchase_deducts_once_restores_related_meter_and_caps_at_100():
    state = {
        "gold": 20,
        "pet": {"well_fed": 90, "energy": 50, "happiness": 60},
        "offers": {
            "alimentar": {"price": 8, "restore": 25, "status": "pending"},
        },
    }

    assert purchase_offer(state, "alimentar")
    assert state["gold"] == 12
    assert state["pet"] == {"well_fed": 100, "energy": 50, "happiness": 60}
    assert not purchase_offer(state, "alimentar")
    assert state["gold"] == 12


def test_unaffordable_offer_stays_pending_and_can_be_skipped():
    state = {
        "gold": 3,
        "pet": new_pet(),
        "offers": {"jugar": {"price": 7, "restore": 20, "status": "pending"}},
    }

    assert not purchase_offer(state, "jugar")
    assert state["gold"] == 3
    assert state["offers"]["jugar"]["status"] == "pending"
    assert skip_offer(state, "jugar")
    assert not purchase_offer(state, "jugar")
    assert state["gold"] == 3
