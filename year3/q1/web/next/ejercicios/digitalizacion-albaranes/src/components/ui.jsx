import Link from "next/link";

export function PageHeader({ eyebrow, title, description, actionHref, actionLabel }) {
  return (
    <div className="page-header">
      <div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1>{description && <p>{description}</p>}</div>
      {actionHref && <Link className="button" href={actionHref}>{actionLabel}</Link>}
    </div>
  );
}

export function Message({ type = "info", children }) {
  return children ? <p className={`message ${type}`} role={type === "error" ? "alert" : "status"}>{children}</p> : null;
}

export function EmptyState({ children }) { return <div className="empty">{children}</div>; }

export function AddressFields({ prefix = "", required = false, values = {}, onChange }) {
  const field = (name) => `${prefix}${name}`;
  return (
    <fieldset><legend>Dirección</legend><div className="form-grid">
      <label className="span-2">Calle<input name={field("street")} value={values.street || ""} onChange={onChange} required={required} /></label>
      <label>Número<input name={field("number")} value={values.number || ""} onChange={onChange} required={required} /></label>
      <label>Código postal<input name={field("postal")} value={values.postal || ""} onChange={onChange} inputMode="numeric" pattern="[0-9]{5}" required={required} /></label>
      <label>Ciudad<input name={field("city")} value={values.city || ""} onChange={onChange} required={required} /></label>
      <label>Provincia<input name={field("province")} value={values.province || ""} onChange={onChange} required={required} /></label>
    </div></fieldset>
  );
}

export function formatDate(value) {
  if (!value) return "—";
  return new Intl.DateTimeFormat("es-ES", { dateStyle: "medium" }).format(new Date(value));
}
