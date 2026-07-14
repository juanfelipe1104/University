# Aplicaciones móviles

Proyecto Android desarrollado durante las clases. Reúne navegación con fragments, autenticación con Firebase y un catálogo remoto con carrito.

## Documentación

- [Android, Kotlin, Dart y Flutter](docs/apuntes.md)

## Proyectos relacionados

- [Calculadora](https://github.com/juanfelipe1104/calculadora): calculadora multiplataforma desarrollada con Flutter.

- [Movie Shelf](https://github.com/juanfelipe1104/movie_shelf): gestor de películas para Android desarrollado con Kotlin.

## Ejecución

Requisitos:

- Android Studio compatible con Android Gradle Plugin 9.2.1.
- JDK 17 o superior.
- Android SDK 36.
- Un dispositivo o emulador con Android 7.0 (API 24) o superior.

El proyecto incluye la configuración de Firebase usada durante las clases. La autenticación y la base de datos requieren conexión y que el proyecto remoto siga disponible. El catálogo consulta la API pública de DummyJSON.

Desde Android Studio, sincroniza Gradle y ejecuta la configuración `app`. Desde terminal:

```bash
./gradlew test
./gradlew lint
./gradlew assembleDebug
```

## Funcionalidad

- Registro e inicio de sesión mediante Firebase Auth.
- Almacenamiento del perfil básico en Firebase Realtime Database.
- Navegación entre pantallas mediante fragments y Navigation Component.
- Catálogo remoto, filtro por categoría y detalle de producto.
- Lista o cuadrícula en función de la orientación del dispositivo.
- Carrito en memoria con recuento, total y finalización de compra.
- Estados de carga y mensajes de error para las operaciones remotas.
