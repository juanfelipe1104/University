package com.juan.procesamientodatos
package scalaClase.classes

class Perro(nombre: String) extends Animal(nombre) {
  def hacerSonido(): Unit = println(s"$nombre dice: Guau!")
}
