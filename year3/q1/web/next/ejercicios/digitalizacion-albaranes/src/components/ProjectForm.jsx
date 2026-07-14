"use client";

import { useEffect, useState } from "react";
import { AddressFields, Message } from "./ui";
import { apiFetch } from "@/lib/api";

const emptyAddress = { street: "", number: "", postal: "", city: "", province: "" };

export default function ProjectForm({ project, onSaved }) {
  const [clients, setClients] = useState([]);
  const [address, setAddress] = useState(project?.address || emptyAddress);
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);
  useEffect(() => { apiFetch("/client?limit=100").then((data) => setClients(data.clients)).catch((reason) => setError(reason.message)); }, []);
  function changeAddress(event) { setAddress((current) => ({ ...current, [event.target.name]: event.target.value })); }
  async function submit(event) {
    event.preventDefault(); setSending(true); setError("");
    const form = new FormData(event.currentTarget);
    const fields = project ? ["projectCode", "name", "email", "notes"] : ["client", "projectCode", "name", "email", "notes"];
    const payload = Object.fromEntries(fields.map((key) => [key, form.get(key)]).filter(([, value]) => value));
    if (Object.values(address).some(Boolean)) payload.address = address;
    if (project) payload.active = form.get("active") === "on";
    try {
      const data = await apiFetch(project ? `/project/${project._id}` : "/project", { method: project ? "PUT" : "POST", body: JSON.stringify(payload) });
      onSaved(data.project || data);
    } catch (reason) { setError(reason.message); } finally { setSending(false); }
  }
  const currentClient = typeof project?.client === "object" ? project.client._id : project?.client;
  return <form className="panel form-stack" onSubmit={submit}><Message type="error">{error}</Message><div className="form-grid">
    <label>Cliente<select name="client" defaultValue={currentClient || ""} disabled={Boolean(project)} required><option value="" disabled>Selecciona un cliente</option>{clients.map((client) => <option key={client._id} value={client._id}>{client.name || client.cif}</option>)}</select></label>
    <label>Código de proyecto<input name="projectCode" defaultValue={project?.projectCode || ""} required /></label>
    <label>Nombre<input name="name" defaultValue={project?.name || ""} /></label><label>Correo de contacto<input type="email" name="email" defaultValue={project?.email || ""} /></label>
    <label className="span-2">Notas<textarea name="notes" defaultValue={project?.notes || ""} rows="4" /></label>
    {project && <label className="choice"><input type="checkbox" name="active" defaultChecked={project.active !== false} /> Proyecto activo</label>}
    </div><AddressFields values={address} onChange={changeAddress} /><button className="button" disabled={sending}>{sending ? "Guardando…" : project ? "Guardar cambios" : "Crear proyecto"}</button></form>;
}
