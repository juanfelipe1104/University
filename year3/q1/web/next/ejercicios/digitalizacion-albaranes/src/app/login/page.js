"use client";

import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";
import { Suspense, useState } from "react";
import { apiFetch } from "@/lib/api";
import { useAuth } from "@/components/AuthProvider";
import { Message } from "@/components/ui";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { startSession } = useAuth();
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  async function submit(event) {
    event.preventDefault(); setError(""); setSending(true);
    const form = new FormData(event.currentTarget);
    try {
      const session = await apiFetch("/user/login", { method: "POST", body: JSON.stringify(Object.fromEntries(form)) });
      const user = await startSession(session);
      const requested = searchParams.get("next");
      router.replace(requested || (user?.company ? "/dashboard" : "/onboarding"));
    } catch (reason) { setError(reason.message); } finally { setSending(false); }
  }

  return <form className="panel auth-card" onSubmit={submit}><p className="eyebrow">Acceso</p><h1>Bienvenido de nuevo</h1>
    <Message type="error">{error}</Message>
    <label>Correo electrónico<input type="email" name="email" autoComplete="email" required /></label>
    <label>Contraseña<input type="password" name="password" autoComplete="current-password" required /></label>
    <button className="button" disabled={sending}>{sending ? "Entrando…" : "Entrar"}</button>
    <p className="muted">¿No tienes cuenta? <Link className="text-link" href="/registro">Regístrate</Link></p>
  </form>;
}

export default function LoginPage() {
  return <main className="container auth-shell"><Suspense fallback={<p>Preparando formulario…</p>}><LoginForm /></Suspense></main>;
}
