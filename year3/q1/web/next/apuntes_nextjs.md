# Next.js con App Router

## Qué aporta Next.js

Next.js es un framework basado en React. Añade una estructura de aplicación y capacidades que React no define por sí solo:

- enrutamiento basado en el sistema de archivos;
- renderizado en servidor y generación estática;
- Server Components y Client Components;
- carga de datos, caché y revalidación;
- optimización de imágenes y fuentes;
- metadatos;
- Route Handlers para endpoints HTTP;
- compilación y optimización de producción.

## Creación de un proyecto

```console
npx create-next-app@latest mi-aplicacion
cd mi-aplicacion
npm run dev
```

Next.js requiere Node.js. El asistente permite elegir JavaScript o TypeScript, ESLint, Tailwind, directorio `src`, App Router y alias de importación.

Comandos habituales:

| Comando | Función |
|---|---|
| `npm run dev` | Servidor de desarrollo |
| `npm run build` | Compilación optimizada |
| `npm start` | Ejecuta la compilación de producción |
| `npm run lint` | Ejecuta el analizador configurado |

## Estructura principal

```text
src/
├── app/
│   ├── layout.js
│   ├── page.js
│   ├── globals.css
│   └── clientes/
│       └── page.js
├── components/
└── lib/
public/
next.config.mjs
package.json
```

- `app/` define rutas, layouts y archivos especiales.
- `components/` contiene piezas reutilizables de interfaz.
- `lib/` agrupa acceso a datos, utilidades y lógica compartida.
- `public/` sirve archivos estáticos desde la raíz del sitio.

## Rutas basadas en directorios

Cada directorio dentro de `app` representa un segmento de URL cuando contiene un `page.js`:

```text
app/page.js                       /
app/about/page.js                 /about
app/contact/book/page.js          /contact/book
app/clientes/[id]/page.js         /clientes/:id
```

Un archivo que no utiliza una convención reservada puede colocarse junto a una ruta sin convertirse en una URL pública.

### Páginas

```jsx
export default function AboutPage() {
  return <h1>Sobre la aplicación</h1>;
}
```

### Segmentos dinámicos

Los corchetes declaran un parámetro. En las versiones actuales, `params` se recibe como promesa en una página de servidor:

```jsx
export default async function ClientPage({ params }) {
  const { id } = await params;
  return <h1>Cliente {id}</h1>;
}
```

En un Client Component puede usarse `useParams` de `next/navigation`.

## Layouts

Un layout envuelve las páginas de su segmento y conserva su estado durante la navegación.

```jsx
import "./globals.css";

export const metadata = {
  title: "Bildy App",
  description: "Gestión digital de albaranes",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <nav>Navegación</nav>
        {children}
      </body>
    </html>
  );
}
```

Solo existe un layout raíz, pero cada segmento puede definir otro `layout.js`. Esto permite crear una navegación o panel lateral específico para una sección.

## Navegación

### Link

`Link` realiza navegación cliente sin recargar todo el documento:

```jsx
import Link from "next/link";

<Link href="/clientes">Clientes</Link>;
```

Next puede precargar rutas visibles para acelerar la transición.

### useRouter

Cuando se necesita ejecutar lógica antes de navegar se usa `useRouter` en un Client Component:

```jsx
"use client";

import { useRouter } from "next/navigation";

export default function SaveButton() {
  const router = useRouter();

  async function save() {
    await saveData();
    router.push("/clientes");
  }

  return <button onClick={save}>Guardar</button>;
}
```

Otras operaciones son `replace`, `back`, `forward` y `refresh`.

## Metadatos y SEO

Los Server Components pueden exportar metadatos estáticos:

```jsx
export const metadata = {
  title: "Clientes | Bildy",
  description: "Consulta y administra clientes",
};
```

Para valores que dependen de parámetros se utiliza `generateMetadata`. Next genera las etiquetas correspondientes del `<head>`.

## Fuentes

`next/font` descarga y optimiza las fuentes durante la construcción, evita peticiones externas desde el navegador y reduce cambios de diseño.

```jsx
import { Roboto } from "next/font/google";

const roboto = Roboto({
  subsets: ["latin"],
  weight: ["300", "400", "500", "700"],
  style: ["normal", "italic"],
});

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body className={roboto.className}>{children}</body>
    </html>
  );
}
```

## Página 404

`app/not-found.js` personaliza el contenido de una ruta inexistente:

```jsx
import Link from "next/link";

export default function NotFound() {
  return (
    <main>
      <h1>404</h1>
      <p>Página no encontrada</p>
      <Link href="/">Volver al inicio</Link>
    </main>
  );
}
```

Desde un Server Component se puede invocar `notFound()` cuando un recurso solicitado no existe.

## Server Components y Client Components

Con App Router, los componentes son **Server Components** por defecto.

### Server Components

