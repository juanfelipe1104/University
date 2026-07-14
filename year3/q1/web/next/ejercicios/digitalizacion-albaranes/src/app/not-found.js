import Link from "next/link";

export default function NotFound() {
  return <main className="container hero"><p className="eyebrow">Error 404</p><h1>Esta página no existe.</h1><p className="hero-copy">La dirección puede ser incorrecta o el contenido ya no estar disponible.</p><div className="actions"><Link className="button" href="/">Volver al inicio</Link></div></main>;
}
