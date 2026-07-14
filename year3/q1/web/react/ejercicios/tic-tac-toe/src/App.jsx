import { useState } from "react";
import "./App.css";
import Board from "./components/Board.jsx";
import Winner from "./components/Winner.jsx";
import { calculateWinner } from "./utils/calculateWinner.js";

const EMPTY_BOARD = Array(9).fill(null);

function buildBoard(history) {
  return history.reduce((board, [index, player]) => {
    board[index] = player;
    return board;
  }, [...EMPTY_BOARD]);
}

function App() {
  const [history, setHistory] = useState([]);

  const board = buildBoard(history);
  const winner = calculateWinner(board);
  const isDraw = !winner && history.length === board.length;
  const currentPlayer = history.length % 2 === 0 ? "X" : "O";
  const gameOver = Boolean(winner) || isDraw;

  function playSquare(index) {
    if (gameOver || board[index]) return;
    setHistory((currentHistory) => [...currentHistory, [index, currentPlayer]]);
  }

  function resetGame() {
    setHistory([]);
  }

  return (
    <main className="game-page">
      <section className="game-card" aria-labelledby="game-title">
        <header className="game-heading">
          <p className="eyebrow">React · useState</p>
          <h1 id="game-title">Tic-tac-toe</h1>
          <p>Consigue tres fichas en línea antes que tu rival.</p>
        </header>

        <div className="game-layout">
          <div>
            <p className="turn" aria-live="polite">
              {gameOver ? "Partida terminada" : "Turno de"}
              {!gameOver && (
                <strong className={`player player-${currentPlayer}`}>
                  {currentPlayer}
                </strong>
              )}
            </p>

            <Board
              squares={board}
              winnerLine={winner?.line ?? []}
              disabled={gameOver}
              onPlay={playSquare}
            />
          </div>

          <aside className="game-info">
            <Winner winner={winner?.player} isDraw={isDraw} />

            <div className="move-history">
              <h2>Jugadas</h2>
              {history.length === 0 ? (
                <p className="empty-history">La partida todavía no ha comenzado.</p>
              ) : (
                <ol>
                  {history.map(([index, player], moveIndex) => (
                    <li key={`${index}-${moveIndex}`}>
                      <span className={`history-player player-${player}`}>{player}</span>
                      Casilla {index + 1}
                    </li>
                  ))}
                </ol>
              )}
            </div>

            <button className="reset-button" type="button" onClick={resetGame}>
              Nueva partida
            </button>
          </aside>
        </div>
      </section>
    </main>
  );
}

export default App;