- se ejecutan en el servidor;
- pueden obtener datos y acceder a recursos del servidor;
- no incluyen su código en el bundle JavaScript del cliente;
- no usan estado, efectos, eventos ni APIs del navegador;
- pueden renderizar Client Components y pasarles props serializables.

### Client Components

Necesitan la directiva al principio del archivo:

```jsx
"use client";
```

Se utilizan cuando hacen falta:

- `useState`, `useEffect`, `useContext` u otros hooks de cliente;
- eventos como `onClick` y `onChange`;
- APIs como `window`, `localStorage` o geolocalización;
- bibliotecas dependientes del navegador.

La directiva crea una frontera: los módulos importados por ese archivo pasan a formar parte del grafo cliente. Conviene situarla lo más abajo posible y mantener en el servidor todo lo que no requiera interactividad.

## Obtención de datos en el servidor

Un Server Component puede ser asíncrono:

```jsx
async function getPosts() {
  const response = await fetch("https://api.example.com/posts");

  if (!response.ok) {
    throw new Error("No se pudieron cargar las publicaciones");
  }

  return response.json();
}

export default async function PostsPage() {
  const posts = await getPosts();

  return posts.map((post) => <article key={post.id}>{post.title}</article>);
}
```

La política de caché debe elegirse según la naturaleza de los datos:

```js
// Datos siempre actualizados
fetch(url, { cache: "no-store" });

// Revalidación periódica
fetch(url, { next: { revalidate: 3600 } });
```

Los detalles exactos de caché dependen de la versión y configuración de Next. Es preferible declarar la intención en vez de depender de un valor predeterminado.

## Carga, streaming y Suspense

`loading.js` define la interfaz temporal de un segmento mientras se prepara su contenido:

```jsx
export default function Loading() {
  return <p>Cargando…</p>;
}
```

`Suspense` permite mostrar partes de una página a medida que terminan:

```jsx
import { Suspense } from "react";

export default function Page() {
  return (
    <>
      <Post />
      <Suspense fallback={<p>Cargando publicaciones relacionadas…</p>}>
        <RelatedPosts />
      </Suspense>
    </>
  );
}
```

Esto evita que un bloque lento retrase toda la respuesta.

## Manejo de errores

`error.js` captura errores de renderizado de un segmento y debe ser Client Component:

```jsx
"use client";

export default function ErrorPage({ error, unstable_retry }) {
  return (
    <section>
      <h2>No se pudo cargar la sección</h2>
      <p>{error.message}</p>
      <button onClick={unstable_retry}>Reintentar</button>
    </section>
  );
}
```

## Route Handlers

Un archivo `route.js` crea un endpoint HTTP dentro de `app`:

```js
export async function GET() {
  return Response.json({ status: "ok" });
}

export async function POST(request) {
  const body = await request.json();
  return Response.json(body, { status: 201 });
}
```

No puede existir `page.js` y `route.js` en el mismo segmento. Los Route Handlers son útiles como backend propio o capa BFF (*Backend for Frontend*) que adapta una API externa, evita problemas de CORS y oculta direcciones o credenciales solo conocidas por el servidor.

## Estilos

### CSS global

`globals.css` se importa desde el layout raíz y contiene normalización, variables y estilos comunes.

### CSS Modules

Un archivo `Component.module.css` limita los nombres de clase al componente:

```css
.card {
  border-radius: 1rem;
  padding: 1rem;
  background: white;
}
```

```jsx
import styles from "./Card.module.css";

export default function Card({ children }) {
  return <article className={styles.card}>{children}</article>;
}
```

### Tailwind

Tailwind ofrece clases de utilidad y puede configurarse al crear el proyecto. No es obligatorio: CSS global y CSS Modules siguen siendo opciones nativas y adecuadas.

## Autenticación y protección de rutas

Una comprobación de navegación en `proxy.js` no debe ser la única defensa. La autorización debe aplicarse también cerca del acceso a datos y en la API que posee los recursos.

```js
import { cache } from "react";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const verifySession = cache(async () => {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
  return token ? { token } : null;
});

export const getSessionOrRedirect = cache(async () => {
  const session = await verifySession();
  if (!session) redirect("/login");
  return session;
});
```

El backend debe validar el token y comprobar que el usuario puede acceder a cada recurso. Una redirección del frontend solo mejora la experiencia, no constituye seguridad.

## Variables de entorno

```env
API_URL=http://localhost:3000
NEXT_PUBLIC_MAP_URL=https://example.com
```

Las variables sin `NEXT_PUBLIC_` permanecen en el servidor. Las que llevan ese prefijo se incorporan al código del navegador durante la compilación y no deben contener secretos.

## Despliegue

Antes de desplegar:

```console
npm run lint
npm run build
npm start
```

El proyecto puede publicarse en Vercel o en cualquier plataforma compatible con el runtime utilizado. Las variables de entorno, la conectividad con el backend y el almacenamiento persistente deben configurarse en el destino.
