"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { ProtectedPage } from "@/components/AuthProvider";
import { EmptyState, Message, PageHeader } from "@/components/ui";
import { apiFetch } from "@/lib/api";

function Clients() {
  const [data, setData] = useState({ clients: [], totalItems: 0 });
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const load = useCallback(async (search = "") => {
    setError("");
    try { setData(await apiFetch(`/client?limit=50&name=${encodeURIComponent(search)}`)); } catch (reason) { setError(reason.message); }
  }, []);
  useEffect(() => {
    const timer = window.setTimeout(load, 0);
    return () => window.clearTimeout(timer);
  }, [load]);
  function search(event) { event.preventDefault(); load(query); }
  return <main className="container"><PageHeader eyebrow={`${data.totalItems} registros`} title="Clientes" description="Empresas y personas para las que se realizan proyectos." actionHref="/clientes/nuevo" actionLabel="Nuevo cliente" />
    <form className="search" onSubmit={search}><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Buscar por nombre" aria-label="Buscar por nombre" /><button className="button secondary">Buscar</button></form><Message type="error">{error}</Message>
    {data.clients.length ? <div className="table-wrap"><table><thead><tr><th>Nombre</th><th>CIF</th><th>Correo</th><th>Teléfono</th><th></th></tr></thead><tbody>{data.clients.map((client) => <tr key={client._id}><td>{client.name || "Sin nombre"}</td><td>{client.cif}</td><td>{client.email || "—"}</td><td>{client.phone || "—"}</td><td><Link className="text-link" href={`/clientes/${client._id}`}>Ver detalle</Link></td></tr>)}</tbody></table></div> : <EmptyState>No hay clientes que coincidan con la búsqueda.</EmptyState>}
  </main>;
}
export default function ClientsPage() { return <ProtectedPage><Clients /></ProtectedPage>; }
