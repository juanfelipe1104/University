const STORAGE_KEY = "javascript-todo.tasks";

const form = document.querySelector("#task-form");
const titleInput = document.querySelector("#task-title");
const descriptionInput = document.querySelector("#task-description");
const taskList = document.querySelector("#task-list");
const taskTemplate = document.querySelector("#task-template");
const emptyState = document.querySelector("#empty-state");
const taskCounter = document.querySelector("#task-counter");

let tasks = loadTasks();

function loadTasks() {
  try {
    const storedTasks = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]");
    return Array.isArray(storedTasks) ? storedTasks : [];
  } catch (error) {
    console.warn("No se pudieron recuperar las tareas guardadas.", error);
    return [];
  }
}

function saveTasks() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

function createId() {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random()}`;
}

function renderTasks() {
  taskList.replaceChildren();

  for (const task of tasks) {
    const item = taskTemplate.content.firstElementChild.cloneNode(true);
    const toggle = item.querySelector(".task-toggle");
    const title = item.querySelector(".task-title");
    const description = item.querySelector(".task-description");
    const deleteButton = item.querySelector(".delete-button");

    item.dataset.id = task.id;
    item.classList.toggle("is-completed", task.completed);
    toggle.checked = task.completed;
    toggle.setAttribute(
      "aria-label",
      `${task.completed ? "Marcar como pendiente" : "Completar"}: ${task.title}`,
    );
    title.textContent = task.title;
    description.textContent = task.description;
    description.hidden = task.description.length === 0;
    deleteButton.setAttribute("aria-label", `Eliminar: ${task.title}`);

    taskList.append(item);
  }

  const pendingTasks = tasks.filter((task) => !task.completed).length;
  taskCounter.textContent = `${pendingTasks} ${pendingTasks === 1 ? "pendiente" : "pendientes"}`;
  emptyState.hidden = tasks.length > 0;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const title = titleInput.value.trim();
  const description = descriptionInput.value.trim();

  if (!title) {
    titleInput.setCustomValidity("Escribe un título para la tarea.");
    titleInput.reportValidity();
    return;
  }

  tasks.unshift({
    id: createId(),
    title,
    description,
    completed: false,
  });

  saveTasks();
  renderTasks();
  form.reset();
  titleInput.focus();
});

titleInput.addEventListener("input", () => titleInput.setCustomValidity(""));

taskList.addEventListener("change", (event) => {
  if (!event.target.matches(".task-toggle")) return;

  const item = event.target.closest(".task-item");
  const task = tasks.find((candidate) => candidate.id === item.dataset.id);

  if (!task) return;

  task.completed = event.target.checked;
  saveTasks();
  renderTasks();
});

taskList.addEventListener("click", (event) => {
  const deleteButton = event.target.closest(".delete-button");
  if (!deleteButton) return;

  const item = deleteButton.closest(".task-item");
  tasks = tasks.filter((task) => task.id !== item.dataset.id);
  saveTasks();
  renderTasks();
});

renderTasks();
