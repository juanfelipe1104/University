import Link from "next/link";

export default function Home() {
  return (
    <main className="container hero">
      <p className="eyebrow">Digitalización de albaranes</p>
      <h1>El trabajo de campo, ordenado y disponible.</h1>
      <p className="hero-copy">Administra clientes y proyectos, registra materiales u horas de trabajo y descarga cada albarán en PDF.</p>
      <div className="actions"><Link className="button" href="/registro">Crear cuenta</Link><Link className="button secondary" href="/login">Ya tengo cuenta</Link></div>
      <div className="feature-grid">
        <article className="card"><span>01</span><h2>Clientes</h2><p>Información fiscal y de contacto centralizada.</p></article>
        <article className="card"><span>02</span><h2>Proyectos</h2><p>Trabajos vinculados a cada cliente y su ubicación.</p></article>
        <article className="card"><span>03</span><h2>Albaranes</h2><p>Materiales u horas documentados y listos para descargar.</p></article>
      </div>
    </main>
  );
}
