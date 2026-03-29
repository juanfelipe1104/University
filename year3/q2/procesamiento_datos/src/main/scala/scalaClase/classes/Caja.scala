package com.juan.procesamientodatos
package scalaClase.classes

class Caja[T](private var valor: T) {

  // Método para obtener el valor almacenado
  def obtener(): T = valor

  // Método para actualizar el valor almacenado
  def actualizar(nuevoValor: T): Unit = {
    valor = nuevoValor
  }

  // Sobrescribir toString para mostrar el contenido de la caja
  override def toString: String = s"Caja contiene: $valor"
}
