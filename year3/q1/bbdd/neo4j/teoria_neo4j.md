# Neo4j

## 1. Modelo de grafos

Neo4j es una base de datos orientada a grafos. La información se representa mediante **nodos**, **relaciones** y **propiedades**. Es especialmente adecuada cuando las conexiones entre entidades son tan importantes como las entidades: redes sociales, recomendaciones, dependencias, rutas o gestión de permisos.

- Un **nodo** representa una entidad, como una persona, un producto o una ciudad.
- Una **relación** conecta dos nodos y expresa su vínculo. Tiene dirección y un tipo.
- Una **propiedad** es un par clave-valor de un nodo o de una relación.
- Una **etiqueta** clasifica nodos. Un nodo puede tener ninguna, una o varias etiquetas.

```text
(ana:Persona {nombre: "Ana", edad: 21})
       -[:AMIGA_DE {desde: 2024}]->
(luis:Persona {nombre: "Luis", edad: 22})
```

El recorrido de relaciones permite encontrar conexiones sin reconstruirlas mediante uniones repetidas. Las relaciones se almacenan con acceso directo a sus nodos de inicio y fin, por lo que el coste depende principalmente de la zona del grafo recorrida.

## 2. Elementos del modelo

### Nodos, etiquetas y propiedades

Un nodo se escribe entre paréntesis. Dentro pueden aparecer, en este orden, una variable, una o varias etiquetas y un mapa de propiedades:

```cypher
()
(n)
(:Persona)
(p:Persona:Estudiante)
(p:Persona {nombre: "Ana", edad: 21})
```

Las variables (`p`, `n`) existen durante la consulta y permiten reutilizar el elemento en otras cláusulas. Las etiquetas no son un tipo rígido: se pueden añadir o eliminar.

Las propiedades admiten valores escalares como texto, números, booleanos, fechas y valores espaciales, además de listas de valores. No se almacenan objetos anidados arbitrarios como propiedad; cuando se necesita una entidad relacionada se suele representar como otro nodo y una relación.

### Relaciones

Una relación se representa con corchetes entre dos nodos. Puede ser dirigida, no dirigida en el patrón de búsqueda, y tener tipo, variable y propiedades:

```cypher
(a)-[:CONOCE]->(b)
(a)<-[:SIGUE]-(b)
(a)-[r:AMIGA_DE {desde: 2024}]->(b)
(a)-[r:SIGUE|BLOQUEA]->(b)
```

Aunque una relación se almacena con dirección, se puede consultar sin imponerla con `--`. Los tipos se suelen escribir en mayúsculas y describen una acción o vínculo: `COMPRA`, `VIVE_EN`, `PERTENECE_A`.

## 3. Patrones y caminos

Cypher es el lenguaje de consultas de Neo4j. Una consulta describe un **patrón** de nodos y relaciones que se debe encontrar o crear.

```cypher
(p:Persona)-[:VIVE_EN]->(c:Ciudad)
```

Un camino puede tener varias relaciones. Para expresar longitudes variables se indica el rango después del tipo de relación:

```cypher
(a)-[:CONOCE*2]->(b)      // exactamente dos relaciones
(a)-[:CONOCE*1..3]->(b)   // de una a tres relaciones
(a)-[:CONOCE*..4]->(b)    // hasta cuatro relaciones
```

Los recorridos de longitud variable deben acotarse siempre que sea posible: un recorrido sin límite puede ser muy costoso en un grafo denso. Se puede asignar el camino a una variable para inspeccionarlo:

```cypher
MATCH camino = (a:Persona {nombre: "Ana"})-[:CONOCE*1..3]->(b)
RETURN camino, length(camino), nodes(camino), relationships(camino)
```

## 4. Creación de datos

`CREATE` inserta el patrón indicado, sin comprobar si ya existe.

```cypher
CREATE (a:Persona {nombre: "Ana", edad: 21})
RETURN a

CREATE (a:Persona {nombre: "Ana"})-[:CONOCE {desde: date("2025-01-01")}]->
       (l:Persona {nombre: "Luis"})
```

Para crear una relación entre nodos existentes, primero se localizan con `MATCH`:

```cypher
MATCH (a:Persona {nombre: "Ana"}), (l:Persona {nombre: "Luis"})
CREATE (a)-[:CONOCE]->(l)
```

`MERGE` garantiza que exista un patrón: si no lo encuentra, lo crea. Es útil para operaciones idempotentes, pero el patrón completo debe estar bien definido para evitar duplicados inesperados.

```cypher
MERGE (p:Persona {email: "ana@correo.com"})
ON CREATE SET p.nombre = "Ana", p.creadoEn = datetime()
ON MATCH SET p.ultimaConsulta = datetime()
RETURN p
```

Para crear una relación sin duplicarla, se recomienda localizar los nodos por una clave única y aplicar `MERGE` solo a la relación:

```cypher
MATCH (a:Persona {email: "ana@correo.com"})
MATCH (l:Persona {email: "luis@correo.com"})
MERGE (a)-[r:CONOCE]->(l)
ON CREATE SET r.desde = date()
RETURN r
```

## 5. Lectura con `MATCH`

