# Búsqueda y Análisis de la Información

Material de teoría, ejemplos y ejercicios de la asignatura Búsqueda y Análisis de la Información (BAIN).

## Contenidos

| Bloque | Contenido |
| --- | --- |
| [`01_fundamentos_python_pandas`](01_fundamentos_python_pandas/) | Sintaxis de Python, formatos de datos y análisis con Pandas. |
| [`02_codificacion_regex_tokenizacion`](02_codificacion_regex_tokenizacion/) | Codificación de caracteres, expresiones regulares, tokenización y normalización. |
| [`03_web_scraping_apis`](03_web_scraping_apis/) | Consumo de APIs, HTML, Beautiful Soup y Selenium. |
| [`04_procesamiento_lenguaje_natural`](04_procesamiento_lenguaje_natural/) | Análisis de sentimiento, resumen extractivo y modelado de tópicos con LDA. |
| [`05_analisis_grafos`](05_analisis_grafos/) | Representación de redes, centralidad, PageRank y detección de comunidades. |
| [`06_modelos_lenguaje`](06_modelos_lenguaje/) | Transformers, modelos de lenguaje y diseño de prompts. |
| [`practicas`](practicas/) | Entregas y materiales asociados a las prácticas de la asignatura. |

## Entorno

El proyecto utiliza Python 3.12 y [`uv`](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias.

```bash
uv sync
uv run jupyter lab
```

Los notebooks deben ejecutarse desde el directorio que los contiene cuando acceden a datasets mediante rutas relativas.

Algunos ejemplos necesitan recursos externos:

- los ejercicios de NLTK descargan corpus y modelos la primera vez;
- Selenium requiere un navegador compatible;
- los ejemplos de APIs y modelos de lenguaje necesitan conexión y, cuando corresponda, credenciales propias;
- los modelos de Hugging Face pueden requerir varios gigabytes de memoria y almacenamiento.

Las credenciales no deben escribirse directamente en los notebooks ni incorporarse al repositorio.
