package com.juan.procesamientodatos
package scalaClase

import scalaClase.classes.Longitud

import scala.language.implicitConversions

/*
En este ejercicio, los estudiantes aprenderán a utilizar implicits para trabajar con unidades de medida, permitiendo realizar conversiones automáticas entre diferentes unidades de longitud, como metros y kilómetros.

Requisitos:
Definir un tipo Longitud:
Crea una clase Longitud que represente una medida de longitud en metros (Double).

Agregar conversiones implícitas:
Implementa una conversión implícita para transformar metros a kilómetros y viceversa.

Métodos adicionales mediante implicit class:
Crea un metodo adicional para la clase Longitud llamado aKilometros que convierta metros a kilómetros, y un metodo aMetros que convierta kilómetros a metros. Ambos métodos deben devolver una nueva instancia de Longitud con la unidad convertida.

Realizar pruebas:
Usa los métodos y conversiones implícitas para realizar operaciones entre diferentes unidades de longitud.

Pistas:
Utiliza implicit def para convertir entre Double (representando kilómetros) y Longitud (en metros).
Puedes realizar operaciones entre diferentes unidades utilizando las conversiones implícitas, sin necesidad de escribir código adicional para las conversiones.
 */

object implicits extends App {
  implicit def kmToLongitud(km: Double): Longitud = new Longitud(km * 1000)

  implicit def longitudToKm(longitud: Longitud): Double = longitud.metros / 1000

  // 4. Pruebas
  val distanciaEnMetros = new Longitud(1500)
  println(distanciaEnMetros.aKilometros) // Salida: 1.5 metros en kilómetros
  println(distanciaEnMetros.aMetros) // Salida: 1500000 metros

  val distanciaEnKm: Longitud = 2.5 // Se convierte automáticamente a Longitud en metros
  println(distanciaEnKm) // Salida: 2500 metros

  val distanciaEnMetros2: Double = distanciaEnMetros // Se convierte automáticamente a Double
  println(distanciaEnMetros2) // Salida: 1.5 metros
}