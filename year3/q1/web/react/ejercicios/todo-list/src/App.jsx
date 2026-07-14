import "./App.css";
import ListToDo from "./components/ListToDo.jsx";
import Logo from "./components/Logo.jsx";

function App() {
  return (
    <main className="page-shell">
      <header className="page-header">
        <Logo />
        <div>
          <p className="eyebrow">Organizador personal</p>
          <h1>Mis tareas</h1>
          <p className="intro">Añade una tarea, complétala y sigue avanzando.</p>
        </div>
      </header>

      <ListToDo />
    </main>
  );
}

export default App;
