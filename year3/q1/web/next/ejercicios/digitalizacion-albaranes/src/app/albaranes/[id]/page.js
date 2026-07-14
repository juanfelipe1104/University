"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ProtectedPage } from "@/components/AuthProvider";
import { apiFetch, downloadDeliveryNote } from "@/lib/api";
import { formatDate, Message, PageHeader } from "@/components/ui";

function NoteDetail() {
  const { id } = useParams(); const [note, setNote] = useState(null); const [error, setError] = useState(""); const [downloading, setDownloading] = useState(false);
  useEffect(() => { apiFetch(`/deliverynote/${id}`).then((data) => setNote(data.deliveryNote)).catch((reason) => setError(reason.message)); }, [id]);
  async function download() { setDownloading(true); setError(""); try { await downloadDeliveryNote(id); } catch (reason) { setError(reason.message); } finally { setDownloading(false); } }
  return <main className="container narrow"><PageHeader eyebrow="Albarán" title={note ? `${note.format === "material" ? "Material" : "Horas"} · ${formatDate(note.workDate)}` : "Detalle del albarán"} description={note?.description || "Consulta y descarga el documento."} /><Message type="error">{error}</Message>{note && <div className="panel detail-grid"><div><span>Cliente</span><strong>{note.client?.name || note.client?.cif}</strong></div><div><span>Proyecto</span><strong>{note.project?.name || note.project?.projectCode}</strong></div><div><span>Fecha</span><strong>{formatDate(note.workDate)}</strong></div><div><span>Estado</span><strong>{note.signed ? "Firmado" : "Sin firmar"}</strong></div>{note.format === "material" ? <><div><span>Material</span><strong>{note.material}</strong></div><div><span>Cantidad</span><strong>{note.quantity} {note.unit}</strong></div></> : note.workers?.length ? <div className="span-2"><span>Trabajadores</span><ul>{note.workers.map((worker, index) => <li key={index}>{worker.name}: {worker.hours} h</li>)}</ul></div> : <div><span>Horas</span><strong>{note.hours} h</strong></div>}<div className="span-2"><button className="button" onClick={download} disabled={downloading}>{downloading ? "Preparando PDF…" : "Descargar PDF"}</button></div></div>}</main>;
}
export default function NoteDetailPage() { return <ProtectedPage><NoteDetail /></ProtectedPage>; }
