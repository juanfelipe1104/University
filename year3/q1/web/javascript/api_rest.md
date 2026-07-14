# API REST desde JavaScript

## Recursos y HTTP

Una API REST expone recursos mediante URLs y utiliza HTTP para consultarlos o modificarlos. El cliente inicia cada petición y el servidor devuelve una respuesta con estado, cabeceras y, opcionalmente, cuerpo.

Principios relevantes:

- **cliente-servidor:** interfaz y datos evolucionan de forma independiente;
- **sin estado:** cada petición contiene la información necesaria para procesarse;
- **interfaz uniforme:** recursos y operaciones siguen reglas consistentes;
- **representaciones:** un recurso se transmite normalmente como JSON;
- **caché:** la respuesta indica si puede reutilizarse;
- **sistema por capas:** el cliente no necesita saber si hay proxies o balanceadores intermedios.

Una URL identifica recursos, no acciones:

```text
GET    /usuarios       Lista usuarios
GET    /usuarios/7     Obtiene el usuario 7
POST   /usuarios       Crea un usuario
PUT    /usuarios/7     Sustituye el usuario 7
PATCH  /usuarios/7     Modifica parte del usuario 7
DELETE /usuarios/7     Elimina el usuario 7
```

## JSON

JSON admite objetos, arrays, cadenas, números, booleanos y `null`. Sus claves y cadenas usan comillas dobles y no permite comentarios.

```js
const texto = JSON.stringify({ nombre: "Ana", edad: 25 });
const usuario = JSON.parse(texto);
```

`undefined`, funciones y determinadas estructuras de JavaScript no tienen una representación JSON directa.

## Fetch

`fetch` devuelve una promesa que se resuelve con un objeto `Response`. Solo rechaza normalmente por errores de red o cancelación; una respuesta HTTP `404` o `500` sigue siendo una respuesta resuelta. Por ello hay que comprobar `response.ok`.

```js
async function solicitar(url, opciones = {}) {
  const response = await fetch(url, opciones);

  if (!response.ok) {
    throw new Error(`Error HTTP ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
```

El cuerpo solo puede consumirse una vez mediante `json()`, `text()`, `blob()` u otro lector.

## GET

`GET` es el método predeterminado y no debe modificar el recurso.

```js
const usuarios = await solicitar("http://localhost:3000/users");
const usuario = await solicitar("http://localhost:3000/users/1");
```

Los parámetros de consulta se construyen con `URLSearchParams`:

```js
const parametros = new URLSearchParams({ grupo: "INSG", activo: "true" });
const usuarios = await solicitar(`/users?${parametros}`);
```

## POST

`POST` crea habitualmente un recurso. El servidor decide su identificador y suele responder con `201 Created`.

```js
const nuevoUsuario = await solicitar("http://localhost:3000/users", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Ana García",
    email: "ana@example.com",
    age: 25,
  }),
});
```

## PUT y PATCH

`PUT` sustituye la representación completa del recurso. `PATCH` modifica solo los campos enviados.

```js
await solicitar("http://localhost:3000/users/1", {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "Ana García",
    email: "ana@example.com",
    age: 26,
  }),
});
```

```js
await solicitar("http://localhost:3000/users/1", {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ age: 27 }),
});
```

## DELETE

```js
await solicitar("http://localhost:3000/users/1", {
  method: "DELETE",
});
```

Una eliminación correcta puede responder con `200` y contenido o con `204 No Content`.

## Códigos de estado

| Grupo | Significado | Ejemplos |
|---|---|---|
| `1xx` | Información provisional | `100 Continue` |
| `2xx` | Operación correcta | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | Redirección | `301 Moved Permanently`, `304 Not Modified` |
| `4xx` | Error atribuible a la petición | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `405 Method Not Allowed` |
| `5xx` | Error del servidor | `500 Internal Server Error`, `503 Service Unavailable` |

`401` indica que falta autenticación válida; `403`, que el servidor reconoce al cliente pero no autoriza la operación.

## Estados de interfaz

Una interfaz que consume una API debe representar al menos cuatro estados:

1. carga;
2. datos disponibles;
3. resultado vacío;
4. error con una acción de reintento cuando tenga sentido.

```js
async function cargarUsuarios() {
  mostrarCarga();

  try {
    const usuarios = await solicitar("/users");
    usuarios.length === 0 ? mostrarVacio() : mostrarUsuarios(usuarios);
  } catch (error) {
    mostrarError(error.message);
  }
}
```

## Cancelación

`AbortController` evita conservar una petición que ya no interesa:

```js
const controller = new AbortController();

fetch("/users", { signal: controller.signal });
controller.abort();
```

Es útil en búsquedas mientras se escribe o al abandonar una vista.

## JSON Server

JSON Server permite simular una API durante el desarrollo.

```console
npm install -g json-server
json-server --watch db.json
```

```json
{
  "users": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john.smith@example.com",
      "age": 25
    }
  ]
}
```

El recurso estará disponible normalmente en `http://localhost:3000/users`. El frontend y JSON Server son procesos distintos, aunque ambos se ejecuten en `localhost`.

## Orígenes y CORS

Un origen combina protocolo, host y puerto. `http://localhost:5500` y `http://localhost:3000` son orígenes distintos. El navegador solo permite determinadas peticiones entre orígenes si el servidor responde con las cabeceras CORS apropiadas.

CORS es una protección aplicada por el navegador, no un mecanismo de autenticación. La API debe validar permisos y datos independientemente del origen.

## Buenas prácticas

- Codificar los parámetros de URL en lugar de concatenar texto sin escapar.
- Comprobar `response.ok` antes de procesar el cuerpo.
- Mostrar errores comprensibles sin exponer detalles internos.
- No almacenar secretos de una API privada en JavaScript enviado al navegador.
- Deshabilitar temporalmente acciones para evitar envíos duplicados.
- Tratar reintentos con cuidado: repetir una operación no idempotente puede duplicar recursos.
- Validar siempre en el servidor aunque el formulario ya se haya validado en el cliente.
