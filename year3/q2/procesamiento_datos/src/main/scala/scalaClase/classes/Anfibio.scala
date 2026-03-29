package com.juan.procesamientodatos
package scalaClase.classes

import scalaClase.traits.{Acuatico, Terrestre}

class Anfibio(nombre: String) extends Vehiculo(nombre) with Terrestre with Acuatico {
  def tipoCombustible(): String = "Híbrido"
}
