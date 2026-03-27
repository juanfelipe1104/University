import Square from './Square'

function Board({board, handleClick}) {
    return (
        <div id="board">
            {board.map((value, index) => (
                <Square key={index} index={index} value={value} handleClick={handleClick}/>
            ))}
        </div>
    )
}

export default Board