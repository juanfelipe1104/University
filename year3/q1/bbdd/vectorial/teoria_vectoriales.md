# Bases de datos vectoriales

## 1. Idea general

Una base de datos vectorial almacena y consulta **embeddings**: vectores numéricos que representan el significado o las características de un objeto. Puede indexar texto, imágenes, audio, código u otros contenidos siempre que un modelo los transforme en vectores de dimensión fija.

La búsqueda no se basa principalmente en coincidencias literales, sino en cercanía en un espacio vectorial. Una consulta se convierte en embedding y se recuperan los vectores más próximos según una métrica elegida.

```text
documento ──> modelo de embeddings ──> vector + metadatos ──> índice vectorial
consulta   ──> mismo modelo             ──> vector ──────────> vecinos más cercanos
```

Dos objetos semánticamente parecidos deberían producir vectores cercanos. Por ejemplo, «cómo crear una rama en Git» y «crear un branch nuevo» pueden estar próximos aunque no compartan las mismas palabras.

## 2. Embeddings

Un embedding es un vector denso de números reales:

```text
[0.12, -0.41, 0.08, ..., 0.33]
```

La dimensión depende del modelo: son habituales 384, 768, 1 024 o 1 536 componentes, entre otras. La dimensión es fija para un modelo concreto y todos los vectores de una colección deben tener la misma longitud.

Características importantes:

- **Denso**: casi todos sus componentes tienen valor; no representa directamente las palabras o atributos originales.
- **Semántico**: codifica relaciones aprendidas por el modelo, no reglas definidas manualmente.
- **Dependiente del modelo**: embeddings de modelos distintos no son comparables entre sí aunque tengan la misma dimensión.
- **Dependiente del pipeline**: idioma, limpieza, formato de entrada, instrucciones y normalización afectan al resultado.

Para crear una colección coherente se debe usar el mismo modelo, versión, preprocesado y métrica para los documentos y para las consultas.

## 3. Normalización

Normalizar un vector L2 consiste en dividirlo por su norma euclídea:

$$
\hat{x} = \frac{x}{\lVert x \rVert_2}
$$

Tras la normalización, todos los vectores tienen norma 1. Así se elimina el efecto de su magnitud y se compara principalmente su dirección. Es habitual normalizar cuando se usa similitud del coseno o producto interno, siempre que el modelo y el motor de búsqueda lo esperen.

La normalización debe aplicarse de forma consistente. Mezclar vectores normalizados y sin normalizar en un mismo índice produce rankings difíciles de interpretar.

## 4. Métricas de similitud y distancia

La métrica define qué significa que dos vectores estén cerca. Debe elegirse según el modelo de embeddings y mantenerse igual al crear y consultar el índice.

### Similitud del coseno

Mide el coseno del ángulo entre dos vectores:

$$
\operatorname{coseno}(x, y) = \frac{x \cdot y}{\lVert x \rVert_2\lVert y \rVert_2}
$$

Un valor alto indica direcciones parecidas. Es muy común para embeddings de texto porque da importancia a la orientación semántica y no a la magnitud.

### Producto interno

El producto interno es:

$$
x \cdot y = \sum_{i=1}^{d} x_i y_i
$$

Es apropiado si el modelo se entrenó para que los pares relevantes tengan un producto interno alto. Con vectores normalizados, ordenar por producto interno y por coseno produce el mismo ranking.

### Distancia euclídea (L2)

Mide la distancia geométrica:

$$
d_2(x, y) = \sqrt{\sum_{i=1}^{d}(x_i-y_i)^2}
$$

En L2, un valor pequeño indica mayor similitud. Puede utilizarse con embeddings de imagen, audio u otros modelos cuya magnitud y distancia estén definidas para esa métrica.

| Métrica | Mejor resultado | Uso frecuente |
| --- | --- | --- |
| Coseno | Valor más alto | Texto con embeddings normalizados |
| Producto interno | Valor más alto | Modelos entrenados para maximizarlo |
| L2 | Valor más bajo | Modelos que usan distancia geométrica |

No se debe asumir que L2, coseno y producto interno son intercambiables. La documentación del modelo debe indicar la métrica recomendada.

## 5. Generación de embeddings

Los embeddings se generan con modelos alojados mediante API o con modelos ejecutados localmente, por ejemplo familias de *sentence transformers*.

| Enfoque | Ventajas | Inconvenientes |
| --- | --- | --- |
| API gestionada | Integración rápida, calidad y escalado administrados | Coste por uso, dependencia externa y requisitos de privacidad |
| Modelo local | Control de datos, coste predecible y posible ajuste al dominio | Hardware, despliegue, actualización y mantenimiento propios |

El texto que se entrega al modelo debe representar una unidad con significado. Antes de generar embeddings conviene limpiar formatos irrelevantes, conservar información útil como títulos y elegir una política de fragmentación estable.

Cada vector debería conservar trazabilidad mínima: modelo, versión, fecha de generación, configuración de normalización, estrategia de *chunking* y referencia al contenido original.

