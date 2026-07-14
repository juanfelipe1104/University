function Square({ value, position, isWinner, disabled, onPlay }) {
  const classNames = [
    "square",
    value ? `square-${value}` : "",
    isWinner ? "is-winner" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button
      className={classNames}
      type="button"
      role="gridcell"
      aria-label={`Casilla ${position + 1}${value ? `, marcada con ${value}` : ", vacía"}`}
      disabled={disabled}
      onClick={() => onPlay(position)}
    >
      {value}
    </button>
  );
}

export default Square;