`MATCH` busca patrones en el grafo. Las variables que devuelve `RETURN` pueden ser nodos, relaciones, propiedades, expresiones o caminos.

```cypher
MATCH (n)
RETURN n

MATCH (p:Persona)
RETURN p.nombre, p.edad

MATCH (p:Persona)-[r:CONOCE]->(otra:Persona)
RETURN p.nombre, otra.nombre, r.desde
```

`OPTIONAL MATCH` conserva la fila aunque el patrón opcional no exista; las variables de ese patrón toman el valor `null`. Es análogo a un *left join*.

```cypher
MATCH (p:Persona)
OPTIONAL MATCH (p)-[:VIVE_EN]->(c:Ciudad)
RETURN p.nombre, c.nombre
```

### Filtros con `WHERE`

`WHERE` restringe el patrón encontrado. Puede filtrar por propiedades, etiquetas, expresiones, pertenencia a una lista, patrones adicionales y expresiones regulares.

```cypher
MATCH (p:Persona)
WHERE p.edad >= 18 AND p.edad < 30
  AND p.nombre STARTS WITH "A"
RETURN p

MATCH (p)
WHERE p:Persona AND p.email IS NOT NULL
RETURN p.nombre

MATCH (p:Persona)
WHERE p.nombre IN ["Ana", "Luis"]
RETURN p

MATCH (p:Persona)
WHERE p.nombre =~ "(?i)ana.*"
RETURN p
```

También puede usarse un patrón como condición:

```cypher
MATCH (p:Persona)
WHERE (p)-[:VIVE_EN]->(:Ciudad {nombre: "Madrid"})
RETURN p.nombre
```

## 6. Presentación y paginación

`RETURN` define las columnas del resultado. `DISTINCT` elimina filas duplicadas y `AS` asigna un alias.

```cypher
MATCH (p:Persona)-[:CONOCE]->(amiga:Persona)
RETURN DISTINCT amiga.nombre AS nombre
```

`ORDER BY` ordena las filas; `ASC` es el orden ascendente por defecto y `DESC` el descendente. `SKIP` y `LIMIT` implementan paginación.

```cypher
MATCH (p:Persona)
RETURN p.nombre, p.edad
ORDER BY p.edad DESC, p.nombre ASC
SKIP 10
LIMIT 5
```

Para que una paginación sea estable, el orden debe incluir un criterio que resuelva empates, como una propiedad única.

## 7. Agregación y agrupación

Las funciones de agregación reducen varias filas a un valor. Las expresiones que aparecen junto a una agregación en `RETURN` se convierten en claves de agrupación.

```cypher
MATCH (:Persona)-[r]->()
RETURN type(r) AS tipo, count(*) AS total
ORDER BY total DESC
```

| Función | Resultado |
| --- | --- |
| `count(*)` | Número de filas |
| `count(valor)` | Número de valores no nulos |
| `sum(valor)` | Suma de valores numéricos |
| `avg(valor)` | Media |
| `min(valor)` / `max(valor)` | Mínimo o máximo |
| `collect(valor)` | Lista de valores no nulos |

```cypher
MATCH (p:Persona)-[:VIVE_EN]->(c:Ciudad)
RETURN c.nombre AS ciudad,
       count(p) AS habitantes,
       avg(p.edad) AS edadMedia,
       collect(p.nombre) AS personas
```

`collect(DISTINCT expresion)` construye una lista sin repetidos.

## 8. `WITH`, `UNWIND` y `UNION`

`WITH` pasa a la parte siguiente de la consulta solo las variables y expresiones indicadas. También permite filtrar, ordenar o limitar resultados intermedios.

```cypher
MATCH (p:Persona)-[:CONOCE]->(amiga)
WITH p, count(amiga) AS numeroAmistades
WHERE numeroAmistades >= 3
RETURN p.nombre, numeroAmistades
```

`UNWIND` expande una lista en filas. Resulta útil para cargar varios valores o transformar colecciones.

```cypher
UNWIND ["Ana", "Luis", "Marta"] AS nombre
CREATE (:Persona {nombre: nombre})

UNWIND [1, 1, 2, 3] AS n
WITH DISTINCT n
RETURN collect(n) AS numeros
```

`UNION` combina los resultados de dos consultas compatibles y elimina duplicados; `UNION ALL` los conserva. Ambas partes deben devolver el mismo número de columnas con nombres compatibles.

```cypher
MATCH (p:Persona)
RETURN p.nombre AS nombre
UNION
MATCH (a:Animal)
RETURN a.nombre AS nombre
```

## 9. Funciones y predicados

Los predicados sobre listas evalúan una condición para sus elementos:

```cypher
MATCH camino = (:Persona {nombre: "Ana"})-[:CONOCE*1..3]->(:Persona)
WHERE all(n IN nodes(camino) WHERE n.edad >= 18)
RETURN camino
```

| Predicado | Significado |
| --- | --- |
| `all(x IN lista WHERE condicion)` | Todos cumplen la condición |
| `any(x IN lista WHERE condicion)` | Al menos uno la cumple |
| `none(x IN lista WHERE condicion)` | Ninguno la cumple |
| `single(x IN lista WHERE condicion)` | Exactamente uno la cumple |

