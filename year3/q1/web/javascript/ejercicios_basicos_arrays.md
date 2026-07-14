# Ejercicios básicos de arrays

## 1. Clonar un array con spread

**Enunciado:** Dado `[1, 2, 3]`, crea una copia exacta usando el operador spread.

**Solución:**

```js
const original = [1, 2, 3];
const copia = [...original];

console.log(copia); // [1, 2, 3]
```

## 2. Combinar arrays

**Enunciado:** Une `[1, 2, 3]` y `[4, 5, 6]` en un solo array con spread.

**Solución:**

```js
const primeraParte = [1, 2, 3];
const segundaParte = [4, 5, 6];
const numeros = [...primeraParte, ...segundaParte];

console.log(numeros); // [1, 2, 3, 4, 5, 6]
```

## 3. Añadir elementos con spread

**Enunciado:** A `[10, 20, 30]`, añade `5` al inicio y `40` al final usando spread.

**Solución:**

```js
const numeros = [10, 20, 30];
const ampliado = [5, ...numeros, 40];

console.log(ampliado); // [5, 10, 20, 30, 40]
```

## 4. Rest en desestructuración

**Enunciado:** Extrae el primer elemento de `[1, 2, 3, 4, 5]` y guarda el resto en otra variable usando rest.

**Solución:**

```js
const numeros = [1, 2, 3, 4, 5];
const [primero, ...resto] = numeros;

console.log(primero); // 1
console.log(resto);   // [2, 3, 4, 5]
```

## 5. Función con parámetros variables

**Enunciado:** Crea una función `suma(...nums)` que devuelva la suma de todos sus parámetros usando `reduce`.

**Solución:**

```js
function suma(...nums) {
  return nums.reduce((total, numero) => total + numero, 0);
}

console.log(suma(1, 2, 3, 4)); // 10
```

## 6. Map básico

**Enunciado:** Multiplica por `2` cada número de `[1, 2, 3, 4]` usando `map`.

**Solución:**

```js
const numeros = [1, 2, 3, 4];
const dobles = numeros.map((numero) => numero * 2);

console.log(dobles); // [2, 4, 6, 8]
```

## 7. Filter

**Enunciado:** Filtra los números pares de `[1, 2, 3, 4, 5, 6]`.

**Solución:**

```js
const numeros = [1, 2, 3, 4, 5, 6];
const pares = numeros.filter((numero) => numero % 2 === 0);

console.log(pares); // [2, 4, 6]
```

## 8. Find

**Enunciado:** Encuentra el primer número mayor que `10` en `[4, 9, 16, 25, 36]`.

**Solución:**

```js
const numeros = [4, 9, 16, 25, 36];
const encontrado = numeros.find((numero) => numero > 10);

console.log(encontrado); // 16
```

## 9. Some

**Enunciado:** Comprueba si al menos un número de `[5, 8, 12, 20]` es mayor que `15`.

**Solución:**

```js
const numeros = [5, 8, 12, 20];
const hayMayorQueQuince = numeros.some((numero) => numero > 15);

console.log(hayMayorQueQuince); // true
```

## 10. Every

**Enunciado:** Comprueba si todos los números de `[2, 4, 6, 8]` son pares.

**Solución:**

```js
const numeros = [2, 4, 6, 8];
const todosSonPares = numeros.every((numero) => numero % 2 === 0);

console.log(todosSonPares); // true
```

## 11. Reduce básico

**Enunciado:** Calcula el producto de `[1, 2, 3, 4]` usando `reduce`.

**Solución:**

```js
const numeros = [1, 2, 3, 4];
const producto = numeros.reduce(
  (acumulador, numero) => acumulador * numero,
  1,
);

console.log(producto); // 24
```

## 12. Sort numérico

**Enunciado:** Ordena `[40, 100, 1, 5, 25, 10]` de menor a mayor.

**Solución:**

```js
const numeros = [40, 100, 1, 5, 25, 10];
const ordenados = [...numeros].sort((a, b) => a - b);

console.log(ordenados); // [1, 5, 10, 25, 40, 100]
```

## 13. forEach

**Enunciado:** Recorre `[1, 2, 3]` e imprime cada valor multiplicado por `3`.

**Solución:**

```js
const numeros = [1, 2, 3];

numeros.forEach((numero) => {
  console.log(numero * 3);
});

// 3
// 6
// 9
```

## 14. Rest en objetos

**Enunciado:** Dado `{ id: 1, nombre: "Ana", edad: 25, pais: "España" }`, extrae `id` y guarda el resto en otro objeto.

**Solución:**

