"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ProtectedPage } from "@/components/AuthProvider";
import ProjectForm from "@/components/ProjectForm";
import { Message, PageHeader } from "@/components/ui";
import { apiFetch } from "@/lib/api";

function ProjectDetail() {
  const { id } = useParams(); const [project, setProject] = useState(null); const [error, setError] = useState(""); const [saved, setSaved] = useState("");
  useEffect(() => { apiFetch(`/project/${id}`).then((data) => setProject(data.project)).catch((reason) => setError(reason.message)); }, [id]);
  return <main className="container narrow"><PageHeader eyebrow="Proyecto" title={project?.name || project?.projectCode || "Detalle del proyecto"} description={project ? `Código ${project.projectCode}` : "Cargando información…"} /><Message type="error">{error}</Message><Message type="success">{saved}</Message>{project && <ProjectForm project={project} onSaved={(updated) => { setProject(updated); setSaved("Proyecto actualizado correctamente"); }} />}</main>;
}
export default function ProjectDetailPage() { return <ProtectedPage><ProjectDetail /></ProtectedPage>; }
