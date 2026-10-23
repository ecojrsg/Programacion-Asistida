"use strict";

const board = document.getElementById("board");
const playButton = document.getElementById("play-button");
const resetButton = document.getElementById("reset-button");
const message = document.getElementById("message");
const dieValue = document.getElementById("die-value");
const pieces = [0, 1].map((player) => document.getElementById(`piece-${player}`));
// shortcut: progress lasts for this tab; add storage if resuming games is needed.
let state = Game.create();
let busy = false;

function cellPoint(number, player = 0) {
  if (number === 0) return { x: 15 + player * 8, y: 104.5 };
  const row = Math.floor((number - 1) / 10);
  const column = (number - 1) % 10;
  return { x: (row % 2 ? 9 - column : column) * 10 + 5, y: 95 - row * 10 };
}

function piecePoint(number, player) {
  const point = cellPoint(number, player);
  return { x: point.x + (number ? (player ? 2 : -2) : 0), y: point.y + (number ? 1.6 : 0) };
}

function buildBoard() {
  for (let number = 1; number <= 100; number += 1) {
    const cell = document.createElement("li");
    const point = cellPoint(number);
    const target = Game.jumps[number];
    const kind = target ? (target > number ? "ladder" : "snake") : "";
    cell.className = `cell ${number % 2 ? "" : "alternate"} ${kind} ${number === 100 ? "finish" : ""}`;
    cell.style.gridColumn = Math.round((point.x + 5) / 10);
    cell.style.gridRow = Math.round((point.y + 5) / 10);
    const label = document.createElement("span");
    label.className = "cell-number";
    label.textContent = number;
    cell.append(label);
    if (target) {
      const hint = document.createElement("small");
      hint.className = "connection-label";
      hint.textContent = `${kind === "ladder" ? "↑" : "↓"}${target}`;
      cell.append(hint);
    }
    const description = target ? `${kind === "ladder" ? "Escalera" : "Serpiente"} a ${target}.` : "";
    cell.setAttribute("aria-label", `Casilla ${number}. ${description}`.trim());
    board.append(cell);
  }
}

function render() {
  for (let player = 0; player < 2; player += 1) {
    const position = state.positions[player];
    const point = piecePoint(position, player);
    pieces[player].style.left = `${point.x}%`;
    pieces[player].style.top = `${point.y}%`;
    document.getElementById(`position-${player}`).textContent = position || "Salida";
    document.getElementById(`player-${player}`).classList.toggle("active", state.phase !== "ready" && state.player === player);
  }
  const label = state.phase === "ready" ? "La mesa está lista"
    : state.phase === "won" ? `¡Ganó Jugador ${state.player + 1}!`
      : `Turno de Jugador ${state.player + 1}`;
  document.getElementById("turn-label").textContent = label;
  document.getElementById("turn-count").textContent = `${state.turns} ${state.turns === 1 ? "tirada" : "tiradas"}`;
  playButton.textContent = state.phase === "ready" ? "Comenzar partida"
    : state.phase === "won" ? "¡Partida terminada!" : busy ? "En movimiento…" : "Lanzar dado";
  playButton.disabled = busy || state.phase === "won";
  resetButton.disabled = busy || state.phase === "ready";
  document.querySelector(".play-panel").setAttribute("aria-busy", String(busy));
}

function describeMove(move) {
  let text = `Jugador ${move.player + 1} sacó ${move.die}. `;
  if (move.overshoot) text += `Necesitas llegar exactamente a 100. Te quedas en ${move.from}.`;
  else if (move.kind === "ladder") text += `¡Escalera! Sube de ${move.landing} a ${move.to}.`;
  else if (move.kind === "snake") text += `¡Serpiente! Baja de ${move.landing} a ${move.to}.`;
  else text += `Avanza a la casilla ${move.to}.`;
  return text + (state.phase === "won" ? ` ¡Ganó Jugador ${move.player + 1}!`
    : ` Turno de Jugador ${state.player + 1}.`);
}

async function playTurn() {
  if (busy || state.phase === "won") return;
  if (state.phase === "ready") {
    state = { ...Game.create(), phase: "playing" };
    message.textContent = "Empieza Jugador 1. Lanza el dado y encuentra tu camino.";
    render();
    return;
  }
  const result = Game.move(state, Math.floor(Math.random() * 6) + 1);
  busy = true;
  dieValue.textContent = "…";
  render();
  let timeout;
  try {
    await Promise.race([
      window.Visuals?.play(result.move, pieces[result.move.player], piecePoint, () => {
        dieValue.textContent = result.move.die;
      }) ?? Promise.resolve(),
      new Promise((resolve) => { timeout = setTimeout(resolve, 3000); }),
    ]);
  } catch (error) {
    window.Visuals?.stop();
    window.Visuals = undefined;
    document.body.classList.remove("has-visuals");
    console.warn("Visual effect skipped; the turn will still finish.", error);
  } finally {
    clearTimeout(timeout);
    window.Visuals?.stop();
    dieValue.textContent = result.move.die;
    state = result.state;
    busy = false;
    render();
    message.textContent = describeMove(result.move);
    if (state.phase === "won") window.Visuals?.celebrate(pieces[state.player]);
  }
}

function resetGame() {
  if (busy) return;
  if (state.phase === "playing" && !window.confirm("¿Comenzar una nueva partida? Se perderá el progreso actual.")) return;
  state = Game.create();
  dieValue.textContent = "—";
  window.Visuals?.reset();
  message.textContent = "Mesa lista otra vez. Una nueva partida, una nueva oportunidad.";
  render();
  playButton.focus();
}

buildBoard();
try {
  window.Visuals?.mount(Game.jumps, cellPoint);
} catch (error) {
  window.Visuals = undefined;
  document.body.classList.remove("has-visuals");
  console.warn("Visual decoration unavailable; using the plain board.", error);
}
render();
playButton.addEventListener("click", playTurn);
resetButton.addEventListener("click", resetGame);
