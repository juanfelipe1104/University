# MongoDB

## 1. Idea general

MongoDB es una base de datos **NoSQL orientada a documentos**. La información se guarda en colecciones y cada registro es un documento BSON (la representación binaria de JSON).

| Modelo relacional | MongoDB |
| --- | --- |
| Base de datos | Base de datos |
| Tabla | Colección |
| Fila | Documento |
| Columna | Campo |
| Clave primaria | `_id` |
| JOIN | `$lookup` (si es necesario) |

Un documento puede contener objetos y arrays. Esto permite guardar juntos los datos que normalmente se consultan juntos:

```javascript
{
  _id: ObjectId("..."),
  nombre: "Perico",
  contacto: {
    email: "perico@correo.com",
    telefonos: ["123-456-789", "987-654-321"]
  },
  direccion: { calle: "Calle Principal", numero: 2 }
}
```

MongoDB no obliga a que todos los documentos de una colección tengan el mismo esquema. Aun así, conviene diseñar un formato consistente y validar los datos importantes.

## 2. Modelado: embeber o referenciar

La decisión principal de diseño es si un dato se guarda dentro del documento o en otra colección.

- **Embeber**: usar objetos o arrays anidados cuando los datos pertenecen claramente a una entidad, se leen normalmente junto a ella y su tamaño está acotado. Por ejemplo, las direcciones de un usuario.
- **Referenciar**: guardar el `_id` de otro documento cuando la relación se reutiliza mucho, puede crecer sin límite o las dos partes cambian de forma independiente. Por ejemplo, pedidos y productos.

```javascript
// Referencia de un pedido a su cliente
{ _id: 1001, clienteId: ObjectId("..."), fecha: ISODate("2026-01-10") }
```

No hay una regla universal: el modelo debe responder a las consultas más frecuentes. Evitar relaciones innecesarias reduce el uso de `$lookup`, pero un documento no debe crecer sin control. El tamaño máximo de un documento BSON es **16 MiB**.

## 3. Esquema y validación

Una colección puede aceptar documentos distintos, pero se puede imponer una validación con `$jsonSchema`:

```javascript
db.createCollection("alumnos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "grado"],
      properties: {
        nombre: { bsonType: "string" },
        grado: { bsonType: "string" },
        notaMedia: { bsonType: ["double", "int", "decimal"] }
      }
    }
  }
})
```

La validación no reemplaza la validación de la aplicación: protege la base de datos ante inserciones o actualizaciones que no respeten los invariantes básicos.

## 4. CRUD

### Inserción

```javascript
db.alumnos.insertOne({ nombre: "Ana", edad: 21, asignaturas: ["BBDD"] })

db.alumnos.insertMany([
  { nombre: "Luis", edad: 20 },
  { nombre: "Marta", edad: 22 }
])
```

Si no se indica, MongoDB crea el campo `_id` automáticamente. La inserción devuelve el identificador creado.

### Consulta

`find()` devuelve un cursor con todos los documentos que cumplen el filtro; `findOne()` devuelve uno solo o `null`.

```javascript
db.alumnos.find({ edad: { $gte: 21 } })
db.alumnos.findOne({ nombre: "Ana" })

// Campos que se quieren devolver (proyección)
db.alumnos.find({ edad: { $gte: 21 } }, { nombre: 1, edad: 1, _id: 0 })

// Orden, paginación y límite
db.alumnos.find().sort({ edad: -1, nombre: 1 }).skip(10).limit(5)
```

Los campos anidados se consultan con notación de punto: `{ "contacto.email": "ana@correo.com" }`.

### Actualización

```javascript
db.alumnos.updateOne(
  { nombre: "Ana" },
  { $set: { edad: 22 }, $inc: { creditos: 6 } }
)

db.alumnos.updateMany(
  { grado: "Ingeniería" },
  { $set: { activo: true } }
)
```

`replaceOne()` sustituye el documento completo salvo el `_id`; debe usarse solo cuando ese sea el efecto buscado. Con `{ upsert: true }`, una actualización que no encuentra coincidencias inserta un documento nuevo.

```javascript
db.alumnos.updateOne(
  { email: "ana@correo.com" },
  { $set: { nombre: "Ana", activo: true } },
  { upsert: true }
)
```

### Eliminación

