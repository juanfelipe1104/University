"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ProtectedPage, useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import { Message, PageHeader } from "@/components/ui";

function Dashboard() {
  const { user } = useAuth();
  const [counts, setCounts] = useState({ clients: "—", projects: "—", deliveryNotes: "—" });
  const [error, setError] = useState("");
  useEffect(() => {
    Promise.all([apiFetch("/client?limit=1"), apiFetch("/project?limit=1"), apiFetch("/deliverynote?limit=1")])
      .then(([clients, projects, notes]) => setCounts({ clients: clients.totalItems, projects: projects.totalItems, deliveryNotes: notes.totalItems }))
      .catch((reason) => setError(reason.message));
  }, []);
  return <main className="container"><PageHeader eyebrow="Panel de control" title={`Hola, ${user.name || user.email}`} description="Consulta el estado de la actividad y accede a las operaciones habituales." /><Message type="error">{error}</Message>
    <section className="stats"><Link href="/clientes" className="stat"><strong>{counts.clients}</strong><span>Clientes</span></Link><Link href="/proyectos" className="stat"><strong>{counts.projects}</strong><span>Proyectos</span></Link><Link href="/albaranes" className="stat"><strong>{counts.deliveryNotes}</strong><span>Albaranes</span></Link></section>
    <section><h2>Acciones rápidas</h2><div className="feature-grid"><Link href="/clientes/nuevo" className="card interactive"><span>+</span><h3>Nuevo cliente</h3></Link><Link href="/proyectos/nuevo" className="card interactive"><span>+</span><h3>Nuevo proyecto</h3></Link><Link href="/albaranes/nuevo" className="card interactive"><span>+</span><h3>Nuevo albarán</h3></Link></div></section>
  </main>;
}

export default function DashboardPage() { return <ProtectedPage><Dashboard /></ProtectedPage>; }
