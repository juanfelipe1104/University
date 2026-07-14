"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { useAuth } from "@/components/AuthProvider";
import { Message } from "@/components/ui";

export default function VerifyPage() {
  const router = useRouter();
  const { startSession } = useAuth();
  const [code, setCode] = useState("");
  const [devCode, setDevCode] = useState("");
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);
  useEffect(() => {
    const timer = window.setTimeout(() => setDevCode(sessionStorage.getItem("bildy_dev_code") || ""), 0);
    return () => window.clearTimeout(timer);
  }, []);

  async function submit(event) {
    event.preventDefault(); setSending(true); setError("");
    try {
      const data = await apiFetch("/user/validation", { method: "PUT", body: JSON.stringify({ code }) });
      sessionStorage.removeItem("bildy_dev_code");
      await startSession(data);
      router.replace("/onboarding");
    } catch (reason) { setError(reason.message); } finally { setSending(false); }
  }
  return <main className="container auth-shell"><form className="panel auth-card" onSubmit={submit}>
    <p className="eyebrow">Verificación</p><h1>Confirma tu correo</h1><p>Introduce el código de seis dígitos recibido.</p>
    {devCode && <Message>En desarrollo, el código devuelto por la API es <strong>{devCode}</strong>.</Message>}
    <Message type="error">{error}</Message>
    <label>Código<input value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))} inputMode="numeric" pattern="[0-9]{6}" required /></label>
    <button className="button" disabled={sending || code.length !== 6}>{sending ? "Verificando…" : "Verificar cuenta"}</button>
  </form></main>;
}
