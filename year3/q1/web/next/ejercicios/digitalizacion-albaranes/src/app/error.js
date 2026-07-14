"use client";

export default function GlobalError({ error, unstable_retry }) {
  return <main className="container hero"><p className="eyebrow">Error inesperado</p><h1>No se pudo mostrar la página.</h1><p className="hero-copy">{error?.message || "Vuelve a intentarlo dentro de unos instantes."}</p><div className="actions"><button className="button" onClick={() => unstable_retry()}>Reintentar</button></div></main>;
}
