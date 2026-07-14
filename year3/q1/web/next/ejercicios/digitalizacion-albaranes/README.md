# Digitalización de albaranes

Aplicación Next.js que consume la API de [BildyApp](https://github.com/juanfelipe1104/bildy_app) para gestionar clientes, proyectos y albaranes.

## Requisitos

- Node.js 20.9 o posterior.
- BildyApp ejecutándose en `http://localhost:3000`.

## Puesta en marcha

```console
npm install
cp .env.example .env
npm run dev
```

La interfaz se abre en `http://localhost:3001`. El Route Handler `/api/bildy/[...path]` reenvía las peticiones a BildyApp para evitar llamadas entre orígenes diferentes.

La dirección del backend puede cambiarse en `.env`:

```env
BILDY_API_URL=http://localhost:3000
```

## Funcionalidad

- registro, validación, inicio y cierre de sesión;
- renovación automática del token de acceso;
- configuración del perfil y de la empresa;
- alta, listado, filtrado, detalle y edición de clientes;
- alta, listado, filtrado, detalle y edición de proyectos;
- creación y consulta de albaranes de material u horas;
- descarga del albarán en PDF.

## Comprobaciones

```console
npm run lint
npm run build
```
