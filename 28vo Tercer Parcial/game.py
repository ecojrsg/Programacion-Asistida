# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-06 01:21:26
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-06 01:33:54
"""Decide the result of a rock-paper-scissors round."""

MOVES = ("piedra", "papel", "tijera")


def determine_winner(player_move: str, computer_move: str) -> str:
    """Return the winner, or raise ValueError for an invalid move."""
    if player_move not in MOVES or computer_move not in MOVES:
        raise ValueError("Las jugadas deben ser piedra, papel o tijera.")
    if player_move == computer_move:
        return "tie"
    winning_pairs = (
        ("piedra", "tijera"),
        ("papel", "piedra"),
        ("tijera", "papel"),
    )
    if (player_move, computer_move) in winning_pairs:
        return "player"
    return "computer"
