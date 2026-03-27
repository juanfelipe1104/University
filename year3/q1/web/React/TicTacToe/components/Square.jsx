function Square({index, value, handleClick}) {
    const disabled = value !== '';
    return (
        <button id={`id${index}`} className="square" disabled={disabled} onClick={() => handleClick(index)}>
            {value}
        </button>
    )
}

export default Square