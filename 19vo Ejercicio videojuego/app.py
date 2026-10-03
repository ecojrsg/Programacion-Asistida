# @Author: Jonathan Serna
# @Date:   2026-09-28 16:41:21
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-02 18:30:59

"""Render the Spanish interface for the math castle game."""

import html
import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from game import ExerciseGenerator, load_json, new_game, submit_answer, timeout
from wordle import (
    MAX_ATTEMPTS,
    MAX_WORD_LENGTH,
    new_game as new_wordle_game,
    submit_guess as submit_wordle_guess,
)


def return_from_wordle() -> None:
    """Resume the combat timer after the Wordle joker ends."""
    state = st.session_state.game
    state["started_at"] += time.time() - st.session_state.wordle_started_at
    st.session_state.wordle_active = False
    st.session_state.wordle_game = None
    st.session_state.pop("wordle_started_at", None)


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


def render_wordle() -> None:
    """Render the Wordle joker and its return actions."""
    wordle = st.session_state.wordle_game
    st.subheader("🃏 Comodín: Wordle")
    st.caption(
        "Adivina la palabra española. Las tildes no cambian las letras; "
        "tienes seis intentos."
    )
    st.markdown(
        """
        <style>
        .wordle-row { display: flex; gap: 5px; margin: 8px 0; }
        .wordle-tile { align-items: center; color: white; display: inline-flex;
          font-size: 1.1rem; font-weight: 700; height: 2.4rem;
          justify-content: center; width: 2.4rem; }
        .wordle-correct { background: #538d4e; }
        .wordle-present { background: #b59f3b; }
        .wordle-absent { background: #787c7e; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    feedback_labels = {
        "correct": "correcta",
        "present": "en otra posición",
        "absent": "ausente",
    }
    for index, attempt in enumerate(wordle["guesses"], start=1):
        tiles = "".join(
            f'<span class="wordle-tile wordle-{color}" aria-label="'
            f'{html.escape(letter.upper())}: {feedback_labels[color]}">'
            f"{html.escape(letter.upper())}</span>"
            for letter, color in zip(attempt["word"], attempt["feedback"])
        )
        st.markdown(
            f'<div class="wordle-row" role="list" aria-label="Intento '
            f'{index}">{tiles}</div>',
            unsafe_allow_html=True,
        )
    st.progress(
        len(wordle["guesses"]) / MAX_ATTEMPTS,
        text=f"Intentos: {len(wordle['guesses'])}/{MAX_ATTEMPTS}",
    )

    if wordle["status"] == "playing":
        with st.form("wordle_guess_form"):
            guess = st.text_input(
                "Tu palabra", max_chars=MAX_WORD_LENGTH, key="wordle_guess_input"
            )
            submitted = st.form_submit_button("Probar palabra", type="primary")
        if submitted:
            try:
                submit_wordle_guess(wordle, guess)
            except ValueError as error:
                st.error(str(error))
            else:
                st.rerun()
        if st.button("Cancelar comodín y volver al castillo", key="cancel_wordle"):
            return_from_wordle()
            st.rerun()
    else:
        if wordle["status"] == "won":
            st.success(f"¡Adivinaste! La palabra era **{wordle['target']}**.")
        else:
            st.error(
                f"Se acabaron los intentos. La palabra era **{wordle['target']}**."
            )
        if st.button("Volver al castillo", key="return_from_wordle"):
            return_from_wordle()
            st.rerun()


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
    wordle_active = st.session_state.get("wordle_active", False)
    remaining = 0
    if not wordle_active and not state["finished"] and state["health"] > 0:
        remaining = refresh_timer(state, settings, generator)
    render_status(state, settings)
    if wordle_active:
        render_wordle()
        st.stop()
    if state["finished"]:
        st.success(f"¡Victoria! Reuniste {state['gold']} monedas.")
    elif state["health"] <= 0:
        st.error("Has quedado sin vida. El castillo te derrotó.")
    elif remaining > 0:
        render_round(state, settings, generator, remaining)
    if not state["finished"] and state["health"] > 0:
        if st.button("🃏 Usar comodín: Wordle"):
            st.session_state.wordle_game = new_wordle_game()
            st.session_state.wordle_started_at = time.time()
            st.session_state.wordle_active = True
            st.rerun()
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
