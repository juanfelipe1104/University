import { useState } from "react";
import FormToDo from "./FormToDo.jsx";
import ToDo from "./ToDo.jsx";

function ListToDo() {
  const [tasks, setTasks] = useState([]);

  const completedTasks = tasks.filter((task) => task.completed).length;
  const pendingTasks = tasks.length - completedTasks;

  function addTask(task) {
    setTasks((currentTasks) => [task, ...currentTasks]);
  }

  function deleteTask(id) {
    setTasks((currentTasks) => currentTasks.filter((task) => task.id !== id));
  }

  function completeTask(id) {
    setTasks((currentTasks) =>
      currentTasks.map((task) =>
        task.id === id ? { ...task, completed: !task.completed } : task,
      ),
    );
  }

  return (
    <section className="todo-card" aria-labelledby="task-list-title">
      <FormToDo onSubmit={addTask} />

      <div className="list-heading">
        <div>
          <p className="eyebrow">Tu progreso</p>
          <h2 id="task-list-title">Lista de tareas</h2>
        </div>
        <p className="counter" aria-live="polite">
          <strong>{pendingTasks}</strong> {pendingTasks === 1 ? "pendiente" : "pendientes"}
        </p>
      </div>

      {tasks.length === 0 ? (
        <p className="empty-list">No hay tareas. Escribe una para comenzar.</p>
      ) : (
        <ul className="todo-list">
          {tasks.map((task) => (
            <ToDo
              key={task.id}
              id={task.id}
              text={task.text}
              completed={task.completed}
              completeToDo={completeTask}
              deleteToDo={deleteTask}
            />
          ))}
        </ul>
      )}

      {tasks.length > 0 && (
        <p className="completion-summary">
          {completedTasks} de {tasks.length} completadas
        </p>
      )}
    </section>
  );
}

export default ListToDo;
