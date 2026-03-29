package com.juan.procesamientodatos
package scalaClase.classes

import scalaClase.traits.Aereo

class Avion(nombre: String) extends Vehiculo(nombre) with Aereo {
  def tipoCombustible(): String = "Querosen"
}
