const GAME_DURATION = 10_000;
const MOLE_INTERVAL = 650;

const holes = [...document.querySelectorAll(".hole")];
const startButton = document.querySelector("#start-button");
const scoreElement = document.querySelector("#score");
const timeElement = document.querySelector("#time");
const statusElement = document.querySelector("#game-status");
const resultDialog = document.querySelector("#result-dialog");
const finalScore = document.querySelector("#final-score");

let score = 0;
let activeHole = -1;
let gameEndsAt = 0;
let moleTimer;
let clockFrame;
let isPlaying = false;

function randomHole() {
  if (holes.length <= 1) return 0;

  let nextHole;
  do {
    nextHole = Math.floor(Math.random() * holes.length);
  } while (nextHole === activeHole);

  return nextHole;
}

function hideMole() {
  holes.forEach((hole) => hole.classList.remove("has-mole", "was-hit"));
  activeHole = -1;
}

function showMole() {
  hideMole();
  activeHole = randomHole();
  holes[activeHole].classList.add("has-mole");
  holes[activeHole].setAttribute("aria-label", `Agujero ${activeHole + 1}: topo visible`);
}

function updateClock(now) {
  const remaining = Math.max(0, gameEndsAt - now);
  timeElement.textContent = (remaining / 1000).toFixed(1);

  if (remaining > 0) {
    clockFrame = requestAnimationFrame(updateClock);
  }
}

function finishGame() {
  if (!isPlaying) return;

  isPlaying = false;
  clearInterval(moleTimer);
  cancelAnimationFrame(clockFrame);
  hideMole();
  timeElement.textContent = "0.0";
  startButton.disabled = false;
  startButton.textContent = "Jugar otra vez";

  const scoreText = `${score} ${score === 1 ? "punto" : "puntos"}`;
  finalScore.textContent = scoreText;
  statusElement.textContent = `Partida terminada. Has conseguido ${scoreText}.`;
  resultDialog.showModal();
}

function startGame() {
  clearInterval(moleTimer);
  cancelAnimationFrame(clockFrame);

  score = 0;
  isPlaying = true;
  gameEndsAt = performance.now() + GAME_DURATION;
  scoreElement.textContent = "0";
  timeElement.textContent = "10.0";
  startButton.disabled = true;
  startButton.textContent = "Jugando…";
  statusElement.textContent = "La partida ha comenzado.";

  showMole();
  moleTimer = setInterval(showMole, MOLE_INTERVAL);
  clockFrame = requestAnimationFrame(updateClock);
  setTimeout(finishGame, GAME_DURATION);
}

holes.forEach((hole, index) => {
  hole.addEventListener("click", () => {
    if (!isPlaying || index !== activeHole || hole.classList.contains("was-hit")) {
      return;
    }

    score += 1;
    scoreElement.textContent = String(score);
    hole.classList.add("was-hit");
    hole.setAttribute("aria-label", `Agujero ${index + 1}: topo golpeado`);

    setTimeout(() => {
      if (index === activeHole && isPlaying) showMole();
    }, 110);
  });
});

startButton.addEventListener("click", startGame);

resultDialog.addEventListener("click", (event) => {
  if (event.target === resultDialog) resultDialog.close();
});
