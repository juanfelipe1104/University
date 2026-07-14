import { useState } from "react";

function FormToDo({ onSubmit }) {
  const [input, setInput] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    const text = input.trim();
    if (!text) return;

    onSubmit({
      id: globalThis.crypto.randomUUID(),
      text,
      completed: false,
    });
    setInput("");
  }

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <label htmlFor="new-task">Nueva tarea</label>
      <div className="form-row">
        <input
          id="new-task"
          type="text"
          value={input}
          maxLength={120}
          placeholder="Escribe una tarea"
          autoComplete="off"
          onChange={(event) => setInput(event.target.value)}
        />
        <button type="submit" disabled={!input.trim()}>
          Añadir
        </button>
      </div>
    </form>
  );
}

export default FormToDo;
