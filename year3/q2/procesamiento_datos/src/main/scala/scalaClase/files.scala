package com.juan.procesamientodatos
package scalaClase

import scala.io.Source
import java.io.PrintWriter

/*
En este ejercicio, trabajarás con lectura y escritura de archivos en Scala utilizando la biblioteca scala.io.Source y la clase PrintWriter.

Tareas:
1. Leer un archivo de texto ubicado en la ruta /home/bigdata/microcuento.txt.
2. Obtener estadísticas sobre el contenido del archivo:
   - Número total de líneas.
   - Verificar si todas las líneas tienen más de 50 o 100 caracteres.
   - Buscar la existencia de ciertas palabras como "llaves" o "datos".
   - Obtener el tamaño de todas las líneas que comienzan con la letra "U".
   - Extraer líneas que contengan más de 20 caracteres distintos.
   - Convertir el archivo a un solo string con separadores de línea.
   - Obtener la primera línea de forma segura (si no hay líneas, devolver "No hay primera línea").
   - Relacionar las primeras 10 líneas con un rango de números usando zip.
3. Escribir en un nuevo archivo ubicado en "/home/bigdata/microcuento_uppercase.txt":
   - Convertir todas las líneas del texto original a mayúsculas.
   - Guardar el resultado en el nuevo archivo.
 */

object files extends App {
  private val filenameInput = "src/main/scala/files/microcuento.txt"
  private val fileReader = Source.fromFile(filenameInput)
  private val lines = fileReader.getLines().toList
  fileReader.close()
  println(lines.size)
  println(lines.forall(_.length > 50))
  println(lines.forall(_.length > 100))

  println(lines.exists(_.contains("llaves")))
  println(lines.exists(_.contains("datos")))

  println(lines.collect { case line if line.startsWith("U") => line.length })

  println(lines.takeWhile(_.distinct.length > 20))

  println(lines.mkString(System.lineSeparator()))

  println(Range.inclusive(1,10).zip(lines).mkString(System.lineSeparator()))

  println(Range.inclusive(1,10).zip(lines).mkString(System.lineSeparator()))

  // Escritura de ficheros

  private val filenameOutput = "src/main/scala/files/microcuento_uppercase.txt"
  private val printWriter = new PrintWriter(filenameOutput)

  lines.foreach(line => printWriter.println(line.toUpperCase))

  printWriter.close()

}