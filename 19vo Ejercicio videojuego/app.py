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
    st.session_state.game["started_at"] += time.time() - st.session_state.wordle_started_at
    st.session_state.wordle_active = False
    st.session_state.wordle_game = None
    st.session_state.pop("wordle_started_at", None)


st.set_page_config(page_title="Castillo Matemático", page_icon="🏰")
settings = load_json("config/settings.json")
generator = ExerciseGenerator(load_json("config/exercises.json"))

if "game" not in st.session_state:
    st.session_state.game = None
state = st.session_state.game

st.title("🏰 Castillo Matemático")
st.caption("Resuelve las operaciones para avanzar por las habitaciones.")

if state is None:
    st.info("Tu aventura comienza con 100 puntos de vida.")
    if st.button("Comenzar partida", type="primary"):
        st.session_state.game = new_game(settings, generator)
        st.rerun()
    st.stop()

wordle_active = st.session_state.get("wordle_active", False)
remaining = None
if not wordle_active and not state["finished"] and state["health"] > 0:
    remaining = state["exercise"].time_seconds - int(time.time() - state["started_at"])
    if remaining <= 0:
        timeout(state, settings, generator)
        st.warning(f"¡Tiempo agotado! El enemigo infligió {settings['z']} de daño.")
        st.rerun()
    st_autorefresh(interval=1000, key="clock")

st.metric("❤️ Vida", state["health"])
st.metric("🪙 Oro", state["gold"])
st.subheader("🗺️ Mapa")
st.write(" → ".join(f"🚪 {i}" if i >= state["room"] else "✅" for i in range(1, settings["rooms"] + 1)))

if wordle_active:
    wordle = st.session_state.wordle_game
    st.subheader("🃏 Comodín: Wordle")
    st.caption("Adivina la palabra española. Las tildes no cambian las letras; tienes seis intentos.")
    st.markdown(
        """
        <style>
        .wordle-row { display: flex; gap: 5px; margin: 8px 0; }
        .wordle-tile { align-items: center; color: white; display: inline-flex;
          font-size: 1.1rem; font-weight: 700; height: 2.4rem; justify-content: center;
          width: 2.4rem; }
        .wordle-correct { background: #538d4e; }
        .wordle-present { background: #b59f3b; }
        .wordle-absent { background: #787c7e; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    feedback_labels = {"correct": "correcta", "present": "en otra posición", "absent": "ausente"}
    for index, attempt in enumerate(wordle["guesses"], start=1):
        tiles = "".join(
            f'<span class="wordle-tile wordle-{color}" aria-label="{html.escape(letter.upper())}: '
            f'{feedback_labels[color]}">'
            f"{html.escape(letter.upper())}</span>"
            for letter, color in zip(attempt["word"], attempt["feedback"])
        )
        st.markdown(
            f'<div class="wordle-row" role="list" aria-label="Intento {index}">{tiles}</div>',
            unsafe_allow_html=True,
        )
    st.progress(
        len(wordle["guesses"]) / MAX_ATTEMPTS,
        text=f"Intentos: {len(wordle['guesses'])}/{MAX_ATTEMPTS}",
    )

    if wordle["status"] == "playing":
        with st.form("wordle_guess_form"):
            guess = st.text_input("Tu palabra", max_chars=MAX_WORD_LENGTH, key="wordle_guess_input")
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
            st.error(f"Se acabaron los intentos. La palabra era **{wordle['target']}**.")
        if st.button("Volver al castillo", key="return_from_wordle"):
            return_from_wordle()
            st.rerun()
    st.stop()

if state["finished"]:
    st.success(f"¡Victoria! Reuniste {state['gold']} monedas.")
elif state["health"] <= 0:
    st.error("Has quedado sin vida. El castillo te derrotó.")
elif remaining > 0:
    st.subheader(f"Enemigo de la habitación {state['room']}")
    st.write(f"Operación ({state['exercise'].difficulty}): **{state['exercise'].text} = ?**")
    st.progress(remaining / state["exercise"].time_seconds, text=f"Tiempo restante: {remaining}s")
    with st.form("answer"):
        answer = st.number_input("Tu respuesta", step=1, format="%d")
        if st.form_submit_button("Atacar"):
            if submit_answer(state, int(answer), settings, generator):
                st.success("¡Correcto! Enemigo derrotado.")
            else:
                st.error(f"Respuesta incorrecta. Pierdes {settings['x']} de vida.")
            st.rerun()

if not state["finished"] and state["health"] > 0:
    if st.button("🃏 Usar comodín: Wordle"):
        st.session_state.wordle_game = new_wordle_game()
        st.session_state.wordle_started_at = time.time()
        st.session_state.wordle_active = True
        st.rerun()

col1, col2 = st.columns(2)
with col1:
    if st.button("Salir de la partida"):
        st.session_state.game = None
        st.rerun()
with col2:
    if st.button("Reiniciar partida"):
        st.session_state.game = new_game(settings, generator)
        st.rerun()
