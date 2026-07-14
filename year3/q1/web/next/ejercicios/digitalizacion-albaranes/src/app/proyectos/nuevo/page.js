"use client";

import { useRouter } from "next/navigation";
import { ProtectedPage } from "@/components/AuthProvider";
import ProjectForm from "@/components/ProjectForm";
import { PageHeader } from "@/components/ui";

function NewProject() { const router = useRouter(); return <main className="container narrow"><PageHeader eyebrow="Proyectos" title="Nuevo proyecto" description="Asocia el trabajo a un cliente y asigna un código identificativo." /><ProjectForm onSaved={(project) => router.push(project?._id ? `/proyectos/${project._id}` : "/proyectos")} /></main>; }
export default function NewProjectPage() { return <ProtectedPage><NewProject /></ProtectedPage>; }
