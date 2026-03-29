package com.juan.procesamientodatos
package scalaClase.classes

class Longitud(val metros: Double) {
  def aKilometros: Longitud = new Longitud(metros / 1000)
  def aMetros: Longitud = new Longitud(metros * 1000)

  override def toString: String = s"$metros metros"
}
