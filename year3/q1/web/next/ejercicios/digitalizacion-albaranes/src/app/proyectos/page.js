"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { ProtectedPage } from "@/components/AuthProvider";
import { EmptyState, Message, PageHeader } from "@/components/ui";
import { apiFetch } from "@/lib/api";

function Projects() {
  const [data, setData] = useState({ projects: [], totalItems: 0 });
  const [clients, setClients] = useState({});
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const load = useCallback(async (search = "") => {
    try { setData(await apiFetch(`/project?limit=50&name=${encodeURIComponent(search)}`)); setError(""); } catch (reason) { setError(reason.message); }
  }, []);
  useEffect(() => {
    const timer = window.setTimeout(load, 0);
    apiFetch("/client?limit=100").then((result) => setClients(Object.fromEntries(result.clients.map((client) => [client._id, client.name || client.cif])))).catch(() => {});
    return () => window.clearTimeout(timer);
  }, [load]);
  return <main className="container"><PageHeader eyebrow={`${data.totalItems} registros`} title="Proyectos" description="Trabajos vinculados a los clientes de la compañía." actionHref="/proyectos/nuevo" actionLabel="Nuevo proyecto" />
    <form className="search" onSubmit={(event) => { event.preventDefault(); load(query); }}><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Buscar por nombre" aria-label="Buscar por nombre" /><button className="button secondary">Buscar</button></form><Message type="error">{error}</Message>
    {data.projects.length ? <div className="table-wrap"><table><thead><tr><th>Código</th><th>Proyecto</th><th>Cliente</th><th>Estado</th><th></th></tr></thead><tbody>{data.projects.map((project) => <tr key={project._id}><td>{project.projectCode}</td><td>{project.name || "Sin nombre"}</td><td>{clients[typeof project.client === "object" ? project.client._id : project.client] || "—"}</td><td><span className={`badge ${project.active === false ? "inactive" : "active"}`}>{project.active === false ? "Inactivo" : "Activo"}</span></td><td><Link className="text-link" href={`/proyectos/${project._id}`}>Ver detalle</Link></td></tr>)}</tbody></table></div> : <EmptyState>No hay proyectos que coincidan con la búsqueda.</EmptyState>}
  </main>;
}
export default function ProjectsPage() { return <ProtectedPage><Projects /></ProtectedPage>; }
