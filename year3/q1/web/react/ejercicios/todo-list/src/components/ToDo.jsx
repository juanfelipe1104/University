function ToDo({ id, text, completed, completeToDo, deleteToDo }) {
  return (
    <li className={`todo-item${completed ? " completed" : ""}`}>
      <label className="todo-content">
        <input
          type="checkbox"
          checked={completed}
          aria-label={`${completed ? "Marcar como pendiente" : "Completar"}: ${text}`}
          onChange={() => completeToDo(id)}
        />
        <span className="checkmark" aria-hidden="true"></span>
        <span className="todo-text">{text}</span>
      </label>

      <button
        className="delete-button"
        type="button"
        aria-label={`Eliminar: ${text}`}
        onClick={() => deleteToDo(id)}
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </li>
  );
}

export default ToDo;