```javascript
db.alumnos.deleteOne({ nombre: "Luis" })
db.alumnos.deleteMany({ activo: false })
```

Primero conviene ejecutar el mismo filtro con `find()` para comprobar qué documentos se verán afectados.

## 5. Filtros habituales

| Tipo | Operadores principales |
| --- | --- |
| Comparación | `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin` |
| Lógicos | `$and`, `$or`, `$nor`, `$not` |
| Existencia/tipo | `$exists`, `$type` |
| Evaluación | `$regex`, `$text`, `$mod`, `$expr` |
| Arrays | `$all`, `$elemMatch`, `$size` |

```javascript
// Entre 18 y 25 años
db.alumnos.find({ edad: { $gte: 18, $lt: 25 } })

// Una de varias titulaciones
db.alumnos.find({ grado: { $in: ["Ingeniería", "Matemáticas"] } })

// Condiciones alternativas
db.alumnos.find({ $or: [{ beca: true }, { notaMedia: { $gte: 8 } }] })

// Campo existente
db.alumnos.find({ telefono: { $exists: true } })
```

### Arrays

Una condición simple sobre un array encuentra documentos para los que algún elemento cumple la condición. Cuando varias condiciones deben cumplirse en **el mismo elemento**, se usa `$elemMatch`:

```javascript
db.alumnos.find({ asignaturas: "BBDD" })

db.alumnos.find({
  notas: { $elemMatch: { asignatura: "BBDD", nota: { $gte: 8 } } }
})

db.alumnos.find({ etiquetas: { $all: ["beca", "erasmus"] } })
db.alumnos.find({ asignaturas: { $size: 4 } })
```

Para actualizar arrays son especialmente útiles:

```javascript
db.alumnos.updateOne({ nombre: "Ana" }, { $addToSet: { asignaturas: "BBDD" } })
db.alumnos.updateOne({ nombre: "Ana" }, { $push: { asignaturas: "IA" } })
db.alumnos.updateOne({ nombre: "Ana" }, { $pull: { asignaturas: "IA" } })
```

`$addToSet` evita duplicados; `$push` siempre añade. Con `$each` se insertan varios valores y con `$slice` se puede limitar el tamaño del array.

## 6. Operadores de actualización

| Operador | Efecto |
| --- | --- |
| `$set` / `$unset` | Crea o cambia un campo / lo elimina |
| `$inc`, `$mul` | Incrementa o multiplica un número |
| `$min`, `$max` | Conserva el menor o mayor valor |
| `$rename` | Cambia el nombre de un campo |
| `$currentDate` | Guarda la fecha actual |
| `$setOnInsert` | Solo actúa al insertar mediante `upsert` |
| `$push`, `$addToSet`, `$pop`, `$pull` | Modifican arrays |

El operador posicional `$` actualiza la primera coincidencia de un array; `$[]` actualiza todos sus elementos y `$[identificador]` permite filtrarlos con `arrayFilters`.

```javascript
db.alumnos.updateOne(
  { nombre: "Ana" },
  { $set: { "notas.$[n].revisada": true } },
  { arrayFilters: [{ "n.nota": { $lt: 5 } }] }
)
```

## 7. Índices y rendimiento

Los índices aceleran filtros, ordenaciones y algunas operaciones de agregación, a cambio de ocupar espacio y hacer más costosas las escrituras. Deben crearse a partir de las consultas reales, no de todos los campos posibles.

```javascript
db.alumnos.createIndex({ email: 1 }, { unique: true })
db.alumnos.createIndex({ grado: 1, notaMedia: -1 })
db.alumnos.getIndexes()
db.alumnos.dropIndex("grado_1_notaMedia_-1")
```

Un índice compuesto ayuda cuando el prefijo de sus campos coincide con el filtro o la ordenación. Para comprobar si se usa, se puede ejecutar:

```javascript
db.alumnos.find({ grado: "Ingeniería" }).sort({ notaMedia: -1 }).explain("executionStats")
```

Buenas prácticas:

- Indexar campos usados con frecuencia en filtros, `sort` y claves de relación.
- Evitar índices redundantes y demasiados índices en colecciones que reciben muchas escrituras.
- Colocar `$match` al inicio de un pipeline cuando sea posible.
- Para búsqueda textual, usar índices de texto o las capacidades de búsqueda específicas del despliegue; una expresión regular sin prefijo selectivo puede ser costosa.

