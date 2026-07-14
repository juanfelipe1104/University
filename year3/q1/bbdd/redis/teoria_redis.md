# Redis

## 1. Idea general

Redis es una base de datos **clave-valor en memoria**. Cada clave identifica un valor y ese valor puede ser una cadena, una lista, un hash, un conjunto u otra estructura de datos. Al trabajar principalmente en RAM, ofrece tiempos de respuesta muy bajos.

Redis puede utilizarse como base de datos, caché, cola de trabajo o sistema de publicación/suscripción. Aunque sus operaciones individuales son atómicas, no sustituye a una base de datos relacional o documental cuando se necesitan consultas complejas, relaciones ricas o almacenamiento masivo en disco.

```text
clave                         valor
usuario:42:nombre             "Ana"
usuario:42:preferencias       hash
carrito:42                    lista o hash
ranking:curso                 sorted set
```

Las claves y los valores son secuencias de bytes (*binary-safe*). Por legibilidad conviene emplear un esquema estable, normalmente con `:` como separador: `tipo:identificador:atributo`.

## 2. Persistencia, replicación y caché

Aunque Redis trabaja en memoria, la persistencia es opcional y puede configurarse de dos formas:

- **RDB**: genera instantáneas de la base de datos en momentos determinados. Es compacto y rápido para recuperar, pero puede perder las últimas escrituras desde la última instantánea.
- **AOF** (*append-only file*): registra las operaciones de escritura. Ofrece mayor durabilidad según la política de sincronización elegida, a cambio de más uso de disco.

Redis admite réplicas y despliegues en clúster. La replicación permite distribuir lecturas y tolerar la caída de un nodo; un clúster divide las claves entre nodos. La consistencia de la replicación es normalmente asíncrona, por lo que una escritura recién realizada puede no estar aún en una réplica.

Como caché, Redis mantiene los datos más consultados para evitar acceder repetidamente a un sistema más lento. Es habitual usar expiraciones y una política de expulsión cuando se alcanza el límite de memoria:

```redis
CONFIG SET maxmemory 100mb
CONFIG SET maxmemory-policy allkeys-lru
```

Políticas frecuentes:

| Política | Comportamiento |
| --- | --- |
| `noeviction` | Rechaza escrituras que necesiten más memoria |
| `allkeys-lru` | Expulsa claves de cualquier tipo según uso reciente |
| `volatile-lru` | Solo expulsa claves con expiración |
| `allkeys-random` | Expulsa claves aleatorias |
| `volatile-random` | Expulsa claves con expiración al azar |
| `volatile-ttl` | Prioriza las claves con menor tiempo de vida restante |

La caché debe considerarse una copia prescindible: la aplicación tiene que poder reconstruir su contenido desde la fuente real.

## 3. Claves, expiración y operaciones generales

```redis
SET usuario:42:nombre "Ana"
EXISTS usuario:42:nombre
DEL usuario:42:nombre usuario:43:nombre
TYPE usuario:42:nombre
RENAME clave:antigua clave:nueva
```

`DEL` elimina una o varias claves y `EXISTS` devuelve cuántas de las claves indicadas existen. Hay que evitar `KEYS *` en producción porque recorre todas las claves y puede bloquear el servidor; para recorrerlas gradualmente se usa `SCAN`.

### Expiración

Una clave puede desaparecer automáticamente al vencer su tiempo de vida:

```redis
SET sesion:abc "usuario:42" EX 3600
EXPIRE carrito:42 1800
PEXPIRE token:abc 5000
TTL sesion:abc
PERSIST sesion:abc
```

| Comando | Acción |
| --- | --- |
| `EXPIRE clave segundos` / `PEXPIRE` | Establece una expiración relativa |
| `EXPIREAT clave timestamp` / `PEXPIREAT` | Establece el instante de expiración |
| `TTL` / `PTTL` | Consulta el tiempo restante en segundos o milisegundos |
| `PERSIST` | Elimina la expiración |

`TTL` devuelve `-1` si la clave existe pero no expira y `-2` si no existe. En `SET`, las opciones `EX` y `PX` fijan la expiración en la misma operación. `NX` solo escribe si la clave no existe y `XX` solo si ya existe.

```redis
SET bloqueo:recurso "token-unico" NX EX 30
SET usuario:42:nombre "Ana" XX
```

## 4. Cadenas (*strings*)

Una cadena es el tipo básico de Redis. Puede contener texto, números o datos binarios y es adecuada para contadores, flags, tokens y valores simples.

```redis
SET saludo "hola"
GET saludo
MSET idioma es tema redis
MGET idioma tema inexistente
APPEND saludo " mundo"
STRLEN saludo
```

Los incrementos son atómicos, por lo que varios clientes pueden actualizar un contador sin perder cambios:

