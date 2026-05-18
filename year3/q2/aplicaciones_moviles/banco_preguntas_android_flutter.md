# Banco completo de preguntas tipo test Android, Kotlin, Dart y Flutter

> Banco unificado con 24 preguntas diferentes.  
> La respuesta correcta aparece marcada con **(CORRECTA)**.

---

## Pregunta 1

**¿Cuál es la forma correcta de acceder a un recurso de color definido en `colors.xml` desde el fichero `activity_main.xml`?**

- A) `@colors/my_color` **(CORRECTA)** *(opción esperada en algunos tests)*
- B) `getColor(R.color.my_color)`
- C) `R.color.my_color`
- D) `resources.getColor(R.color.my_color)`

> **Nota:** técnicamente, en XML Android la forma correcta real es `@color/my_color`, en singular. `@colors/my_color` está mal escrito, pero si esa es la opción que aparece en el test, probablemente es la que esperan marcar.

---

## Pregunta 2

**¿Cuál de las siguientes es una implementación y no una extensión?**

- A) `abstract class Clase : Implementacion()`
- B) `final class Clase : Implementacion()`
- C) `class Clase : Implementacion()`
- D) `class Clase : Implementacion` **(CORRECTA)**

---

## Pregunta 3

**Si utilizamos `ConstraintLayout`, ¿cuál es la única restricción que debe cumplir un elemento?**

- A) Que tenga `id`
- B) Que al menos tenga una restricción por eje **(CORRECTA)**
- C) Que tenga `id` y que al menos tenga restricción en un eje
- D) Que tenga `id` y que al menos tenga una restricción por eje

> **Nota:** técnicamente, en `ConstraintLayout` una vista debe estar restringida en el eje horizontal y en el eje vertical. El `id` solo es necesario si se quiere referenciar esa vista desde otra o desde código.

---

## Pregunta 4

**¿Cuál de los siguientes métodos del ciclo de vida de una `Activity` se encarga de asociar la parte gráfica con la parte lógica?**

- A) `onCreateView`
- B) `onStop`
- C) `onCreate` **(CORRECTA)**
- D) `onStart`

---

## Pregunta 5

**Cuando trabajamos con Dart, si tenemos la siguiente definición de función `saludo(String texto, {var nombre})`, ¿cuál de los siguientes usos es el correcto?**

- A) `saludo("hola", nombre="Juan")` **(CORRECTA)** *(opción esperada en algunos tests)*
- B) `saludo(texto="hola", nombre="Juan")`
- C) `saludo(nombre="Juan")`
- D) `saludo("hola", "Juan")`

> **Nota:** en Dart real, los argumentos nombrados se pasan con `:`, no con `=`. La llamada correcta sería `saludo("hola", nombre: "Juan")`.

---

## Pregunta 6

**¿Cuál es la diferencia entre `final` y `const` en Dart?**

- A) `final` se asigna en tiempo de ejecución, `const` en tiempo de compilación **(CORRECTA)**
- B) `final` se asigna en tiempo de compilación, `const` en tiempo de ejecución
- C) `final` permite valores cambiantes, `const` no
- D) `const` puede cambiar su valor en tiempo de ejecución

---

## Pregunta 7

**¿Cuál de las siguientes afirmaciones sobre un `ActionBar` es correcta?**

- A) Tan solo permite poner menú y un título
- B) Es menos útil que un `Toolbar` **(CORRECTA)**
- C) Es necesario modificar el diseño original para que pueda aparecer
- D) Hay que declararla dentro del XML

---

## Pregunta 8

**¿Cuál de los siguientes métodos del ciclo de vida de un `Fragment` es necesario para que tenga parte gráfica?**

- A) `onAttach`
- B) `onViewCreated`
- C) `onCreateView` **(CORRECTA)**
- D) `onCreate`

---

## Pregunta 9

**En Dart, si queremos usar varios constructores en un objeto, ¿es posible?**

- A) Sí, siempre y cuando exista una sobrecarga del constructor
- B) No, en Dart solo existe un constructor primario
- C) Sí, siempre y cuando se utilicen constructores adicionales nominales **(CORRECTA)**
- D) Sí, definiendo junto al nombre de la clase el primario y el resto con la palabra `constructor`

---

## Pregunta 10

**En Dart, existe el operador null safety y se utiliza de la siguiente forma:**

- A) `println("El siguiente dato puede ser nulo {dato ? "sin valor"}")`
- B) `println("El siguiente dato puede ser nulo {dato ?: "sin valor"}")`
- C) `println("El siguiente dato puede ser nulo {dato ?? "sin valor"}")` **(CORRECTA)**
- D) `println("El siguiente dato puede ser nulo {dato ??: "sin valor"}")`

