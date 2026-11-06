# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-06 01:21:26
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-06 01:21:26
"""Check the winner contract independently of the implementation."""

import pytest

from game import determine_winner


@pytest.mark.parametrize("player_move, computer_move, expected", [
    ("piedra", "piedra", "tie"),
    ("piedra", "papel", "computer"),
    ("piedra", "tijera", "player"),
    ("papel", "piedra", "player"),
    ("papel", "papel", "tie"),
    ("papel", "tijera", "computer"),
    ("tijera", "piedra", "computer"),
    ("tijera", "papel", "player"),
    ("tijera", "tijera", "tie"),
])
def test_determine_winner(player_move, computer_move, expected):
    """Check every valid pair against the rules."""
    assert determine_winner(player_move, computer_move) == expected


@pytest.mark.parametrize("invalid_move", ["", "lagarto", "Piedra", None, []])
@pytest.mark.parametrize("position", ["player", "computer"])
def test_invalid_move(invalid_move, position):
    """Reject an invalid value in either position with ValueError."""
    player_move = invalid_move if position == "player" else "piedra"
    computer_move = invalid_move if position == "computer" else "piedra"
    with pytest.raises(ValueError):
        determine_winner(player_move, computer_move)
