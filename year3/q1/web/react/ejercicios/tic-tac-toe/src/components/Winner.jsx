function Winner({ winner, isDraw }) {
  if (!winner && !isDraw) {
    return (
      <div className="result result-pending">
        <span>Objetivo</span>
        <strong>Tres en línea</strong>
      </div>
    );
  }

  return (
    <div className="result" role="status">
      <span>{isDraw ? "Resultado" : "Ganador"}</span>
      <strong>{isDraw ? "Empate" : `Jugador ${winner}`}</strong>
    </div>
  );
}

export default Winner;
