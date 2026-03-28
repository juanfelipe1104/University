package com.juan.procesamientodatos
package classes

class Box[T](content: T) {
  def getContent: T = content

  def map[U](f: T => U): Box[U] = {
    val mappedContent = f(content)
    new Box(mappedContent)
  }
}