> **Nota:** en Dart real, lo habitual sería usar `print` y la interpolación correcta sería `${dato ?? "sin valor"}`.

---

## Pregunta 11

**Los `Fragments` representan:**

- A) Un elemento lógico que sustituye a una `Activity`
- B) Un elemento que permite comunicar dos pantallas entre sí
- C) Una característica de Android para poder hacer comunicaciones de red
- D) Una parte gráfica que se puede ocultar / mostrar en un momento determinado **(CORRECTA)**

---

## Pregunta 12

**¿Qué método del ciclo de vida de una `Activity` es llamado justo antes de que la UI sea visible al usuario?**

- A) `onPause()`
- B) `onResume()`
- C) `onCreate()`
- D) `onStart()` **(CORRECTA)**

---

## Pregunta 13

**En Flutter, si queremos utilizar un `StatefulWidget` tendremos:**

- A) Una clase que implementa `State`
- B) Una sola clase que extienda de `Stateful`
- C) Una clase que extiende de `State`
- D) Una clase que extiende de `StatefulWidget` y otra que extienda de `State` **(CORRECTA)**

---

## Pregunta 14

**¿Cuál de los siguientes métodos no pertenece al ciclo de vida de una `Activity`?**

- A) `onCreateOptionMenu` **(CORRECTA)**
- B) `onPause`
- C) `onCreate`
- D) `onDestroy`

> **Nota:** el método de menú correcto se llama `onCreateOptionsMenu`, con `Options` en plural. Aun así, no forma parte del ciclo de vida principal de una `Activity`.

---

## Pregunta 15

**¿Cuál es el comportamiento de una `Activity` cuando el dispositivo rota?**

- A) Solo se recrea la vista actual
- B) La `Activity` se destruye y se vuelve a crear **(CORRECTA)**
- C) No ocurre ningún cambio
- D) Se llama a `onPause()` y luego a `onStop()`, pero no a `onDestroy()`

---

## Pregunta 16

**¿Qué operador se utiliza en Kotlin para ejecutar una expresión solo si el valor no es nulo?**

- A) `?.` **(CORRECTA)**
- B) `let`
- C) `!!`
- D) `?:`

---

## Pregunta 17

**Indica cuál afirmación es falsa sobre XML y componentes en Android.**

- A) El atributo `id` es obligatorio para definir un componente en XML **(CORRECTA)**
- B) Si no se indica `orientation` en `LinearLayout`, es horizontal por defecto
- C) Un `RecyclerView` puede tener scroll vertical u horizontal
- D) El atributo `layout_height` puede ser `wrap_content`, `match_parent` o `0dp`

---

## Pregunta 18

**Para representar una lista de datos, ¿qué elemento es mejor?**

- A) Cualquiera de las anteriores
- B) `ListView`
- C) `RecyclerView` **(CORRECTA)**
- D) `GridView`

---

## Pregunta 19

**¿Qué hace el widget `Expanded` en Flutter?**

- A) Hace que su `child` ocupe solo el espacio necesario
- B) Muestra un widget después de forma centrada
- C) Indica que el `child` ocupará todo el espacio disponible en su eje principal **(CORRECTA)**
- D) Oculta su hijo hasta que se presione

---

## Pregunta 20

**Indica el tipo de retorno de la siguiente función definida en Dart: `realizarSuma({int operado1, int operando2})`**

- A) `dynamic` **(CORRECTA)**
- B) `int`
- C) `double`
- D) `void`

---

## Pregunta 21

**En un menú XML, ¿cuál atributo es indispensable para crear un `menu item`?**

- A) Todas las anteriores
- B) `showAsAction`
- C) `id` **(CORRECTA)**
- D) `title`

---

## Pregunta 22

**¿Cuál afirmación sobre Kotlin es falsa?**

- A) Las variables pueden ser mutables o no mutables
- B) Sirve para crear aplicaciones multiplataforma
- C) Es una transpilación de Java **(CORRECTA)**
- D) Es un lenguaje totalmente independiente

---

## Pregunta 23

**¿Cuál es el propósito del archivo `AndroidManifest.xml`?**

- A) Almacenar cadenas para internacionalización
- B) Declarar componentes y permisos **(CORRECTA)**
- C) Controlar diseño de la interfaz
- D) Definir rutas de navegación

---

## Pregunta 24

**¿Cuál es el propósito del archivo `build.gradle` en un proyecto Android?**

- A) Definir el diseño de la interfaz de usuario
- B) Especificar los componentes del manifiesto
- C) Configurar dependencias y opciones de compilación del proyecto **(CORRECTA)**
- D) Gestionar las traducciones de la app

