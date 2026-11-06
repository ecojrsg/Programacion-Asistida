# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-06 01:23:54
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-06 01:33:54
"""Play rock-paper-scissors through a Spanish Streamlit interface."""

import random

import streamlit as st

from game import MOVES, determine_winner

st.set_page_config(page_title="Piedra, papel o tijera", page_icon="✂️")
st.title("Piedra, papel o tijera")
st.caption("Elige tu jugada y juega una ronda contra la computadora.")

if "scores" not in st.session_state:
    st.session_state.scores = {"player": 0, "computer": 0, "tie": 0}
    st.session_state.last_round = None

player_move = st.radio(
    "Tu jugada", MOVES, format_func=str.capitalize, horizontal=True
)
if st.button("Jugar ronda", type="primary"):
    computer_move = random.choice(MOVES)
    winner = determine_winner(player_move, computer_move)
    st.session_state.scores[winner] += 1
    st.session_state.last_round = (player_move, computer_move, winner)

if st.session_state.last_round is not None:
    player_move, computer_move, winner = st.session_state.last_round
    st.subheader("Última ronda")
    st.write(f"Tu jugada: **{player_move.capitalize()}**")
    st.write(f"Computadora: **{computer_move.capitalize()}**")
    messages = {
        "player": "Ganaste la ronda.",
        "computer": "La computadora ganó la ronda.",
        "tie": "La ronda terminó en empate.",
    }
    st.info(messages[winner])

st.subheader("Marcador")
for column, result, label in zip(
    st.columns(3),
    ("player", "computer", "tie"),
    ("Tus victorias", "Computadora", "Empates"),
):
    column.metric(label, st.session_state.scores[result])
st.caption("El marcador se conserva mientras mantengas esta sesión abierta.")
