package com.juan.procesamientodatos
package scalaClase.classes

import scalaClase.traits.{Nadador, Volador}

class Pato extends Nadador with Volador {
  def hacerSonido(): Unit = println("Cuac cuac!")
}