## 8. Agregaciones

`aggregate()` procesa documentos en un **pipeline**: cada etapa recibe los documentos de la anterior y produce otros documentos.

```javascript
db.alumnos.aggregate([
  { $match: { grado: "Ingeniería" } },
  { $group: { _id: "$grado", total: { $sum: 1 }, media: { $avg: "$notaMedia" } } },
  { $sort: { media: -1 } }
])
```

Etapas frecuentes:

| Etapa | Función |
| --- | --- |
| `$match` | Filtra documentos |
| `$project` / `$set` | Selecciona, elimina o calcula campos |
| `$group` | Agrupa y aplica acumuladores |
| `$sort`, `$skip`, `$limit` | Ordena y pagina |
| `$unwind` | Convierte cada elemento de un array en un documento |
| `$lookup` | Incorpora datos de otra colección |
| `$count` | Cuenta documentos |
| `$out` / `$merge` | Escribe el resultado en una colección |

### `$group` y acumuladores

En `$group`, `_id` define la clave de agrupación. Puede ser un campo, una expresión o `null` para un único grupo.

```javascript
db.pedidos.aggregate([
  {
    $group: {
      _id: "$clienteId",
      pedidos: { $sum: 1 },
      gastoTotal: { $sum: "$importe" },
      importeMedio: { $avg: "$importe" },
      primero: { $min: "$fecha" },
      productos: { $addToSet: "$productoId" }
    }
  }
])
```

Otros acumuladores comunes son `$min`, `$max`, `$first`, `$last` y `$push`. Antes de usar `$first` o `$last` se debe definir el orden con `$sort`.

### `$project` y expresiones

`$project` remodela el documento. Se incluyen campos con `1`, se excluyen con `0` (sin mezclar ambos salvo `_id`) y se crean campos mediante expresiones.

```javascript
db.alumnos.aggregate([
  {
    $project: {
      _id: 0,
      nombre: 1,
      estado: { $cond: [{ $gte: ["$notaMedia", 5] }, "apto", "no apto"] },
      nombreMayusculas: { $toUpper: "$nombre" }
    }
  }
])
```

Expresiones útiles: aritméticas (`$add`, `$subtract`, `$multiply`, `$divide`), de cadena (`$concat`, `$toLower`, `$toUpper`), arrays (`$size`, `$map`, `$filter`) y condicionales (`$cond`, `$ifNull`, `$switch`).

### `$unwind`

```javascript
db.alumnos.aggregate([
  { $unwind: "$asignaturas" },
  { $group: { _id: "$asignaturas", matriculados: { $sum: 1 } } },
  { $sort: { matriculados: -1 } }
])
```

Después de `$unwind`, un alumno con tres asignaturas genera tres documentos. La opción `preserveNullAndEmptyArrays: true` conserva los que no tienen elementos.

### `$lookup`

`$lookup` es el equivalente aproximado a un *left outer join*. Devuelve las coincidencias en un array, aunque haya como máximo una.

```javascript
db.pedidos.aggregate([
  {
    $lookup: {
      from: "clientes",
      localField: "clienteId",
      foreignField: "_id",
      as: "cliente"
    }
  },
  { $unwind: "$cliente" }
])
```

Debe utilizarse con criterio: si una lectura siempre necesita esos datos y su tamaño es razonable, quizá convenga embeberlos. Cuando se usa `$lookup`, el campo de la colección destino debería estar indexado cuando corresponda.

## 9. Datos geoespaciales

Para coordenadas geográficas se usa GeoJSON, con el orden **longitud, latitud**:

```javascript
db.lugares.insertOne({
  nombre: "Campus",
  ubicacion: { type: "Point", coordinates: [-3.7038, 40.4168] }
})
db.lugares.createIndex({ ubicacion: "2dsphere" })

db.lugares.find({
  ubicacion: {
    $near: {
      $geometry: { type: "Point", coordinates: [-3.7038, 40.4168] },
      $maxDistance: 1000
    }
  }
})
```

`$geoWithin` encuentra puntos dentro de una zona y `$geoIntersects` encuentra geometrías que intersecan con otra. Las distancias de un índice `2dsphere` se expresan en metros.
