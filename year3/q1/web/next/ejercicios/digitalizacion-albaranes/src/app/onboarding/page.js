"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ProtectedPage, useAuth } from "@/components/AuthProvider";
import { AddressFields, Message, PageHeader } from "@/components/ui";
import { apiFetch } from "@/lib/api";

const blankAddress = { street: "", number: "", postal: "", city: "", province: "" };

function OnboardingForm() {
  const { user, loadUser } = useAuth();
  const router = useRouter();
  const [step, setStep] = useState(user.name && user.nif ? 2 : 1);
  const [freelance, setFreelance] = useState(true);
  const [address, setAddress] = useState(user.address || blankAddress);
  const [companyAddress, setCompanyAddress] = useState(blankAddress);
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  function updateAddress(setter) {
    return (event) => setter((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function saveProfile(event) {
    event.preventDefault(); setSending(true); setError("");
    const form = new FormData(event.currentTarget);
    try {
      await apiFetch("/user/register", { method: "PUT", body: JSON.stringify({ name: form.get("name"), lastName: form.get("lastName"), nif: form.get("nif"), address }) });
      await loadUser(); setStep(2);
    } catch (reason) { setError(reason.message); } finally { setSending(false); }
  }

  async function saveCompany(event) {
    event.preventDefault(); setSending(true); setError("");
    const form = new FormData(event.currentTarget);
    const payload = freelance ? { isFreelance: true } : { isFreelance: false, name: form.get("companyName"), cif: form.get("cif"), address: companyAddress };
    try {
      await apiFetch("/user/company", { method: "PATCH", body: JSON.stringify(payload) });
      await loadUser(); router.replace("/dashboard");
    } catch (reason) { setError(reason.message); } finally { setSending(false); }
  }

  return <main className="container narrow"><PageHeader eyebrow={`Configuración · Paso ${step} de 2`} title={step === 1 ? "Completa tu perfil" : "Configura tu empresa"} description="Estos datos aparecerán asociados a tu actividad y tus albaranes." /><Message type="error">{error}</Message>
    {step === 1 ? <form className="panel form-stack" onSubmit={saveProfile}>
      <div className="form-grid"><label>Nombre<input name="name" defaultValue={user.name || ""} required /></label><label>Apellidos<input name="lastName" defaultValue={user.lastName || ""} required /></label><label>NIF / NIE<input name="nif" defaultValue={user.nif || ""} required /></label></div>
      <AddressFields values={address} onChange={updateAddress(setAddress)} required />
      <button className="button" disabled={sending}>{sending ? "Guardando…" : "Continuar"}</button>
    </form> : <form className="panel form-stack" onSubmit={saveCompany}>
      <fieldset><legend>Tipo de actividad</legend><div className="choice-row"><label className="choice"><input type="radio" checked={freelance} onChange={() => setFreelance(true)} /> Autónomo</label><label className="choice"><input type="radio" checked={!freelance} onChange={() => setFreelance(false)} /> Empresa</label></div></fieldset>
      {freelance ? <p className="message info">La empresa utilizará el nombre, NIF y dirección de tu perfil.</p> : <><div className="form-grid"><label>Razón social<input name="companyName" required /></label><label>CIF<input name="cif" placeholder="B12345678" required /></label></div><AddressFields values={companyAddress} onChange={updateAddress(setCompanyAddress)} required /></>}
      <button className="button" disabled={sending}>{sending ? "Configurando…" : "Finalizar configuración"}</button>
    </form>}
  </main>;
}

export default function OnboardingPage() { return <ProtectedPage requireCompany={false}><OnboardingForm /></ProtectedPage>; }
