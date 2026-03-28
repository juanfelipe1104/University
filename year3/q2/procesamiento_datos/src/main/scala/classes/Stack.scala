package com.juan.procesamientodatos
package classes

class Stack[T] {
  private var elems: List[T] = Nil
  def push(x: T): Unit = { elems = x :: elems }
  def top: T = elems.head
  def pop(): Unit = { elems = elems.tail }
}
