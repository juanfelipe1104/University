"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ProtectedPage } from "@/components/AuthProvider";
import ClientForm from "@/components/ClientForm";
import { Message, PageHeader } from "@/components/ui";
import { apiFetch } from "@/lib/api";

function ClientDetail() {
  const { id } = useParams();
  const [client, setClient] = useState(null);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState("");
  useEffect(() => { apiFetch(`/client/${id}`).then((data) => setClient(data.client)).catch((reason) => setError(reason.message)); }, [id]);
  return <main className="container narrow"><PageHeader eyebrow="Cliente" title={client?.name || "Detalle del cliente"} description={client ? `CIF ${client.cif}` : "Cargando información…"} /><Message type="error">{error}</Message><Message type="success">{saved}</Message>{client && <ClientForm client={client} onSaved={(updated) => { setClient(updated); setSaved("Cliente actualizado correctamente"); }} />}</main>;
}
export default function ClientDetailPage() { return <ProtectedPage><ClientDetail /></ProtectedPage>; }
