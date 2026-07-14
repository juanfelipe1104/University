# Tic-tac-toe

Juego de tres en raya desarrollado con React.

## Ejecución

```console
npm install
npm run dev
```

## Estructura

- `App.jsx`: mantiene el historial como pares `[casilla, jugador]` y deriva el tablero.
- `Board.jsx`: renderiza las nueve casillas.
- `Square.jsx`: representa una casilla y bloquea las ocupadas.
- `Winner.jsx`: muestra ganador, empate o estado de la partida.
- `calculateWinner.js`: comprueba las ocho combinaciones ganadoras.
