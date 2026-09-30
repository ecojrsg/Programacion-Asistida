import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from game import ExerciseGenerator, load_json, new_game, submit_answer, timeout
from fog import SPIN_SECONDS, check_room_event, resolve_roulette, start_roulette

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

remaining = None
fog_event = None
fog_phase = 0
fog_progress = 0
if not state["finished"] and state["health"] > 0:
    room = state["room"]
    fog_event = check_room_event(state, room)
    if fog_event["status"] == "spinning":
        now = time.time()
        result = resolve_roulette(state, room, settings, generator, now=now)
        if result is not None:
            st.rerun()
        elapsed = now - fog_event["started_at"]
        fog_phase = int(elapsed * 16) % 2
        fog_progress = min(100, int(elapsed / SPIN_SECONDS * 100))
        st_autorefresh(interval=100, key=f"fog-roulette-{room}")
    elif fog_event["status"] != "offered":
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
notice = state.get("fog_notice")
if notice and notice["room"] == state["room"] - 1:
    st.success(f"🌫️ La ruleta eligió **Pase libre**: habitación {notice['room']} despejada, sin oro de combate.")

if state["finished"]:
    st.success(f"¡Victoria! Reuniste {state['gold']} monedas.")
elif state["health"] <= 0:
    st.error("Has quedado sin vida. El castillo te derrotó.")
elif fog_event and fog_event["status"] == "offered":
    st.markdown(
        """
        <div style="padding:1.25rem;border-radius:1rem;border:1px solid #8b5cf6;
        background:linear-gradient(135deg,#20133f,#10253b);box-shadow:0 0 28px #8b5cf644;">
          <div style="font-size:.8rem;letter-spacing:.18em;color:#c4b5fd;font-weight:700">EVENTO DE NIEBLA</div>
          <div style="font-size:1.4rem;font-weight:800;margin:.35rem 0">La niebla oculta el destino de esta sala.</div>
          <div style="color:#d1d5db">Una ruleta decidirá entre <b>🌟 Pase libre</b> y <b>⚔️ Enemigo</b>.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🎲 Iniciar ruleta", type="primary", key=f"start-fog-{state['room']}"):
        start_roulette(state, state["room"])
        st.rerun()
elif fog_event and fog_event["status"] == "spinning":
    active_pass = "active" if fog_phase == 0 else ""
    active_enemy = "active" if fog_phase == 1 else ""
    st.markdown(
        f"""
        <style>
          @keyframes fog-glow {{ 0%,100% {{ filter:drop-shadow(0 0 8px #a78bfa); }} 50% {{ filter:drop-shadow(0 0 24px #38bdf8); }} }}
          @keyframes fog-ring {{ from {{ transform:rotate(0deg); }} to {{ transform:rotate(360deg); }} }}
          .fog-roulette {{ position:relative; overflow:hidden; padding:1.4rem; border-radius:1.2rem;
            border:1px solid #7c3aed; background:radial-gradient(circle at 50% 45%,#31205c,#101827 72%);
            color:white; text-align:center; box-shadow:0 0 35px #7c3aed55; }}
          .fog-ring {{ position:absolute; inset:-45%; border:2px dashed #a78bfa55; border-radius:50%; animation:fog-ring 4s linear infinite; pointer-events:none; }}
          .fog-title {{ position:relative; color:#c4b5fd; font-size:.82rem; letter-spacing:.2em; font-weight:800; }}
          .fog-options {{ position:relative; display:flex; align-items:center; justify-content:center; gap:.75rem; margin:1.25rem auto; max-width:38rem; }}
          .fog-option {{ flex:1; padding:1.1rem .6rem; border:1px solid #64748b; border-radius:1rem;
            background:#111827cc; color:#cbd5e1; font-size:1.15rem; font-weight:800; opacity:.55; transform:scale(.94); }}
          .fog-option.active {{ opacity:1; transform:scale(1.04); animation:fog-glow .65s ease-in-out infinite; border-color:#c4b5fd; background:#33245dcc; }}
          .fog-center {{ color:#e9d5ff; font-size:2rem; animation:fog-glow .8s ease-in-out infinite; }}
          .fog-track {{ position:relative; height:.45rem; overflow:hidden; border-radius:99px; background:#334155; }}
          .fog-track span {{ display:block; width:100%; height:100%; border-radius:99px; background:linear-gradient(90deg,#a855f7,#38bdf8);
            transform-origin:left; transition:transform .1s linear; }}
          .fog-caption {{ position:relative; margin-top:.7rem; color:#cbd5e1; }}
          @media (prefers-reduced-motion: reduce) {{
            .fog-ring, .fog-option.active, .fog-center {{ animation:none; }}
            .fog-option, .fog-option.active {{ opacity:1; transform:none; border-color:#64748b; background:#111827cc; }}
            .fog-track span {{ transition:none; }}
          }}
        </style>
        <div class="fog-roulette" role="status" aria-label="Ruleta de niebla en curso">
          <div class="fog-ring"></div>
          <div class="fog-title">🌫️ RULETA DE LA NIEBLA 🌫️</div>
          <div class="fog-options">
            <div class="fog-option {active_pass}">🌟 Pase libre</div>
            <div class="fog-center">◈</div>
            <div class="fog-option {active_enemy}">⚔️ Enemigo</div>
          </div>
          <div class="fog-track" role="progressbar" aria-label="Progreso de la ruleta" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{fog_progress}">
            <span style="transform:scaleX({fog_progress / 100:.3f})"></span>
          </div>
          <div class="fog-caption">El destino de la habitación se está revelando…</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif fog_event and fog_event["status"] == "enemy":
    st.warning(f"🌫️ La ruleta eligió **Enemigo** en la habitación {state['room']}. ¡Resuelve la operación para avanzar!")

if remaining is not None and remaining > 0:
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
