package com.juan.procesamientodatos
package scalaClase.classes

// Definimos la clase base
abstract class Expr
// Expresión para números
case class Number(n: Double) extends Expr
// Expresión para variables
case class Var(name: String) extends Expr
// Operaciones unarias (ej. negación)
case class UnOp(operator: String, arg: Expr) extends Expr
// Operaciones binarias (ej. suma, multiplicación)
case class BinOp(operator: String, left: Expr, right: Expr) extends Expr
