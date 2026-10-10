# @Author: Jonathan Serna
# @Date:   2026-09-28 16:41:21
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-02 11:20:46

"""Render the Spanish interface for the math castle game."""

import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from game import ExerciseGenerator, load_json, new_game, submit_answer, timeout


def render_start(settings: dict, generator: ExerciseGenerator) -> None:
    """Show the welcome message and start button."""
    st.info("Tu aventura comienza con 100 puntos de vida.")
    if st.button("Comenzar partida", type="primary"):
        st.session_state.game = new_game(settings, generator)
        st.rerun()


def refresh_timer(
    state: dict, settings: dict, generator: ExerciseGenerator
) -> int:
    """Refresh the active timer, rerunning the app when time expires.

    Returns:
        Seconds remaining in the current turn.
    """
    elapsed = int(time.time() - state["started_at"])
    remaining = state["exercise"].time_seconds - elapsed
    if remaining <= 0:
        timeout(state, settings, generator)
        st.warning(
            f"¡Tiempo agotado! El enemigo infligió {settings['z']} de daño."
        )
        st.rerun()
    st_autorefresh(interval=1000, key="clock")
    return remaining


def render_status(state: dict, settings: dict) -> None:
    """Show health, gold, and room progress."""
    st.metric("❤️ Vida", state["health"])
    st.metric("🪙 Oro", state["gold"])
    st.subheader("🗺️ Mapa")
    rooms = [
        f"🚪 {room}" if room >= state["room"] else "✅"
        for room in range(1, settings["rooms"] + 1)
    ]
    st.write(" → ".join(rooms))


def render_round(
    state: dict, settings: dict, generator: ExerciseGenerator, remaining: int
) -> None:
    """Show the timed exercise and handle a submitted answer."""
    exercise = state["exercise"]
    st.subheader(f"Enemigo de la habitación {state['room']}")
    st.write(f"Operación ({exercise.difficulty}): **{exercise.text} = ?**")
    st.progress(
        remaining / exercise.time_seconds,
        text=f"Tiempo restante: {remaining}s",
    )
    with st.form("answer"):
        answer = st.number_input("Tu respuesta", step=1, format="%d")
        if not st.form_submit_button("Atacar"):
            return
        if submit_answer(state, int(answer), settings, generator):
            st.success("¡Correcto! Enemigo derrotado.")
        else:
            st.error(f"Respuesta incorrecta. Pierdes {settings['x']} de vida.")
        st.rerun()


def render_controls(settings: dict, generator: ExerciseGenerator) -> None:
    """Show the exit and restart buttons in their original columns."""
    exit_col, restart_col = st.columns(2)
    with exit_col:
        if st.button("Salir de la partida"):
            st.session_state.game = None
            st.rerun()
    with restart_col:
        if st.button("Reiniciar partida"):
            st.session_state.game = new_game(settings, generator)
            st.rerun()


def render_game(
    state: dict, settings: dict, generator: ExerciseGenerator
) -> None:
    """Render the current game, including active and finished states."""
    remaining = 0
    if not state["finished"] and state["health"] > 0:
        remaining = refresh_timer(state, settings, generator)
    render_status(state, settings)
    if state["finished"]:
        st.success(f"¡Victoria! Reuniste {state['gold']} monedas.")
    elif state["health"] <= 0:
        st.error("Has quedado sin vida. El castillo te derrotó.")
    elif remaining > 0:
        render_round(state, settings, generator, remaining)
    render_controls(settings, generator)


def main() -> None:
    """Load configuration and route the current Streamlit session."""
    st.set_page_config(page_title="Castillo Matemático", page_icon="🏰")
    settings = load_json("config/settings.json")
    generator = ExerciseGenerator(load_json("config/exercises.json"))
    if "game" not in st.session_state:
        st.session_state.game = None
    st.title("🏰 Castillo Matemático")
    st.caption("Resuelve las operaciones para avanzar por las habitaciones.")
    state = st.session_state.game
    if state is None:
        render_start(settings, generator)
        st.stop()
    render_game(state, settings, generator)


if __name__ == "__main__":
    main()