## 6. Fragmentación de documentos (*chunking*)

Un documento largo normalmente se divide en fragmentos antes de indexarse. Cada fragmento se convierte en un vector y recibe un identificador propio.

```text
documento: guia_git.md
├── chunk 0: introducción y configuración
├── chunk 1: crear y cambiar ramas
└── chunk 2: fusionar ramas
```

El tamaño del fragmento es un compromiso:

- Fragmentos muy grandes mezclan temas distintos y reducen la precisión de la recuperación.
- Fragmentos muy pequeños pierden contexto y pueden no contener una respuesta útil completa.
- Un solapamiento entre fragmentos evita perder una idea que queda en el límite, pero aumenta almacenamiento y resultados redundantes.

No existe un tamaño universal. Para texto suelen probarse fragmentos de unas pocas centenas de palabras o un número equivalente de tokens, respetando secciones, párrafos y encabezados cuando sea posible. Los parámetros deben evaluarse con consultas reales.

## 7. Modelo de datos

Un registro vectorial suele incluir cinco piezas:

```json
{
  "id": "guia_git:chunk:12",
  "embedding": [0.12, -0.41, 0.08],
  "document": "Para crear una rama se utiliza git branch...",
  "metadata": {
    "origen": "guia_git.md",
    "indice_chunk": 12,
    "idioma": "es",
    "tema": "git",
    "fecha": "2026-01-10",
    "modelo": "modelo-v1"
  },
  "uri": "docs/guia_git.md"
}
```

| Campo | Función |
| --- | --- |
| Identificador estable | Actualizar, eliminar y deduplicar el vector |
| Embedding | Permitir la búsqueda semántica |
| Documento o payload | Mostrar el fragmento y usarlo como contexto |
| Metadatos | Filtrar, segmentar y aplicar reglas de acceso |
| Referencia al origen | Recuperar el documento completo o citarlo |

Una colección puede contener varios vectores por objeto, por ejemplo uno para título y otro para cuerpo. En ese caso deben nombrarse, versionarse y consultarse explícitamente para evitar combinar espacios semánticos incompatibles.

## 8. Metadatos y filtros

El vector rara vez basta por sí solo. Los metadatos permiten limitar la búsqueda a contenidos que cumplan condiciones estructuradas:

```text
consulta semántica: «configurar servidores»
filtros: idioma = "es" AND tema = "infraestructura" AND año >= 2025
```

Los filtros más útiles son los que se usan con frecuencia y reducen de verdad el conjunto de candidatos: idioma, categoría, estado, permisos, cliente, rango temporal o tipo de documento.

Un identificador único por documento normalmente no sirve como filtro de descubrimiento, porque su selectividad es extrema y solo recuperaría un elemento conocido de antemano.

El motor puede aplicar el filtro **antes** de la búsqueda vectorial (*pre-filter*) o después (*post-filter*). El pre-filtrado reduce el trabajo, pero debe estar indexado y ser compatible con la estructura de búsqueda. El post-filtrado puede devolver menos de `k` resultados útiles si se descartan muchos candidatos después de recuperarlos.

Los filtros también son fundamentales para seguridad: una consulta debe restringirse por permisos o inquilino antes de que el contenido pueda llegar al usuario o a un modelo generativo.

## 9. Búsqueda exacta y aproximada

Una consulta pide normalmente los `k` vecinos más cercanos (*top-k*).

### Búsqueda exacta (FLAT)

La búsqueda FLAT compara el vector de consulta con todos los vectores candidatos y ordena el resultado. Garantiza el top-k exacto para la métrica elegida.

Su coste crece aproximadamente con el número de vectores y con la dimensionalidad. Es adecuada para colecciones pequeñas o medianas, para filtros muy selectivos, para validar resultados y para reordenar un conjunto reducido de candidatos.

### Búsqueda aproximada (ANN)

La búsqueda de vecinos aproximados (*Approximate Nearest Neighbors*) explora solo una parte prometedora del espacio vectorial. Reduce latencia y coste a cambio de que alguno de los vecinos verdaderos puede no aparecer entre los resultados.

| FLAT | ANN |
| --- | --- |
| Top-k exacto | Top-k aproximado |
| Coste lineal sobre candidatos | Menor latencia a gran escala |
| Sin índice complejo | Requiere construir y mantener un índice |
| Útil como referencia | Útil con millones de vectores y alto QPS |

El objetivo de ANN no es ser perfecto, sino alcanzar un *recall* suficiente dentro de una latencia y coste aceptables.

## 10. Índices ANN

Los índices ANN establecen el compromiso entre memoria, tiempo de construcción, velocidad y calidad.

### HNSW

HNSW (*Hierarchical Navigable Small Worlds*) organiza vectores en un grafo navegable de varias capas. La búsqueda empieza en capas superiores poco densas y desciende hacia vecinos cada vez más cercanos.

