package com.juan.procesamientodatos
import classes.{Expr, BinOp, Number, UnOp, Var, Persona}



object pattern extends App {
  private val expr1 = UnOp("-", UnOp("-", Number(5)))
  private val expr2 = BinOp("+", Var("x"), Number(0))
  private val expr3 = BinOp("*", Var("y"), Number(1))
  private val expr4 = BinOp("+", Number(3), Number(4))

  private def simplifyTop(expr: Expr): Expr = expr match {
    case UnOp("-", UnOp("-", e))  => e
    case BinOp("+", e, Number(0)) => e
    case BinOp("+", Number(0), e) => e
    case BinOp("*", e, Number(1)) => e
    case BinOp("*", Number(1), e) => e
    case _                        => expr
  }
  println(simplifyTop(expr1))
  println(simplifyTop(expr2))
  println(simplifyTop(expr3))
  println(simplifyTop(expr4))
}

/*
Se desea modelar un sistema que clasifique personas según su edad usando pattern matching en Scala.
Requerimientos:
1) Define una case class llamada Persona con dos atributos:
 - nombre: String
- edad: Int
2) Implementa una función clasificarPersona(p: Persona): String que:
- Devuelva "Menor de edad" si la persona tiene menos de 18 años.
- Devuelva "Adulto" si la persona tiene entre 18 y 65 años.
- Devuelva "Adulto mayor" si la persona tiene más de 65 años.
3) Prueba la función con diferentes instancias de Persona.
 */

object pattern2 extends App {
  private def describirPersona(p: Persona): String = p match {
    case Persona(nombre, edad) if edad < 18  => s"$nombre es menor de edad."
    case Persona(nombre, edad) if edad <= 65 => s"$nombre es adulto."
    case other => s"${other.nombre} es adulto mayor."
  }
  private val p1 = Persona("Juan", 16)
  private val p2 = Persona("Ana", 25)
  private val p3 = Persona("Sara", 70)
  println(describirPersona(p1)) // Salida: Juan es menor de edad.
  println(describirPersona(p2)) // Salida: Ana es adulto.
  println(describirPersona(p3)) // Salida: Sara es adulto mayor.
}