```redis
SET visitas 0
INCR visitas
INCRBY visitas 10
INCRBYFLOAT saldo 2.5
DECRBY stock 1
```

`GETSET` escribe un valor y devuelve el anterior en una única operación. `MSET` y `MGET` escriben o leen varias claves; `MSETNX` solo escribe si ninguna de las claves indicadas existe.

```redis
GETSET contador 0
MSETNX configuracion:version 1 configuracion:modo produccion
```

## 5. Listas

Una lista conserva el orden de los elementos y permite insertar o extraer eficazmente por ambos extremos. Es útil para colas, pilas, historiales recientes y trabajos pendientes.

```redis
LPUSH tareas "primera" "segunda"
RPUSH tareas "tercera"
LRANGE tareas 0 -1
LPOP tareas
RPOP tareas
LLEN tareas
```

`LPUSH` inserta por la izquierda y `RPUSH` por la derecha; `LPOP` y `RPOP` extraen de esos extremos. En `LRANGE`, el índice `0` es el primer elemento y `-1` el último.

```redis
RPUSH ultimos 1 2 3 4 5
LTRIM ultimos 0 2
LINDEX ultimos 1
LSET ultimos 0 "nuevo"
```

`LTRIM` conserva solo el rango indicado. `LINSERT` inserta antes o después de un valor, `LREM` elimina coincidencias y `LPUSHX` / `RPUSHX` solo insertan si la lista ya existe.

### Listas bloqueantes y colas

`BLPOP` y `BRPOP` esperan a que una lista tenga elementos. Si la lista está vacía, el cliente se bloquea hasta recibir un valor o hasta agotar el tiempo; `0` espera indefinidamente.

```redis
BRPOP cola:trabajos 30
BLPOP cola:alta cola:baja 0
```

Para mover un elemento de una cola a otra de forma atómica se usa `RPOPLPUSH` (o el comando moderno `LMOVE`):

```redis
RPOPLPUSH cola:pendiente cola:procesando
```

Este patrón permite que un trabajador tome un trabajo y lo marque como procesándose. Si falla, se puede recuperar desde la segunda lista.

## 6. Hashes

Un hash almacena pares campo-valor bajo una única clave. Es adecuado para representar objetos pequeños, como un perfil de usuario, sin crear una clave de Redis por atributo.

```redis
HSET usuario:42 nombre "Ana" email "ana@correo.com" edad 21
HGET usuario:42 nombre
HMGET usuario:42 nombre email
HGETALL usuario:42
HKEYS usuario:42
HVALS usuario:42
```

`HSETNX` escribe un campo solo si aún no existe. Los campos numéricos se pueden modificar de forma atómica:

```redis
HSET usuario:42 creditos 6
HINCRBY usuario:42 creditos 3
HINCRBYFLOAT usuario:42 saldo 1.5
HDEL usuario:42 email
HEXISTS usuario:42 nombre
HLEN usuario:42
```

La expiración se asigna a la clave del hash completa, no a campos individuales.

## 7. Conjuntos (*sets*)

Un set es una colección sin orden y sin elementos duplicados. Sirve para etiquetas, permisos, seguidores o para hacer operaciones de teoría de conjuntos.

```redis
SADD usuario:42:roles alumno delegado alumno
SMEMBERS usuario:42:roles
SISMEMBER usuario:42:roles delegado
SREM usuario:42:roles delegado
SCARD usuario:42:roles
```

`SPOP` extrae un elemento aleatorio y `SRANDMEMBER` lo devuelve sin eliminarlo.

```redis
SADD grupo:a ana luis marta
SADD grupo:b luis marta pablo
SINTER grupo:a grupo:b
SUNION grupo:a grupo:b
SDIFF grupo:a grupo:b
```

Las variantes `SINTERSTORE`, `SUNIONSTORE` y `SDIFFSTORE` guardan el resultado en otra clave. `SMOVE origen destino miembro` traslada un elemento entre sets de forma atómica.

## 8. Conjuntos ordenados (*sorted sets*)

Un sorted set asocia un valor numérico (*score*) a cada miembro. Los miembros no se repiten; Redis los mantiene ordenados por score y, si hay empate, por orden lexicográfico. Son adecuados para rankings, prioridades y líneas temporales.

```redis
ZADD ranking 100 ana 85 luis 92 marta
ZRANGE ranking 0 -1 WITHSCORES
ZREVRANGE ranking 0 2 WITHSCORES
ZSCORE ranking ana
ZRANK ranking luis
ZREVRANK ranking luis
```

Para consultar por puntuación:

```redis
ZRANGEBYSCORE ranking 80 100 WITHSCORES
ZREVRANGEBYSCORE ranking +inf 90 LIMIT 0 10
ZCOUNT ranking 80 100
ZINCRBY ranking 5 ana
```

