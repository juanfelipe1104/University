# Fundamentos de React

## React y las interfaces por componentes

React es una biblioteca para construir interfaces web y nativas mediante **componentes**. Un componente encapsula una parte de la interfaz, su comportamiento y su representación.

React se ocupa de renderizar la interfaz y mantenerla sincronizada con los datos. No prescribe por sí solo el enrutamiento, la obtención de datos o la estructura completa de una aplicación; esas necesidades se cubren con otras bibliotecas o frameworks como Next.js.

```jsx
function MyButton() {
  return <button type="button">Púlsame</button>;
}

export default function App() {
  return (
    <main>
      <h1>Mi aplicación</h1>
      <MyButton />
    </main>
  );
}
```

Los componentes propios empiezan por mayúscula. Las etiquetas HTML se escriben en minúscula, lo que permite a React distinguir entre ambos.

## Proyecto React con Vite

El navegador no interpreta JSX directamente. Vite proporciona el servidor de desarrollo y transforma, agrupa y optimiza los archivos para producción.

```console
npm create vite@latest mi-proyecto -- --template react
cd mi-proyecto
npm install
npm run dev
```

Comandos habituales:

| Comando | Función |
|---|---|
| `npm run dev` | Inicia el servidor de desarrollo |
| `npm run build` | Genera la versión de producción en `dist/` |
| `npm run preview` | Sirve localmente la compilación de producción |
| `npm run lint` | Ejecuta el analizador configurado por el proyecto |

### Punto de entrada

`index.html` contiene el nodo raíz:

```html
<div id="root"></div>
```

`src/main.jsx` conecta ese nodo con el componente principal:

```jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

`StrictMode` activa comprobaciones adicionales durante el desarrollo. Puede ejecutar ciclos adicionales de renderizado y efectos para descubrir componentes impuros o limpiezas ausentes; esto no sucede en la compilación de producción.

## Composición de componentes

Los componentes se combinan anidándolos. JSX debe devolver un único elemento raíz; si no se necesita una etiqueta adicional se usa un fragmento.

```jsx
function ImagenAleatoria() {
  return <img src="https://picsum.photos/400/300" alt="Paisaje aleatorio" />;
}

function Galeria() {
  return (
    <>
      <ImagenAleatoria />
      <ImagenAleatoria />
      <ImagenAleatoria />
    </>
  );
}
```

Cada componente debe tener una responsabilidad clara. Las piezas reutilizables suelen guardarse en `src/components/`, junto con sus estilos cuando resulte conveniente.

## JSX

JSX es una extensión de JavaScript que describe la interfaz con una sintaxis similar a HTML. El proceso de construcción lo transforma en llamadas de JavaScript.

Reglas principales:

- devolver un único elemento raíz o un fragmento;
- cerrar todas las etiquetas, incluidas `<img />` y `<br />`;
- usar `className` en vez de `class` y `htmlFor` en vez de `for`;
- escribir propiedades y eventos en *camelCase*, como `readOnly` u `onClick`;
- incluir expresiones JavaScript mediante llaves.

```jsx
function Avatar() {
  const person = {
    name: "Lin Lanying",
    image: "/lin-lanying.jpg",
  };

  return (
    <figure>
      <img src={person.image} alt={person.name} />
      <figcaption>{person.name}</figcaption>
    </figure>
  );
}
```

Dentro de las llaves se admiten **expresiones**, no sentencias como `if` o `for`. Un doble par de llaves representa un objeto JavaScript dentro de una expresión:

```jsx
<div style={{ backgroundColor: "navy", color: "white" }}>Contenido</div>
```

## Props

Las props son datos que un componente padre entrega a un hijo. Pueden contener cadenas, números, objetos, arrays, elementos o funciones.

```jsx
function Avatar({ person, size = 80 }) {
  return (
    <img
      src={person.image}
      alt={person.name}
      width={size}
      height={size}
    />
  );
}

<Avatar
  person={{ name: "Ana", image: "/ana.jpg" }}
  size={120}
/>;
```

Las props son de solo lectura. Un hijo no debe modificarlas: cuando necesita comunicar una acción, invoca una función recibida como prop.

### children

El contenido escrito entre las etiquetas de un componente llega mediante la prop `children`:

```jsx
function Panel({ title, children }) {
  return (
    <section>
      <h2>{title}</h2>
      {children}
    </section>
  );
}

<Panel title="Perfil">
  <Avatar person={person} />
