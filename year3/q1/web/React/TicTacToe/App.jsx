
import './App.css'
import {useState} from 'react'

import Board from './components/Board.jsx'
import Winner from './components/Winner.jsx';

const winnerChoices = [[0,1,2], [3,4,5], [6,7,8],[0,3,6], [1,4,7], [2,5,8], [0, 4, 8], [2,4,6]];
const checkPlayer = (board, choices, player) => {
  return choices.some((item) => (board[item[0]] === board[item[1]] 
    && board[item[1]] === board[item[2]] && board[item[0]] === player));
}

const checkWinner = (board, winnerChoices) => {
  let winner = null;
  if (checkPlayer(board, winnerChoices, 'X'))
    winner = 'X';
    else if (checkPlayer(board, winnerChoices, 'O'))
    winner = 'O';
  else if (board.reduce((acc, item) => (item != '') ? acc : acc -1, 9) == 9)
    winner = 'Empate';
  return winner;
}

export default function App() {
  const [moves, setMoves] = useState([]);
  const board = Array(9).fill('');
  const nextPlayer = (moves.length % 2) ? 'X' : 'O';

  moves.forEach(item => board[item[0]] = item[1]);
  const champion = checkWinner(board, winnerChoices);

  const handleClick = (index) => {   
    setMoves((prev) => [...prev, [index, nextPlayer]]);
  }

  const handleNewGame = () =>{
    setMoves([]);
  }
  
  return (<>
  {champion && ( <Winner player={champion} onOk={handleNewGame}></Winner>)}
  <h1>TicTacToe</h1>
  <h1>Next player: {nextPlayer}</h1>
    <Board board={board} handleClick={handleClick}/>
    </>
  )
}

 