import Square from "./Square.jsx";

function Board({ squares, winnerLine, disabled, onPlay }) {
  return (
    <div className="board" role="grid" aria-label="Tablero de tres por tres">
      {squares.map((value, index) => (
        <Square
          key={index}
          value={value}
          position={index}
          isWinner={winnerLine.includes(index)}
          disabled={disabled || Boolean(value)}
          onPlay={onPlay}
        />
      ))}
    </div>
  );
}

export default Board;
