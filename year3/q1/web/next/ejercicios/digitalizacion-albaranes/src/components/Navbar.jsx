"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "./AuthProvider";
import { apiFetch } from "@/lib/api";

export default function Navbar() {
  const { user, loading, endSession } = useAuth();
  const router = useRouter();

  async function logout() {
    try { await apiFetch("/user/logout", { method: "POST" }); } catch { /* Se limpia la sesión local igualmente. */ }
    endSession();
    router.push("/login");
  }

  return (
    <header className="site-header">
      <nav className="navbar" aria-label="Navegación principal">
        <Link href="/" className="brand">Bildy</Link>
        {!loading && user ? (
          <>
            <div className="nav-links">
              <Link href="/dashboard">Panel</Link><Link href="/clientes">Clientes</Link>
              <Link href="/proyectos">Proyectos</Link><Link href="/albaranes">Albaranes</Link>
            </div>
            <button className="button ghost small" onClick={logout}>Cerrar sesión</button>
          </>
        ) : !loading ? (
          <div className="nav-links"><Link href="/login">Entrar</Link><Link href="/registro">Crear cuenta</Link></div>
        ) : null}
      </nav>
    </header>
  );
}