Los límites son inclusivos por defecto. Un límite exclusivo se escribe con `(`, como `(100`; `-inf` y `+inf` representan límites abiertos. Para eliminar:

```redis
ZREM ranking ana
ZREMRANGEBYRANK ranking 0 9
ZREMRANGEBYSCORE ranking -inf 10
ZCARD ranking
```

Cuando todos los miembros tienen el mismo score se puede trabajar por orden lexicográfico con `ZRANGEBYLEX`, `ZLEXCOUNT` y `ZREMRANGEBYLEX`. Las operaciones `ZINTERSTORE` y `ZUNIONSTORE` combinan sorted sets; permiten ponderar scores con `WEIGHTS` y agregarlos con `SUM`, `MIN` o `MAX`.

## 9. Bitmaps

Un bitmap no es un tipo independiente: se guarda como cadena y se manipula a nivel de bit. Permite representar estados booleanos de muchos elementos con poco espacio, por ejemplo, la asistencia diaria de usuarios identificados por número.

```redis
SETBIT asistencia:2026-01-10 42 1
GETBIT asistencia:2026-01-10 42
BITCOUNT asistencia:2026-01-10
BITOP AND activos:dos-dias asistencia:2026-01-10 asistencia:2026-01-11
BITPOS asistencia:2026-01-10 1
```

`SETBIT` devuelve el valor anterior del bit. `BITOP` calcula `AND`, `OR`, `XOR` o `NOT` y almacena el resultado en una clave destino.

## 10. Iteración segura

Los comandos `SCAN`, `SSCAN`, `HSCAN` y `ZSCAN` permiten recorrer colecciones grandes de forma incremental sin bloquear el servidor durante toda la operación.

```redis
SCAN 0 MATCH usuario:* COUNT 100
SSCAN usuario:42:roles 0 COUNT 50
HSCAN usuario:42 0 MATCH e* COUNT 10
ZSCAN ranking 0 COUNT 20
```

Cada llamada devuelve un cursor y los resultados del lote. Se continúa usando el cursor devuelto hasta recibir `0`. `COUNT` es una sugerencia, no una garantía del tamaño del lote; durante una iteración pueden aparecer elementos repetidos o cambios concurrentes.

## 11. Pipelining y transacciones

El *pipelining* envía varios comandos sin esperar la respuesta de cada uno. Reduce viajes de ida y vuelta de red, pero no convierte los comandos en una transacción ni cambia su orden de ejecución.

Las transacciones agrupan comandos con `MULTI` y `EXEC`. Redis los ejecuta seguidos, sin intercalarlos con comandos de otros clientes.

```redis
MULTI
INCR visitas
HINCRBY usuario:42 acciones 1
EXEC
```

Antes de `EXEC`, los comandos quedan en cola. `DISCARD` vacía la cola y cancela la transacción. Redis no incluye un rollback después de `EXEC`: si un comando falla en tiempo de ejecución, los demás comandos de la transacción no se deshacen.

### Bloqueo optimista con `WATCH`

`WATCH` observa una o varias claves. Si otra conexión las modifica antes de `EXEC`, Redis aborta la transacción y devuelve un resultado nulo. La aplicación debe volver a leer y reintentar.

```redis
WATCH stock:producto:10
GET stock:producto:10
MULTI
DECR stock:producto:10
EXEC
```

Este patrón implementa *compare-and-swap*. Para incrementar o decrementar un contador no hace falta `WATCH`, porque `INCR` y `DECR` ya son atómicos.

## 12. Publicación y suscripción

En Pub/Sub, un publicador envía mensajes a un canal y los clientes suscritos los reciben inmediatamente:

```redis
SUBSCRIBE chat:sala-1
PSUBSCRIBE chat:*
PUBLISH chat:sala-1 "Hola"
UNSUBSCRIBE chat:sala-1
PUNSUBSCRIBE chat:*
```

Pub/Sub no conserva los mensajes: un suscriptor desconectado no recibe lo que se publique durante su ausencia. Por ello es útil para notificaciones en tiempo real, chats o eventos efímeros; para colas durables o consumidores que deben recuperar mensajes se emplean estructuras persistentes, como listas o streams.

## 13. Criterios de diseño

- Usar nombres de clave consistentes y con un prefijo que identifique el tipo de dato.
- Elegir la estructura de Redis que expresa la operación necesaria: hash para atributos, set para pertenencia, sorted set para orden por puntuación y lista para extremos/colas.
- Establecer TTL en sesiones, tokens, cachés y datos temporales; una expiración evita crecimiento indefinido.
- Evitar comandos que recorran toda la base, especialmente `KEYS`, en entornos con carga.
- Controlar la memoria con `INFO memory`, expiraciones y una política de expulsión acorde al caso de uso.
- Diseñar la aplicación para asumir que una caché puede perderse y que una réplica puede ir con retraso respecto al nodo principal.