- Ofrece muy buen recall y baja latencia en muchos casos.
- Consume memoria porque guarda enlaces entre vectores.
- Los parámetros de construcción y búsqueda controlan el equilibrio entre coste y recall.

### IVF

IVF (*Inverted File Index*) agrupa vectores alrededor de centroides. En consulta compara primero con los centroides y explora solo las listas más prometedoras.

- Reduce comparaciones al no recorrer todo el índice.
- Requiere elegir cuántas listas crear y cuántas explorar por consulta.
- Puede combinarse con compresión para reducir memoria.

### Compresión

Técnicas como *product quantization* representan vectores de manera más compacta. Reducen memoria y pueden acelerar búsquedas, pero introducen una aproximación adicional. Es común recuperar candidatos comprimidos y reordenarlos mediante la distancia exacta sobre los vectores originales.

## 11. Recuperación híbrida y re-ranking

La búsqueda vectorial destaca al encontrar significado parecido, pero puede fallar con identificadores, nombres exactos, siglas, números o términos muy específicos. La recuperación híbrida combina una señal semántica con una señal léxica, como BM25 o coincidencia de palabras.

```text
consulta
 ├── búsqueda vectorial ──> candidatos semánticos
 ├── búsqueda léxica    ──> candidatos con términos exactos
 └── fusión y re-ranking ─> resultados finales
```

El **re-ranking** toma un número mayor de candidatos iniciales y aplica un modelo más preciso, normalmente más lento, para ordenarlos. Una arquitectura habitual es:

1. Recuperar `k'` candidatos rápidamente con ANN y filtros.
2. Reordenar los mejores candidatos con distancia exacta, un modelo *cross-encoder* u otra señal de negocio.
3. Devolver los `k` resultados finales.

El valor de `k'` debe ser superior al número de resultados finales, pero no tan alto que el re-ranking anule la mejora de latencia.

## 12. Uso en RAG

RAG (*Retrieval-Augmented Generation*) combina recuperación de información y generación. Antes de responder, el sistema busca fragmentos relevantes y los introduce como contexto para el modelo generativo.

```text
documentos → chunking → embeddings → base vectorial

pregunta → embedding → recuperación + filtros → pasajes → modelo generativo → respuesta
```

La base vectorial no garantiza que la respuesta sea correcta. Una recuperación pobre, fragmentos inadecuados o un contexto demasiado largo pueden llevar al modelo a responder con información incompleta o inventada. Conviene incluir la referencia al origen en cada resultado y pedir al generador que se limite al contexto recuperado cuando el caso lo requiera.

## 13. Evaluación

La evaluación debe separar dos aspectos: la calidad del espacio de embeddings y el comportamiento del sistema en una tarea real.

### Evaluación intrínseca

Analiza la estructura del espacio vectorial sin depender directamente de una aplicación concreta. Por ejemplo, se puede observar si elementos de la misma clase forman grupos o medir la separación con métricas como *Silhouette Score*.

Es útil para diagnóstico, pero no demuestra por sí sola que un buscador o un sistema RAG vaya a ser útil para los usuarios.

### Evaluación extrínseca

Mide la recuperación sobre un conjunto de consultas con resultados relevantes etiquetados (*ground truth*).

| Métrica | Definición | Interpretación |
| --- | --- | --- |
| Recall@k | relevantes recuperados en top-k / relevantes totales | Capacidad de no perder resultados útiles |
| Precision@k | relevantes en top-k / k | Pureza de los primeros resultados |
| Hit Rate@k | consultas con al menos un relevante en top-k / consultas | Probabilidad de dar algún resultado útil |
| MRR | media de 1 / posición del primer relevante | Premia que el primer relevante aparezca pronto |
| nDCG@k | DCG normalizado por el ideal | Considera posición y distintos grados de relevancia |

Para evaluar un índice ANN se puede calcular el top-k exacto con FLAT y usarlo como referencia. El recall del índice mide qué proporción de esos vecinos exactos recupera ANN, mientras que la latencia se mide con percentiles, especialmente P50, P95 y P99.

## 14. Proceso de trabajo

1. Definir los casos de consulta y qué resultado se considerará relevante.
2. Elegir un modelo de embeddings apropiado para idioma, dominio y tipo de contenido.
3. Diseñar el chunking y los metadatos antes de indexar grandes volúmenes.
4. Generar embeddings consistentes y guardar su versión junto al contenido.
5. Elegir métrica e índice; empezar con FLAT si el volumen lo permite para crear una referencia.
6. Añadir filtros de metadatos y controles de permiso que reduzcan el espacio de búsqueda.
7. Evaluar recall, precisión y latencia con un conjunto versionado de consultas reales.
8. Ajustar modelo, fragmentación, `k`, parámetros ANN y re-ranking; reevaluar después de cada cambio.

Cambiar el modelo, la dimensión, la normalización o el preprocesado exige regenerar los embeddings de la colección. Mezclar versiones convierte la distancia entre vectores en una señal no fiable.
