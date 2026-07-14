"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { ProtectedPage } from "@/components/AuthProvider";
import { EmptyState, formatDate, Message, PageHeader } from "@/components/ui";
import { apiFetch } from "@/lib/api";

function Notes() {
  const [data, setData] = useState({ deliveryNotes: [], totalItems: 0 });
  const [clients, setClients] = useState({}); const [projects, setProjects] = useState({});
  const [format, setFormat] = useState(""); const [signed, setSigned] = useState(""); const [error, setError] = useState("");
  const load = useCallback(async (selectedFormat = "", selectedSigned = "") => {
    const query = new URLSearchParams({ limit: "50", sort: "-workDate" });
    if (selectedFormat) query.set("format", selectedFormat); if (selectedSigned) query.set("signed", selectedSigned);
    try { setData(await apiFetch(`/deliverynote?${query}`)); setError(""); } catch (reason) { setError(reason.message); }
  }, []);
  useEffect(() => {
    const timer = window.setTimeout(load, 0);
    Promise.all([apiFetch("/client?limit=100"), apiFetch("/project?limit=100")]).then(([c, p]) => {
      setClients(Object.fromEntries(c.clients.map((item) => [item._id, item.name || item.cif])));
      setProjects(Object.fromEntries(p.projects.map((item) => [item._id, item.name || item.projectCode])));
    }).catch(() => {});
    return () => window.clearTimeout(timer);
  }, [load]);
  return <main className="container"><PageHeader eyebrow={`${data.totalItems} registros`} title="Albaranes" description="Partes de materiales y horas asociados a un proyecto." actionHref="/albaranes/nuevo" actionLabel="Nuevo albarán" />
    <form className="search" onSubmit={(e) => { e.preventDefault(); load(format, signed); }}><select value={format} onChange={(e) => setFormat(e.target.value)} aria-label="Formato"><option value="">Todos los formatos</option><option value="material">Material</option><option value="hours">Horas</option></select><select value={signed} onChange={(e) => setSigned(e.target.value)} aria-label="Firma"><option value="">Todos</option><option value="true">Firmados</option><option value="false">Sin firmar</option></select><button className="button secondary">Filtrar</button></form><Message type="error">{error}</Message>
    {data.deliveryNotes.length ? <div className="table-wrap"><table><thead><tr><th>Fecha</th><th>Tipo</th><th>Cliente</th><th>Proyecto</th><th>Firma</th><th></th></tr></thead><tbody>{data.deliveryNotes.map((note) => <tr key={note._id}><td>{formatDate(note.workDate)}</td><td>{note.format === "material" ? "Material" : "Horas"}</td><td>{clients[note.client] || "—"}</td><td>{projects[note.project] || "—"}</td><td><span className={`badge ${note.signed ? "active" : "inactive"}`}>{note.signed ? "Firmado" : "Pendiente"}</span></td><td><Link className="text-link" href={`/albaranes/${note._id}`}>Ver detalle</Link></td></tr>)}</tbody></table></div> : <EmptyState>No hay albaranes que coincidan con los filtros.</EmptyState>}
  </main>;
}
export default function NotesPage() { return <ProtectedPage><Notes /></ProtectedPage>; }
