"use strict";

window.Visuals = (() => {
  const animations = new Set();
  const still = window.matchMedia("(prefers-reduced-motion: reduce)");
  const faces = [[5], [1, 9], [1, 5, 9], [1, 3, 7, 9], [1, 3, 5, 7, 9], [1, 3, 4, 6, 7, 9]];
  const angles = [[0, 0], [0, -90], [-90, 0], [90, 0], [0, 90], [0, 180]];
  let die;
  let generation = 0;

  function pose(value, spin = 0) {
    const [x, y] = angles[value - 1];
    return `translateY(0px) rotateZ(0deg) rotateX(-16deg) rotateY(-18deg) rotateX(${x + spin}deg) rotateY(${y + spin * 1.5}deg)`;
  }

  async function animate(element, frames, duration, easing = "ease-in-out") {
    const animation = element.animate(frames, { duration, fill: "forwards", easing });
    animations.add(animation);
    await animation.finished.catch(() => {});
  }

  function ladder(from, to) {
    const dx = to.x - from.x;
    const dy = to.y - from.y;
    const length = Math.hypot(dx, dy);
    const nx = -dy / length * 12;
    const ny = dx / length * 12;
    const rails = [-1, 1].map((side) => `M${from.x + nx * side},${from.y + ny * side}L${to.x + nx * side},${to.y + ny * side}`).join("");
    const count = Math.max(3, Math.floor(length / 35));
    let rungs = "";
    for (let index = 1; index <= count; index += 1) {
      const x = from.x + dx * index / (count + 1);
      const y = from.y + dy * index / (count + 1);
      rungs += `M${x - nx},${y - ny}L${x + nx},${y + ny}`;
    }
    return `<g><path class="route-shadow" d="${rails}${rungs}" stroke-width="11"/><path class="ladder-rung" d="${rungs}"/><path class="ladder-rail" d="${rails}"/><path class="ladder-light" d="${rails}"/></g>`;
  }

  function snake(from, to) {
    const dx = to.x - from.x;
    const dy = to.y - from.y;
    const length = Math.hypot(dx, dy);
    const bend = Math.min(90, length * .2);
    const nx = -dy / length * bend;
    const ny = dx / length * bend;
    const path = `M${from.x},${from.y}C${from.x + dx * .3 + nx},${from.y + dy * .3 + ny} ${from.x + dx * .7 - nx},${from.y + dy * .7 - ny} ${to.x},${to.y}`;
    const angle = Math.atan2(dy, dx) * 180 / Math.PI;
    return `<g><path class="route-shadow" d="${path}" stroke-width="24"/><path class="snake-body" d="${path}"/><path class="snake-mark" d="${path}"/><g transform="translate(${from.x},${from.y}) rotate(${angle})"><ellipse class="snake-head" rx="25" ry="18"/><circle cx="-10" cy="-8" r="4" fill="#fff6dc"/><circle cx="-10" cy="8" r="4" fill="#fff6dc"/><circle cx="-12" cy="-8" r="2" fill="#293c2e"/><circle cx="-12" cy="8" r="2" fill="#293c2e"/></g></g>`;
  }

  function mount(jumps, pointOf) {
    const point = (number) => {
      const value = pointOf(number);
      return { x: value.x * 10, y: value.y * 10 };
    };
    const entries = Object.entries(jumps);
    document.getElementById("routes").innerHTML =
      entries.filter(([from, to]) => to > Number(from)).map(([from, to]) => ladder(point(Number(from)), point(to))).join("") +
      entries.filter(([from, to]) => to < Number(from)).map(([from, to]) => snake(point(Number(from)), point(to))).join("");
    die = document.createElement("div");
    die.className = "die";
    faces.forEach((dots) => {
      const face = document.createElement("div");
      face.className = "die-face";
      dots.forEach((dot) => {
        const pip = document.createElement("span");
        pip.className = "pip";
        pip.style.gridArea = `${Math.floor((dot - 1) / 3) + 1} / ${(dot - 1) % 3 + 1}`;
        face.append(pip);
      });
      die.append(face);
    });
    document.getElementById("die-art").append(die);
    document.body.classList.add("has-visuals");
  }

  function stop() {
    generation += 1;
    animations.forEach((animation) => animation.cancel());
    animations.clear();
  }

  async function play(move, piece, pointOf, onRolled = () => {}) {
    const current = generation;
    const target = pose(move.die);
    if (!still.matches) {
      await animate(die, [
        { transform: die.style.transform || pose(1) },
        { transform: pose(move.die, 720) },
      ], 1250, "cubic-bezier(0.25, 0.4, 0.55, 1)");
    }
    if (generation !== current) return;
    die.style.transform = target;
    onRolled();
    if (still.matches || move.overshoot) return;
    const origin = pointOf(move.from, move.player);
    const size = document.getElementById("board-plane").clientWidth;
    const duration = (move.landing - move.from) * 90 + (move.kind === "normal" ? 0 : 400);
    const frame = (number, offset) => {
      const point = pointOf(number, move.player);
      return {
        transform: `translate(-50%, -50%) translate(${(point.x - origin.x) * size / 100}px, ${(point.y - origin.y) * size / 100}px)`,
        offset,
      };
    };
    const frames = [frame(move.from, 0)];
    for (let number = move.from + 1; number <= move.landing; number += 1) {
      frames.push(frame(number, (number - move.from) * 90 / duration));
    }
    if (move.kind !== "normal") frames.push(frame(move.to, 1));
    await animate(piece, frames, duration);
  }

  function reset() {
    stop();
    die.style.transform = pose(1);
  }

  function celebrate(piece) {
    if (still.matches) return;
    animate(piece, [
      { transform: "translate(-50%, -50%) scale(1)" },
      { transform: "translate(-50%, -50%) scale(1.35)", offset: .5 },
      { transform: "translate(-50%, -50%) scale(1)" },
    ], 500).then(stop);
  }

  return { mount, play, stop, reset, celebrate };
})();