Funciones frecuentes:

| Función | Uso |
| --- | --- |
| `length(camino)` | Número de relaciones de un camino |
| `size(lista)` | Tamaño de una lista o cadena |
| `type(relacion)` | Tipo de una relación |
| `labels(nodo)` | Etiquetas de un nodo |
| `keys(elemento)` | Nombres de sus propiedades |
| `properties(elemento)` | Mapa de propiedades |
| `startNode(r)` / `endNode(r)` | Nodos de una relación |
| `elementId(elemento)` | Identificador interno textual |
| `coalesce(a, b, ...)` | Primer valor no nulo |
| `range(inicio, fin, paso)` | Lista numérica |

`reduce` acumula un valor al recorrer una lista:

```cypher
WITH [1, 2, 3, 4] AS numeros
RETURN reduce(total = 0, n IN numeros | total + n) AS suma
```

## 10. Actualización

`SET` crea o modifica propiedades y añade etiquetas. Asignar `null` a una propiedad la elimina.

```cypher
MATCH (p:Persona {email: "ana@correo.com"})
SET p.edad = 22,
    p.actualizadoEn = datetime(),
    p:Estudiante
RETURN p

MATCH (p:Persona {email: "ana@correo.com"})
SET p.nombre = null
```

Para añadir o modificar solo algunas propiedades de un mapa se usa `+=`; para reemplazar todas las propiedades se usa `=`.

```cypher
MATCH (p:Persona {email: "ana@correo.com"})
SET p += {ciudad: "Madrid", activo: true}

MATCH (p:Persona {email: "ana@correo.com"})
SET p = {nombre: "Ana", edad: 22}
```

`REMOVE` elimina etiquetas o propiedades de forma explícita:

```cypher
MATCH (p:Persona {email: "ana@correo.com"})
REMOVE p:Estudiante, p.ciudad
```

`FOREACH` ejecuta actualizaciones para cada elemento de una colección, por ejemplo para etiquetar los nodos de un camino:

```cypher
MATCH camino = (:Persona {nombre: "Ana"})-[:CONOCE*1..2]->()
FOREACH (n IN nodes(camino) | SET n:Visitado)
```

## 11. Eliminación

`DELETE` elimina nodos o relaciones. Un nodo con relaciones no puede eliminarse directamente: primero se deben eliminar sus relaciones o usar `DETACH DELETE`.

```cypher
MATCH ()-[r:CONOCE]->()
WHERE r.desde < date("2020-01-01")
DELETE r

MATCH (p:Persona {email: "ana@correo.com"})
DETACH DELETE p
```

`DETACH DELETE` borra el nodo y todas sus relaciones. Por ello el patrón de `MATCH` debe ser lo más específico posible antes de ejecutarlo.

## 12. Índices y restricciones

Los índices aceleran búsquedas por propiedades de nodos o relaciones. No conviene crearlos indiscriminadamente: mejoran lecturas pero añaden coste a las escrituras y consumen espacio.

```cypher
CREATE INDEX persona_email IF NOT EXISTS
FOR (p:Persona) ON (p.email)

CREATE TEXT INDEX persona_nombre IF NOT EXISTS
FOR (p:Persona) ON (p.nombre)

SHOW INDEXES
DROP INDEX persona_email IF EXISTS
```

Los índices de rango son adecuados para igualdad, intervalos y ordenaciones; los de texto sirven para búsquedas textuales y los de punto para propiedades espaciales. Neo4j también puede crear índices vectoriales para búsquedas por similitud sobre *embeddings*.

Las restricciones protegen la calidad del modelo. Una restricción de unicidad evita duplicados y normalmente crea el índice necesario para comprobarla.

```cypher
CREATE CONSTRAINT persona_email_unico IF NOT EXISTS
FOR (p:Persona)
REQUIRE p.email IS UNIQUE

CREATE CONSTRAINT persona_nombre_obligatorio IF NOT EXISTS
FOR (p:Persona)
REQUIRE p.nombre IS NOT NULL

SHOW CONSTRAINTS
DROP CONSTRAINT persona_email_unico IF EXISTS
```

Además de unicidad y existencia, el esquema puede imponer tipos o claves de nodo, según la edición y versión de Neo4j utilizada.

## 13. Rendimiento y diseño

- Modelar las relaciones como relaciones del grafo, no como identificadores repetidos en listas de propiedades.
- Dar a cada relación un tipo concreto y usar direcciones coherentes con la forma habitual de recorrer el grafo.
- Crear restricciones de unicidad para identificadores de negocio, como correo, DNI o código de producto.
- Comenzar los `MATCH` por nodos selectivos e indexados antes de expandir relaciones.
- Limitar la longitud de los caminos variables y evitar patrones demasiado generales, como `MATCH (n)` en grafos grandes.
- Usar `EXPLAIN` para ver el plan previsto y `PROFILE` para medir una consulta con datos reales.

```cypher
PROFILE
MATCH (p:Persona {email: "ana@correo.com"})-[:CONOCE*1..2]->(otra)
RETURN otra.nombre
```
