export default function Winner ({player, onOk}) {
  const text = (player!== 'Empate')?`El ganador es ${player}`: 'Empate';
  return (<div id ="winner">
        <h1>{text}</h1>
        <button onClick={onOk}> Start</button></div>)
}