</Panel>;
```

## Renderizado de listas

`map` transforma datos en elementos React:

```jsx
function UserList({ users }) {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

Cada elemento necesita una `key` estable y única entre sus hermanos. React la utiliza para asociar datos y componentes entre renderizados. No se recomienda usar el índice si los elementos pueden insertarse, eliminarse o reordenarse. `key` es información interna de React y no llega como prop; si el hijo necesita el identificador debe pasarse también como `id`.

## Renderizado condicional

Puede calcularse el JSX antes del `return`:

```jsx
function Greeting({ user }) {
  if (!user) {
    return <LoginButton />;
  }

  return <p>Hola, {user.name}</p>;
}
```

También se usan el ternario y el cortocircuito con `&&`:

```jsx
{isLoggedIn ? <Profile /> : <LoginButton />}
{messages.length > 0 && <MessageList messages={messages} />}
```

Conviene evitar `count && <Component />` si `count` puede ser cero, porque React mostraría el `0`. La condición explícita `count > 0` evita ese resultado.

## Componentes puros

Un componente debe ser puro durante el renderizado:

- las mismas props, estado y contexto producen el mismo JSX;
- no modifica variables u objetos creados fuera de él;
- no realiza efectos secundarios durante el renderizado.

Las interacciones se ejecutan en manejadores de eventos y la sincronización con sistemas externos en efectos.

## Eventos

Los manejadores se pasan como funciones:

```jsx
function AlertButton({ label, message }) {
  function handleClick() {
    window.alert(message);
  }

  return <button onClick={handleClick}>{label}</button>;
}
```

No debe invocarse la función al renderizar:

```jsx
// Correcto
<button onClick={handleClick}>Guardar</button>
<button onClick={() => deleteItem(id)}>Eliminar</button>

// Incorrecto: se ejecuta durante el renderizado
<button onClick={handleClick()}>Guardar</button>
```

Los eventos de React reciben un objeto de evento. En formularios es habitual llamar a `event.preventDefault()` para impedir la recarga del navegador.

## Estado con useState

El estado es la memoria privada de una instancia de componente. `useState` devuelve el valor actual y una función para solicitar su actualización.

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Pulsaciones: {count}
    </button>
  );
}
```

Los hooks se llaman siempre en el nivel superior del componente o de un hook propio, nunca dentro de condiciones, bucles o funciones anidadas.

### El estado es una instantánea

Cada renderizado recibe una instantánea fija del estado. Llamar a `setCount` solicita otro renderizado, pero no cambia la variable `count` dentro del manejador que ya se está ejecutando.

```jsx
// Ambas llamadas calculan 0 + 1 en el mismo renderizado
setCount(count + 1);
setCount(count + 1);
```

Cuando el siguiente valor depende del anterior se usa una actualización funcional:

```jsx
setCount((current) => current + 1);
setCount((current) => current + 1);
// El resultado aumenta en 2
```

React agrupa normalmente las actualizaciones realizadas durante un mismo evento y renderiza después de que termine el manejador.

## Objetos y arrays en el estado

El estado se trata como inmutable. Modificar directamente un objeto no informa a React y conserva una referencia compartida.

```jsx
const [person, setPerson] = useState({ name: "Ana", age: 20 });

setPerson((current) => ({
  ...current,
  age: current.age + 1,
}));
```

Para arrays se usan operaciones que devuelven una copia:

```jsx
setTasks((current) => [newTask, ...current]);
setTasks((current) => current.filter((task) => task.id !== id));
setTasks((current) =>
  current.map((task) =>
    task.id === id ? { ...task, completed: !task.completed } : task,
  ),
);
```

`push`, `pop`, `splice` y la asignación directa mutan el array existente y deben evitarse sobre el estado.

## Diseño del estado

- Agrupar valores que siempre se actualizan juntos.
- Evitar estado redundante: si puede calcularse con props o con otro estado durante el renderizado, no hace falta almacenarlo.
- Evitar contradicciones entre varias variables de estado.
- Mantener la estructura tan plana como sea razonable.
- No duplicar props en el estado salvo que se quiera ignorar deliberadamente sus futuras actualizaciones.

```jsx
const completedCount = tasks.filter((task) => task.completed).length;
```

`completedCount` se deriva de `tasks` y no necesita un `useState` independiente.

## Elevar el estado

Cuando varios componentes deben compartir o coordinar datos, el estado se mueve al antecesor común más cercano. El padre pasa los valores y manejadores mediante props:

```jsx
function Accordion() {
  const [activeId, setActiveId] = useState(null);

  return panels.map((panel) => (
    <Panel
      key={panel.id}
      isOpen={panel.id === activeId}
      onOpen={() => setActiveId(panel.id)}
    />
  ));
}
```

Esto mantiene una única fuente de verdad.

## useRef

`useRef` conserva un valor entre renderizados sin provocar uno nuevo al cambiar `current`.

```jsx
import { useRef } from "react";

function Search() {
  const inputRef = useRef(null);

  return (
    <>
      <input ref={inputRef} />
      <button onClick={() => inputRef.current?.focus()}>
        Enfocar
      </button>
    </>
  );
}
```

Se usa para acceder al DOM, guardar identificadores de temporizadores o conservar datos que no participan en el renderizado. Si un valor debe aparecer en la interfaz, debe ser estado.

## useEffect

`useEffect` sincroniza un componente con sistemas externos: red, suscripciones, temporizadores o APIs imperativas.

```jsx
import { useEffect } from "react";

function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = connect(roomId);
    connection.open();

    return () => connection.close();
  }, [roomId]);

  return <h1>Sala {roomId}</h1>;
}
```

La función de limpieza se ejecuta antes de volver a aplicar el efecto con dependencias distintas y al desmontar el componente.

| Dependencias | Ejecución |
|---|---|
| Sin segundo argumento | Después de cada renderizado |
| `[]` | Al montar; limpieza al desmontar |
| `[a, b]` | Al montar y cuando cambia `a` o `b` |

No se necesita un efecto para calcular datos derivados, responder a un clic o transformar props para renderizar. Esas operaciones pertenecen al renderizado o al manejador del evento.

### Peticiones y limpieza

```jsx
useEffect(() => {
  const controller = new AbortController();

  async function loadData() {
    const response = await fetch(url, { signal: controller.signal });
    const data = await response.json();
    setData(data);
  }

  loadData();
  return () => controller.abort();
}, [url]);
```

La limpieza impide mantener una petición que ya no corresponde al componente actual.
