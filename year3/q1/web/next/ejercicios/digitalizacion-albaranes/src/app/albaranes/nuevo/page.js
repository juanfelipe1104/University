"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { ProtectedPage } from "@/components/AuthProvider";
import { Message, PageHeader } from "@/components/ui";
import { apiFetch } from "@/lib/api";

function NewNote() {
  const router = useRouter(); const [clients, setClients] = useState([]); const [projects, setProjects] = useState([]);
  const [client, setClient] = useState(""); const [format, setFormat] = useState("material"); const [hoursMode, setHoursMode] = useState("total");
  const [workers, setWorkers] = useState([{ name: "", hours: "" }]); const [error, setError] = useState(""); const [sending, setSending] = useState(false);
  useEffect(() => { Promise.all([apiFetch("/client?limit=100"), apiFetch("/project?limit=100")]).then(([c, p]) => { setClients(c.clients); setProjects(p.projects); }).catch((reason) => setError(reason.message)); }, []);
  const availableProjects = useMemo(() => projects.filter((project) => (typeof project.client === "object" ? project.client._id : project.client) === client), [projects, client]);
  function updateWorker(index, key, value) { setWorkers((current) => current.map((worker, i) => i === index ? { ...worker, [key]: value } : worker)); }
  async function submit(event) {
    event.preventDefault(); setSending(true); setError(""); const form = new FormData(event.currentTarget);
    const payload = { client, project: form.get("project"), format, description: form.get("description"), workDate: form.get("workDate") };
    if (format === "material") Object.assign(payload, { material: form.get("material"), quantity: Number(form.get("quantity")), unit: form.get("unit") });
    else if (hoursMode === "total") payload.hours = Number(form.get("hours"));
    else payload.workers = workers.map((worker) => ({ name: worker.name, hours: Number(worker.hours) }));
    try { const data = await apiFetch("/deliverynote", { method: "POST", body: JSON.stringify(payload) }); router.push(`/albaranes/${(data.deliveryNote || data)._id}`); } catch (reason) { setError(reason.message); } finally { setSending(false); }
  }
  return <main className="container narrow"><PageHeader eyebrow="Albaranes" title="Nuevo albarán" description="Registra materiales consumidos o tiempo de trabajo." /><form className="panel form-stack" onSubmit={submit}><Message type="error">{error}</Message><div className="form-grid">
    <label>Cliente<select value={client} onChange={(e) => setClient(e.target.value)} required><option value="" disabled>Selecciona un cliente</option>{clients.map((item) => <option key={item._id} value={item._id}>{item.name || item.cif}</option>)}</select></label>
    <label>Proyecto<select name="project" key={client} disabled={!client} required><option value="">Selecciona un proyecto</option>{availableProjects.map((item) => <option key={item._id} value={item._id}>{item.name || item.projectCode}</option>)}</select></label>
    <label>Fecha de trabajo<input type="date" name="workDate" required /></label><label>Tipo<select value={format} onChange={(e) => setFormat(e.target.value)}><option value="material">Material</option><option value="hours">Horas</option></select></label>
    <label className="span-2">Descripción<textarea name="description" rows="3" /></label></div>
    {format === "material" ? <fieldset><legend>Material utilizado</legend><div className="form-grid"><label>Material<input name="material" required /></label><label>Cantidad<input type="number" name="quantity" min="0.01" step="any" required /></label><label>Unidad<input name="unit" placeholder="kg, unidades, m…" required /></label></div></fieldset> : <fieldset><legend>Horas trabajadas</legend><div className="choice-row"><label className="choice"><input type="radio" checked={hoursMode === "total"} onChange={() => setHoursMode("total")} /> Total</label><label className="choice"><input type="radio" checked={hoursMode === "workers"} onChange={() => setHoursMode("workers")} /> Por trabajador</label></div>{hoursMode === "total" ? <label>Horas<input type="number" name="hours" min="0.01" step="any" required /></label> : <div className="worker-list">{workers.map((worker, index) => <div className="worker-row" key={index}><input value={worker.name} onChange={(e) => updateWorker(index, "name", e.target.value)} placeholder="Nombre" aria-label={`Nombre del trabajador ${index + 1}`} required /><input type="number" min="0.01" step="any" value={worker.hours} onChange={(e) => updateWorker(index, "hours", e.target.value)} placeholder="Horas" aria-label={`Horas del trabajador ${index + 1}`} required />{workers.length > 1 && <button type="button" className="button danger small" onClick={() => setWorkers((current) => current.filter((_, i) => i !== index))}>Quitar</button>}</div>)}<button type="button" className="button secondary small" onClick={() => setWorkers((current) => [...current, { name: "", hours: "" }])}>Añadir trabajador</button></div>}</fieldset>}
    <button className="button" disabled={sending}>{sending ? "Creando…" : "Crear albarán"}</button></form></main>;
}
export default function NewNotePage() { return <ProtectedPage><NewNote /></ProtectedPage>; }
