# Fundamentos de JavaScript

## Características del lenguaje

JavaScript es el lenguaje de programación nativo de la web. ECMAScript, definido por ECMA-262, especifica el lenguaje; los navegadores y Node.js proporcionan los entornos donde se ejecuta.

Sus características principales son:

- compilación *just in time*;
- tipado dinámico y débil;
- recolección automática de memoria;
- funciones de primera clase;
- soporte de programación procedural, funcional y orientada a objetos;
- ejecución de JavaScript en un solo hilo, coordinada con APIs asíncronas mediante el bucle de eventos.

El lenguaje distingue mayúsculas y minúsculas: `usuario`, `Usuario` y `USUARIO` son identificadores diferentes.

## Integración con HTML

Para cargar un archivo JavaScript como módulo:

```html
<script type="module" src="script.js"></script>
```

Los módulos usan modo estricto, permiten `import` y `export`, y difieren el script hasta que el HTML ha sido procesado. Si no se utilizan módulos, puede emplearse `defer`:

```html
<script defer src="script.js"></script>
```

Separar HTML, CSS y JavaScript facilita el mantenimiento. Los manejadores de eventos deben registrarse desde JavaScript en lugar de usar atributos como `onclick` en el HTML.

## Variables y constantes

| Declaración | Ámbito | Reasignable | Uso |
|---|---|---|---|
| `const` | Bloque | No | Opción predeterminada |
| `let` | Bloque | Sí | Valores que deben cambiar |
| `var` | Función | Sí | Código antiguo; se evita en código moderno |

```js
const nombre = "Ana";
let intentos = 0;
intentos += 1;
```

`const` impide reasignar la variable, pero no hace inmutable el objeto almacenado:

```js
const usuario = { nombre: "Ana" };
usuario.nombre = "Marta"; // Válido
// usuario = {};           // Error
```

Una variable declarada pero no inicializada contiene `undefined`. Asignar sin declarar debe evitarse: en modo estricto produce un error.

## Tipos de datos

Los valores primitivos son:

- `number`: números en coma flotante IEEE 754, incluidos `NaN` e `Infinity`;
- `bigint`: enteros de tamaño arbitrario, como `123n`;
- `string`: cadenas de texto;
- `boolean`: `true` o `false`;
- `undefined`: ausencia de valor asignado;
- `null`: ausencia intencionada de valor;
- `symbol`: identificadores únicos.

El resto son objetos, incluidas funciones y arrays.

```js
typeof 42;          // "number"
typeof "texto";     // "string"
typeof true;        // "boolean"
typeof undefined;   // "undefined"
typeof {};          // "object"
typeof [];          // "object"
typeof null;        // "object" (peculiaridad histórica)
Array.isArray([]);  // true
```

### Conversión y valores falsy

En una condición se consideran falsos `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined` y `NaN`. Los arrays y objetos, incluso vacíos, son verdaderos.

```js
Number("12");       // 12
String(12);         // "12"
Boolean("");        // false
Number.isNaN(NaN);  // true
```

La suma también concatena cadenas:

```js
1 + 1;      // 2
"1" + 1;    // "11"
"1" - 1;    // 0, por conversión numérica
```

Es preferible convertir de forma explícita para evitar resultados inesperados.

## Cadenas y plantillas

Las cadenas se delimitan con comillas simples, dobles o acentos graves. Las plantillas permiten interpolar expresiones y escribir varias líneas.

```js
const nombre = "Ana";
const puntos = 8;
const mensaje = `${nombre} tiene ${puntos * 2} puntos`;
```

Métodos habituales:

```js
const texto = "JavaScript moderno";

texto.length;                // 17
texto.includes("Script");    // true
texto.indexOf("moderno");    // 11
texto.slice(0, 10);          // "JavaScript"
texto.split(" ");            // ["JavaScript", "moderno"]
texto.replace("moderno", "web");
texto.toLowerCase();
texto.toUpperCase();
```

Las cadenas son inmutables: estos métodos devuelven una cadena nueva.

## Operadores

### Igualdad

