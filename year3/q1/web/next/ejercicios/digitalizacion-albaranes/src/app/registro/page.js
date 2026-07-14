"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { apiFetch } from "@/lib/api";
import { saveTokens } from "@/lib/auth";
import { Message } from "@/components/ui";

export default function RegisterPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);
  async function submit(event) {
    event.preventDefault(); setError("");
    const form = new FormData(event.currentTarget);
    if (form.get("password") !== form.get("confirm")) { setError("Las contraseñas no coinciden"); return; }
    setSending(true);
    try {
      const data = await apiFetch("/user/register", { method: "POST", body: JSON.stringify({ email: form.get("email"), password: form.get("password") }) });
      saveTokens(data);
      if (data.verificationCode) sessionStorage.setItem("bildy_dev_code", data.verificationCode);
      router.push("/verificar");
    } catch (reason) { setError(reason.message); } finally { setSending(false); }
  }
  return <main className="container auth-shell"><form className="panel auth-card" onSubmit={submit}>
    <p className="eyebrow">Nueva cuenta</p><h1>Empieza a digitalizar</h1><Message type="error">{error}</Message>
    <label>Correo electrónico<input type="email" name="email" autoComplete="email" required /></label>
    <label>Contraseña<input type="password" name="password" minLength="8" maxLength="16" autoComplete="new-password" required /><small>Entre 8 y 16 caracteres.</small></label>
    <label>Repite la contraseña<input type="password" name="confirm" minLength="8" maxLength="16" autoComplete="new-password" required /></label>
    <button className="button" disabled={sending}>{sending ? "Creando…" : "Crear cuenta"}</button>
    <p className="muted">¿Ya estás registrado? <Link className="text-link" href="/login">Inicia sesión</Link></p>
  </form></main>;
}