```js
const persona = {
  id: 1,
  nombre: "Ana",
  edad: 25,
  pais: "España",
};

const { id, ...datosPersona } = persona;

console.log(id);           // 1
console.log(datosPersona); // { nombre: "Ana", edad: 25, pais: "España" }
```

## 15. Eliminar duplicados

**Enunciado:** Convierte `[1, 2, 2, 3, 4, 4, 5]` en `[1, 2, 3, 4, 5]` usando `filter` e `indexOf`.

**Solución:**

```js
const numeros = [1, 2, 2, 3, 4, 4, 5];
const sinDuplicados = numeros.filter(
  (numero, indice, array) => array.indexOf(numero) === indice,
);

console.log(sinDuplicados); // [1, 2, 3, 4, 5]
```

## 16. Flat

**Enunciado:** Convierte `[[1, 2], [3, [43, 44], [5, 67]]]` en `[1, 2, 3, 43, 44, 5, 67]`.

**Solución:**

```js
const numeros = [[1, 2], [3, [43, 44], [5, 67]]];
const plano = numeros.flat(Infinity);

console.log(plano); // [1, 2, 3, 43, 44, 5, 67]
```

## 17. Transformar objetos con map

**Enunciado:** Dado `[{ nombre: "Ana", edad: 20 }, { nombre: "Luis", edad: 25 }]`, devuelve un array que contenga solo los nombres.

**Solución:**

```js
const personas = [
  { nombre: "Ana", edad: 20 },
  { nombre: "Luis", edad: 25 },
];

const nombres = personas.map((persona) => persona.nombre);

console.log(nombres); // ["Ana", "Luis"]
```

## 18. Encadenar métodos

**Enunciado:** Dado `[5, 10, 15, 20, 25]`, filtra los mayores que `10`, multiplícalos por `2` y suma el resultado con `reduce`.

**Solución:**

```js
const numeros = [5, 10, 15, 20, 25];

const total = numeros
  .filter((numero) => numero > 10)
  .map((numero) => numero * 2)
  .reduce((suma, numero) => suma + numero, 0);

console.log(total); // 120
```

## 19. Array de números aleatorios

**Enunciado:** Crea un array de `10` elementos y rellénalo con números enteros aleatorios del `1` al `20`.

**Solución:**

```js
const numeros = Array.from(
  { length: 10 },
  () => Math.floor(Math.random() * 20) + 1,
);

console.log(numeros);
```

## 20. Array de colores y números aleatorios

**Enunciado:** Crea un array con el nombre de cinco colores. A partir de él, crea otro array de objetos que contenga el nombre del color y un número aleatorio.

**Solución:**

```js
const colores = ["rojo", "verde", "azul", "amarillo", "morado"];

const coloresConNumero = colores.map((color) => ({
  color,
  numero: Math.floor(Math.random() * 100) + 1,
}));

console.log(coloresConNumero);
```

## 21. Desestructuración de tres valores

**Enunciado:** Define tres variables `a`, `b` y `c` y asigna a cada una un valor de un array ya definido. Hazlo en una línea de código.

**Solución:**

```js
const numeros = [10, 20, 30];
const [a, b, c] = numeros;

console.log(a, b, c); // 10 20 30
```

## 22. Desestructuración con rest

**Enunciado:** Define tres variables `a`, `b` y `c`. Asigna a las dos primeras los dos primeros valores de un array y a la tercera un array con los demás elementos. Hazlo en una línea de código.

**Solución:**

```js
const numeros = [10, 20, 30, 40, 50];
const [a, b, ...c] = numeros;

console.log(a); // 10
console.log(b); // 20
console.log(c); // [30, 40, 50]
```

## 23. Obtener las dos primeras palabras

**Enunciado:** A partir de una cadena que contiene una frase, obtén otra con las dos primeras palabras.

**Solución:**

```js
const frase = "JavaScript permite crear aplicaciones web";
const [primera, segunda] = frase.trim().split(/\s+/);
const primerasPalabras = [primera, segunda]
  .filter((palabra) => palabra !== undefined)
  .join(" ");

console.log(primerasPalabras); // "JavaScript permite"
```

## 24. Obtener la primera y la última palabra

**Enunciado:** A partir de una cadena que contiene una frase, obtén otra con la primera y la última palabra.

**Solución:**

```js
const frase = "JavaScript permite crear aplicaciones web";
const palabras = frase.trim().split(/\s+/);
const [primera] = palabras;
const ultima = palabras.at(-1);
const resultado = primera === ultima ? primera : `${primera} ${ultima}`;

console.log(resultado); // "JavaScript web"
```