```js
5 === "5"; // false: mismo valor y tipo
5 !== "5"; // true
5 == "5";  // true: convierte tipos
```

Se usan `===` y `!==` salvo que se necesite deliberadamente la conversión de `==`.

### Operadores lógicos y de valores opcionales

```js
const etiqueta = nombre || "Sin nombre";       // Usa el segundo si el primero es falsy
const cantidad = valor ?? 0;                   // Usa 0 solo si valor es null o undefined
const ciudad = usuario.direccion?.ciudad;      // undefined si falta algún nivel
```

`&&` y `||` cortocircuitan y devuelven uno de sus operandos, no necesariamente un booleano.

## Control de flujo

```js
if (nota >= 9) {
  console.log("Sobresaliente");
} else if (nota >= 5) {
  console.log("Aprobado");
} else {
  console.log("Suspenso");
}
```

```js
switch (estado) {
  case "pendiente":
    preparar();
    break;
  case "terminado":
    mostrarResultado();
    break;
  default:
    mostrarError();
}
```

### Bucles

```js
for (let i = 0; i < 3; i += 1) {
  console.log(i);
}

for (const valor of valores) {
  console.log(valor); // Recorre valores de un iterable
}

for (const clave in objeto) {
  console.log(clave, objeto[clave]); // Recorre propiedades enumerables
}
```

`for...of` es adecuado para arrays. `for...in` se reserva para claves de objetos y no debe emplearse para asumir el orden de un array.

## Funciones

Las funciones son valores: pueden guardarse en variables, pasarse como argumentos y devolverse desde otras funciones.

```js
function sumar(a, b = 0) {
  return a + b;
}

const duplicar = (numero) => numero * 2;

const aplicar = (valor, operacion) => operacion(valor);
aplicar(4, duplicar); // 8
```

Las declaraciones `function` se elevan y pueden invocarse antes de aparecer en el archivo. Las expresiones y funciones flecha solo están disponibles después de inicializar su variable.

### Parámetro rest

```js
function sumarTodos(...numeros) {
  return numeros.reduce((total, numero) => total + numero, 0);
}
```

Solo puede existir un parámetro `rest`, debe ser el último y no puede tener valor predeterminado.

### Ámbito y cierres

Una función conserva acceso al entorno léxico donde fue creada. Esto se denomina **closure** o cierre.

```js
function crearContador() {
  let valor = 0;

  return () => {
    valor += 1;
    return valor;
  };
}

const contar = crearContador();
contar(); // 1
contar(); // 2
```

## Objetos y clases

Un objeto agrupa propiedades y métodos.

```js
const persona = {
  nombre: "Ana",
  edad: 25,
  saludar() {
    return `Hola, soy ${this.nombre}`;
  },
};

persona.nombre;
persona["edad"];
```

La notación con corchetes es necesaria cuando la clave se calcula o no es un identificador válido.

JavaScript usa herencia mediante prototipos. La sintaxis `class` ofrece una forma más clara de definir constructores y métodos sobre ese mecanismo.

```js
class Persona {
  constructor(nombre, edad) {
    this.nombre = nombre;
    this.edad = edad;
  }

  saludar() {
    return `Hola, soy ${this.nombre}`;
  }
}

class Estudiante extends Persona {
  constructor(nombre, edad, grado) {
    super(nombre, edad);
    this.grado = grado;
  }
}
```

En una función normal, `this` depende de cómo se invoca. Una función flecha no crea su propio `this`, sino que conserva el del contexto exterior.

## Errores y excepciones

```js
function dividir(a, b) {
  if (b === 0) {
    throw new RangeError("El divisor no puede ser cero");
  }

  return a / b;
}

try {
  console.log(dividir(10, 0));
} catch (error) {
  console.error(error.message);
} finally {
  console.log("Operación finalizada");
}
```

Debe lanzarse un objeto `Error` o una de sus subclases para conservar mensaje y traza.

## BOM y DOM

El **Browser Object Model** expone funciones del navegador. `window` es el objeto global del contexto de una pestaña e incluye APIs como `location`, `history`, temporizadores y almacenamiento.

