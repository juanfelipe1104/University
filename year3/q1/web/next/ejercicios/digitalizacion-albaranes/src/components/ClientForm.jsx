"use client";

import { useState } from "react";
import { AddressFields, Message } from "./ui";
import { apiFetch } from "@/lib/api";

const emptyAddress = { street: "", number: "", postal: "", city: "", province: "" };

export default function ClientForm({ client, onSaved }) {
  const [address, setAddress] = useState(client?.address || emptyAddress);
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);
  function changeAddress(event) { setAddress((current) => ({ ...current, [event.target.name]: event.target.value })); }
  async function submit(event) {
    event.preventDefault(); setSending(true); setError("");
    const form = new FormData(event.currentTarget);
    const payload = Object.fromEntries(["name", "cif", "email", "phone"].map((key) => [key, form.get(key)])
      .filter(([, value]) => value));
    if (Object.values(address).some(Boolean)) payload.address = address;
    try {
      const data = await apiFetch(client ? `/client/${client._id}` : "/client", { method: client ? "PUT" : "POST", body: JSON.stringify(payload) });
      onSaved(data.client || data);
    } catch (reason) { setError(reason.message); } finally { setSending(false); }
  }
  return <form className="panel form-stack" onSubmit={submit}><Message type="error">{error}</Message><div className="form-grid">
    <label>Nombre<input name="name" defaultValue={client?.name || ""} required /></label><label>CIF<input name="cif" defaultValue={client?.cif || ""} placeholder="B12345678" required /></label>
    <label>Correo<input type="email" name="email" defaultValue={client?.email || ""} /></label><label>Teléfono<input type="tel" name="phone" defaultValue={client?.phone || ""} /></label>
    </div><AddressFields values={address} onChange={changeAddress} /><button className="button" disabled={sending}>{sending ? "Guardando…" : client ? "Guardar cambios" : "Crear cliente"}</button></form>;
}
