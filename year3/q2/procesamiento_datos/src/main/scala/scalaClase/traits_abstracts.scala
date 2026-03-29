package com.juan.procesamientodatos
package scalaClase

import classes._
import traits.{Acuatico, Aereo, Terrestre}

object traits_abstracts extends App {
  private val pajaro = new Pajaro()
  pajaro.volar() // Salida: Estoy volando
}

object traits_abstracts2 extends App {
  private val perro = new Perro("Max")
  perro.hacerSonido() // Salida: Max dice: ¡Guau!
}

object traits_abstracts3 extends App {
  private val pato = new Pato()
  pato.nadar()     // Salida: Estoy nadando
  pato.volar()     // Salida: Estoy volando
  pato.hacerSonido() // Salida: Cuac cuac!
}

/*
Vas a modelar un sistema de vehículos en Scala. Algunos vehículos pueden volar, otros pueden navegar y otros pueden conducir por tierra. Deberás utilizar traits para representar estas habilidades y clases para los diferentes tipos de vehículos. Además, cada vehículo debe tener un atributo: su nombre, y debe definir el tipo de combustible.
Genera las clases Avion y Anfibio y llama a los métodos correspondientes para obtener la siguiente salida:
> Boeing 747 usa Querosen
> Volando por el cielo
>
> AmphiCar usa Híbrido
> Conduciendo por la carretera
> Navegando en el agua
 */

object traits_abstract4 extends App {
  // Programa principal
  private val avion = new Avion("Boeing 747")
  println(s"${avion.nombre} usa ${avion.tipoCombustible()}")
  avion.volar()

  private val anfibio = new Anfibio("AmphiCar")
  println(s"${anfibio.nombre} usa ${anfibio.tipoCombustible()}")
  anfibio.conducir()
  anfibio.navegar()

  private def muevete(vehiculo: Vehiculo): Unit = vehiculo match {
    case te: Terrestre => te.conducir()
    case ac: Acuatico => ac.navegar()
    case ae: Aereo => ae.volar()
    case _ => println("Sin movimiento")
  }

  muevete(avion)
  muevete(anfibio)
}