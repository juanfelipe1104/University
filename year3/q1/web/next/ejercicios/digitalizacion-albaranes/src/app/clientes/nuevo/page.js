"use client";

import { useRouter } from "next/navigation";
import { ProtectedPage } from "@/components/AuthProvider";
import ClientForm from "@/components/ClientForm";
import { PageHeader } from "@/components/ui";

function NewClient() {
  const router = useRouter();
  return <main className="container narrow"><PageHeader eyebrow="Clientes" title="Nuevo cliente" description="El CIF identifica al cliente dentro de la compañía." /><ClientForm onSaved={(client) => router.push(client?._id ? `/clientes/${client._id}` : "/clientes")} /></main>;
}
export default function NewClientPage() { return <ProtectedPage><NewClient /></ProtectedPage>; }
