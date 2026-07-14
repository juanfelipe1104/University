const API_URL = (process.env.BILDY_API_URL || "http://localhost:3000").replace(/\/$/, "");

async function proxy(request, { params }) {
  const { path } = await params;
  const incomingUrl = new URL(request.url);
  const target = new URL(`${API_URL}/api/${path.map(encodeURIComponent).join("/")}`);
  target.search = incomingUrl.search;
  const headers = new Headers();
  for (const name of ["authorization", "content-type", "accept"]) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }
  try {
    const hasBody = !["GET", "HEAD"].includes(request.method);
    const upstream = await fetch(target, {
      method: request.method, headers,
      body: hasBody ? await request.arrayBuffer() : undefined,
      cache: "no-store", redirect: "follow",
    });
    const responseHeaders = new Headers();
    for (const name of ["content-type", "content-disposition", "content-length"]) {
      const value = upstream.headers.get(name);
      if (value) responseHeaders.set(name, value);
    }
    return new Response(upstream.body, { status: upstream.status, headers: responseHeaders });
  } catch {
    return Response.json({ error: true, message: "No se puede conectar con BildyApp en localhost:3000" }, { status: 502 });
  }
}

export const dynamic = "force-dynamic";
export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