El **Document Object Model** representa el documento HTML como un árbol de nodos modificable desde JavaScript.

### Selección y modificación

```js
const titulo = document.querySelector("#titulo");
const tarjetas = document.querySelectorAll(".tarjeta");

titulo.textContent = "Nuevo título";
titulo.classList.add("destacado");
titulo.setAttribute("aria-live", "polite");
```

`querySelector` devuelve el primer elemento que coincide o `null`; `querySelectorAll` devuelve una colección de coincidencias. Para insertar texto se prefiere `textContent`. `innerHTML` interpreta etiquetas y no debe recibir contenido no confiable.

### Creación y eliminación

```js
const elemento = document.createElement("li");
elemento.textContent = "Nueva tarea";
document.querySelector("#lista").append(elemento);

elemento.remove();
```

## Eventos

```js
const boton = document.querySelector("#guardar");

boton.addEventListener("click", (event) => {
  event.preventDefault();
  console.log("Guardado");
});
```

El objeto `event` informa del tipo de evento, el elemento que lo originó (`target`) y el elemento cuyo manejador se ejecuta (`currentTarget`). Los eventos suelen propagarse desde el elemento hacia sus antecesores.

La delegación permite administrar elementos dinámicos con un manejador en su contenedor:

```js
lista.addEventListener("click", (event) => {
  const botonEliminar = event.target.closest("[data-action='eliminar']");
  if (!botonEliminar) return;

  botonEliminar.closest("li").remove();
});
```

## Formularios

```js
const formulario = document.querySelector("#registro");

formulario.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!formulario.checkValidity()) {
    formulario.reportValidity();
    return;
  }

  const datos = Object.fromEntries(new FormData(formulario));
  console.log(datos);
});
```

La validación del navegador mejora la experiencia, pero un servidor debe volver a validar todos los datos recibidos.

## Almacenamiento local

`localStorage` persiste pares clave-valor de tipo cadena para el origen actual. Los objetos deben convertirse a JSON.

```js
const preferencias = { tema: "oscuro", tamano: 16 };
localStorage.setItem("preferencias", JSON.stringify(preferencias));

const guardadas = JSON.parse(localStorage.getItem("preferencias") ?? "{}");
localStorage.removeItem("preferencias");
```

No debe utilizarse para contraseñas, tokens sensibles ni grandes cantidades de datos.

## Programación asíncrona

El motor ejecuta la pila de JavaScript. El navegador se encarga de temporizadores, red y eventos. Cuando una operación termina, su continuación entra en una cola y el bucle de eventos la ejecuta cuando la pila queda libre.

### Callbacks

```js
setTimeout(() => {
  console.log("Han pasado dos segundos");
}, 2000);
```

Un callback no bloquea el hilo mientras espera, pero encadenar muchos callbacks puede dificultar el control de errores y el flujo.

### Promesas

Una promesa se encuentra pendiente y termina resuelta con un valor o rechazada con un error.

```js
obtenerDatos()
  .then((datos) => procesar(datos))
  .then((resultado) => console.log(resultado))
  .catch((error) => console.error(error))
  .finally(() => ocultarCarga());
```

### Async y await

Una función `async` siempre devuelve una promesa. `await` suspende esa función, no todo el hilo.

```js
async function cargarDatos() {
  try {
    const datos = await obtenerDatos();
    return procesar(datos);
  } catch (error) {
    console.error("No se pudieron cargar los datos", error);
    throw error;
  }
}
```

Las operaciones independientes pueden iniciarse a la vez:

```js
const [usuarios, tareas] = await Promise.all([
  obtenerUsuarios(),
  obtenerTareas(),
]);
```

Esperarlas secuencialmente aumentaría el tiempo total sin necesidad.

## Módulos

```js
// operaciones.js
export const sumar = (a, b) => a + b;

// app.js
import { sumar } from "./operaciones.js";
console.log(sumar(2, 3));
```

Los módulos tienen su propio ámbito. En el navegador deben servirse normalmente mediante HTTP, no abriendo directamente el archivo con `file://`.
