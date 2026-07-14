# Arrays y objetos en JavaScript

## Arrays

Un array es una colección ordenada y redimensionable. Sus elementos se consultan mediante índices desde cero y pueden pertenecer a tipos distintos, aunque una estructura homogénea suele ser más fácil de mantener.

```js
const valores = [10, 20, 30];

valores[0];       // 10
valores.at(-1);   // 30
valores.length;   // 3
```

Leer una posición inexistente devuelve `undefined`. Asignar una posición alejada crea huecos, por lo que debe evitarse:

```js
const valores = [1, 2, 3];
valores[9] = 10;
// [1, 2, 3, <6 elementos vacíos>, 10]
```

## Mutación y copia

| Método | Acción | Modifica el array |
|---|---|---|
| `push` / `pop` | Añade o elimina al final | Sí |
| `unshift` / `shift` | Añade o elimina al principio | Sí |
| `splice` | Inserta, sustituye o elimina en cualquier posición | Sí |
| `slice` | Copia un intervalo | No |
| `concat` | Combina arrays | No |
| `toSorted` | Devuelve una copia ordenada | No |

```js
const original = [1, 2, 3];
const copia = [...original];
const ampliado = [0, ...original, 4];
```

El operador spread crea una **copia superficial**: copia el array exterior, pero conserva las referencias a los objetos internos.

```js
const original = [{ nombre: "Ana" }];
const copia = [...original];

copia[0].nombre = "Luis";
console.log(original[0].nombre); // "Luis"
```

Para datos compatibles puede usarse `structuredClone(original)` cuando se necesita una copia profunda.

## Recorrido y transformación

Los métodos iterativos reciben normalmente un callback con `(elemento, indice, array)`. La mayoría de las veces solo se necesita el elemento.

### map

Crea un array con el resultado de transformar cada elemento. Conserva la misma longitud.

```js
const dobles = [1, 2, 3].map((numero) => numero * 2);
// [2, 4, 6]
```

### filter

Crea un array con los elementos que cumplen una condición.

```js
const pares = [1, 2, 3, 4].filter((numero) => numero % 2 === 0);
// [2, 4]
```

### find y findIndex

`find` devuelve el primer elemento que cumple la condición; `findIndex`, su posición. Si no existe, devuelven `undefined` y `-1`, respectivamente.

```js
const usuarios = [{ id: 1 }, { id: 2 }];
const usuario = usuarios.find((elemento) => elemento.id === 2);
```

### some y every

```js
[1, 2, 3].some((numero) => numero > 2);  // true
[1, 2, 3].every((numero) => numero > 0); // true
```

`some` comprueba si al menos uno cumple la condición; `every`, si la cumplen todos. Ambos dejan de recorrer cuando ya conocen el resultado.

### forEach

Ejecuta una operación por elemento y devuelve `undefined`. Se utiliza para efectos secundarios, no para construir otro array.

```js
usuarios.forEach((usuario) => console.log(usuario.id));
```

No permite detener el recorrido con `break` ni espera callbacks asíncronos. Para esos casos se usa un bucle `for...of`.

### reduce

Combina todos los elementos en un acumulador.

```js
const total = [10, 20, 30].reduce(
  (acumulador, numero) => acumulador + numero,
  0,
);
```

El segundo argumento es el valor inicial. Incluirlo evita errores con arrays vacíos y hace explícito el tipo del acumulador.

## Ordenación

`sort` modifica el array y compara cadenas por defecto:

```js
[40, 100, 5].sort(); // [100, 40, 5]
```

Para números se proporciona un comparador:

```js
const numeros = [40, 100, 5];
const ascendente = [...numeros].sort((a, b) => a - b);
const descendente = [...numeros].sort((a, b) => b - a);
```

En entornos que lo soporten, `toSorted((a, b) => a - b)` devuelve directamente una copia.

## Arrays anidados

```js
const anidado = [1, [2, [3, 4]]];

anidado.flat();          // [1, 2, [3, 4]]
anidado.flat(2);         // [1, 2, 3, 4]
anidado.flat(Infinity);  // Aplana todos los niveles
```

`flatMap` equivale a aplicar `map` y aplanar un nivel:

```js
const palabras = ["hola mundo", "JavaScript web"];
const tokens = palabras.flatMap((frase) => frase.split(" "));
```

## Desestructuración

### Arrays

```js
const colores = ["rojo", "verde", "azul"];
const [primero, segundo, tercero = "negro"] = colores;

const [cabeza, ...resto] = colores;
```

Se pueden omitir posiciones:

```js
const [, segundo] = colores;
```

### Objetos

```js
const usuario = { id: 1, nombre: "Ana", edad: 25 };
const { id, nombre: nombreVisible, pais = "España" } = usuario;
const { id: identificador, ...datos } = usuario;
```

La desestructuración de objetos busca por nombre de propiedad, no por posición.

## Spread y rest

Ambos usan `...`, pero cumplen funciones opuestas:

- **spread** expande un iterable u objeto;
- **rest** agrupa los valores restantes.

```js
const base = [2, 3];
const numeros = [1, ...base, 4];

Math.max(...numeros);

const configuracion = { tema: "claro", idioma: "es" };
const actualizada = { ...configuracion, tema: "oscuro" };
```

En un objeto, las propiedades posteriores sobrescriben las anteriores.

## Objetos

```js
const nombre = "Ana";
const usuario = {
  nombre,
  edad: 25,
  activo: true,
};

usuario.edad;
usuario["activo"];
```

### Operaciones habituales

```js
Object.keys(usuario);     // Claves
Object.values(usuario);   // Valores
Object.entries(usuario);  // Pares [clave, valor]
Object.hasOwn(usuario, "edad");
```

```js
for (const [clave, valor] of Object.entries(usuario)) {
  console.log(clave, valor);
}
```

Los objetos se comparan por identidad, no por contenido:

```js
{} === {}; // false

const a = {};
const b = a;
a === b;   // true
```

## Set y Map

`Set` almacena valores únicos:

```js
const unicos = [...new Set([1, 2, 2, 3])];
// [1, 2, 3]
```

`Map` almacena pares clave-valor y admite claves de cualquier tipo:

```js
const puntuaciones = new Map();
puntuaciones.set("Ana", 10);
puntuaciones.get("Ana"); // 10
puntuaciones.has("Ana"); // true
```

## Encadenamiento de operaciones

```js
const total = [5, 10, 15, 20, 25]
  .filter((numero) => numero > 10)
  .map((numero) => numero * 2)
  .reduce((suma, numero) => suma + numero, 0);
```

Cada paso debe representar una transformación clara. Si la cadena realiza demasiadas tareas o recorre un conjunto muy grande varias veces, un bucle explícito puede resultar más legible o eficiente.
