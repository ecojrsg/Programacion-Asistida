import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from game import ExerciseGenerator, load_json, new_game, submit_answer, timeout

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

if not state["finished"] and state["health"] > 0:
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

col1, col2 = st.columns(2)
with col1:
    if st.button("Salir de la partida"):
        st.session_state.game = None
        st.rerun()
with col2:
    if st.button("Reiniciar partida"):
        st.session_state.game = new_game(settings, generator)
        st.rerun()
