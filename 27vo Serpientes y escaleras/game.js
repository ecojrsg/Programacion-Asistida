"use strict";

const Game = {
  jumps: Object.freeze({
    3: 22, 8: 30, 20: 41, 28: 55, 58: 77, 75: 94,
    27: 5, 43: 18, 54: 31, 66: 45, 89: 53, 97: 72,
  }),

  create() {
    return { positions: [0, 0], player: 0, phase: "ready", turns: 0 };
  },

  move(state, die) {
    if (state.phase !== "playing") {
      throw new Error("A turn requires an active game.");
    }
    if (!Number.isInteger(die) || die < 1 || die > 6) {
      throw new RangeError("The die must be an integer between 1 and 6.");
    }
    const from = state.positions[state.player];
    const overshoot = from + die > 100;
    const landing = overshoot ? from : from + die;
    const to = overshoot ? from : (Game.jumps[landing] ?? landing);
    const positions = [...state.positions];
    positions[state.player] = to;
    return {
      state: {
        positions,
        player: to === 100 ? state.player : 1 - state.player,
        phase: to === 100 ? "won" : "playing",
        turns: state.turns + 1,
      },
      move: {
        player: state.player, die, from, landing, to, overshoot,
        kind: to > landing ? "ladder" : to < landing ? "snake" : "normal",
      },
    };
  },
};
