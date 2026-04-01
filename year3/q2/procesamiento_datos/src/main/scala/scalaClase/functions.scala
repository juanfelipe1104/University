package com.juan.procesamientodatos
package scalaClase

/*
Define una función filtrarLista que reciba:
- Una lista de enteros (lista).
- Una función (criterio) que tome un entero y devuelva un Boolean (es decir, un predicado).
Luego, usa esta función para filtrar los números pares y los mayores que un cierto valor.
 */

object functions extends App {
  def filtrarLista(lista: List[Int], criterio: Int => Boolean): List[Int] = {
    lista.filter(criterio)
  }

  // Definir funciones de filtrado
  val esPar: Int => Boolean = x => x % 2 == 0
  val mayorQueCinco: Int => Boolean = x => x > 5
  // Uso de la función con distintos criterios
  val numeros = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
  println(filtrarLista(numeros, esPar))
  // Salida esperada: List(2, 4, 6, 8, 10)
  println(filtrarLista(numeros, mayorQueCinco))
  // Salida esperada: List(6, 7, 8, 9, 10)
}

/*
Define una función operar que reciba:
- Dos números enteros (a y b).
- Una función (f) que tome dos enteros y devuelva un entero.
Luego, usa esta función para realizar distintas operaciones matemáticas: suma y multiplicación.
 */

object functions2 extends App {
  def operar(a: Int, b: Int, f: (Int, Int) => Int): Int = {
    f(a, b)
  }

  // Definir funciones de suma y multiplicación
  val suma = (x: Int, y: Int) => x + y
  val multiplicacion = (x: Int, y: Int) => x * y
  // Uso de la función operar con distintas funciones
  println(operar(5, 3, suma)) // Salida esperada: 8
  println(operar(5, 3, multiplicacion)) // Salida esperada: 15
}

object functions3 extends App {
  // Lista de frases
  val frases = List("Hola mundo", "Scala es genial", "La programación funcional es poderosa")

  // Map: Usando map para transformar cada frase en una lista de palabras
  val palabrasConMap = frases.map(frase => frase.split(" "))

  // FlatMap: Usando flatMap para obtener una lista de todas las palabras
  val palabrasConFlatMap = frases.flatMap(frase => frase.split(" "))

  // Imprimir resultados
  println("Resultado usando map:")
  println(palabrasConMap)

  println("\nResultado usando flatMap:")
  println(palabrasConFlatMap)
}

/*
1) Usa map para transformar cada número en una lista que contenga el número y su doble.
(Por ejemplo: el número 2 se convierte en List(2, 4)).

2) Usa flatMap para obtener una única lista con todos los números y sus dobles.
 */

object functions4 extends App {
  val numeros = List(1, 2, 3, 4, 5)
  // Usando map para crear listas con el número y su doble
  val resultadoMap = numeros.map(n => List(n, n * 2))

  // Usando flatMap para obtener una única lista con todos los números y sus dobles
  val resultadoFlatMap = numeros.flatMap(n => List(n, n * 2))

  // Imprimir resultados
  println("Resultado usando map:")
  println(resultadoMap)

  println("\nResultado usando flatMap:")
  println(resultadoFlatMap)
}

object functions5 extends App {
  // Obten el número impar más alto de esta lista:
  val numeros = List(23, 44, 33, 87, 98)
  // Filtrar los números impares:
  val numerosImpares = numeros.filter(_ % 2 != 0)
  println(s"Números impares: $numerosImpares") // Salida: List(23, 33, 87)

  // Encontrar el número impar más alto utilizando reduce:
  val maxImpar = numerosImpares.reduce((a, b) => if (a > b) a else b)
  println(s"El número impar más alto es: $maxImpar") // Salida: 87
}

/*
Dada una lista de números enteros representados como Option[Int], escribe una función que sume todos los valores presentes (es decir, los que no son None) utilizando foldLeft.
Si todos los valores son None, el resultado debe ser 0.
 */

object functions6 extends App {
  val numeros: List[Option[Int]] = List(Option(5), None, Option(10), Option(3), None, Option(7))

  val sumaTotal = numeros.foldLeft(0) { (acumulador, numeroOpt) =>
    numeroOpt match {
      case Some(valor) => acumulador + valor
      case None => acumulador // No sumamos nada si es None
    }
  }

  println(s"La suma total es: $sumaTotal") // Salida esperada: 25
}