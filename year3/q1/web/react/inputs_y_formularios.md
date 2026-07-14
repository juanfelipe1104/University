# Inputs y formularios en React

## Inputs controlados

Un input controlado obtiene su valor del estado de React y comunica cada cambio mediante `onChange`.

```jsx
import { useState } from "react";

function SearchInput() {
  const [query, setQuery] = useState("");

  function handleChange(event) {
    setQuery(event.target.value);
  }

  return (
    <label>
      Buscar
      <input value={query} onChange={handleChange} />
    </label>
  );
}
```

El estado es la fuente de verdad. Esto permite validar, transformar o utilizar el valor mientras el usuario escribe. Un input no debe cambiar entre controlado y no controlado: su estado inicial debe ser una cadena, no `undefined`.

Para varios campos puede usarse un objeto:

```jsx
const [form, setForm] = useState({ email: "", password: "" });

function handleChange(event) {
  const { name, value } = event.target;
  setForm((current) => ({ ...current, [name]: value }));
}
```

```jsx
<input name="email" value={form.email} onChange={handleChange} />
<input name="password" value={form.password} onChange={handleChange} />
```

## Inputs no controlados y useRef

Un input no controlado mantiene el valor en el DOM. `useRef` permite consultarlo cuando hace falta:

```jsx
import { useRef } from "react";

function SearchInput() {
  const inputRef = useRef(null);

  function search() {
    const query = inputRef.current.value.trim();
    performSearch(query);
    inputRef.current.value = "";
  }

  return (
    <>
      <input ref={inputRef} />
      <button type="button" onClick={search}>Buscar</button>
    </>
  );
}
```

Una referencia guarda su valor en `current` y persiste entre renderizados, pero modificarla no provoca un renderizado. También se utiliza para enfocar un campo o seleccionar texto.

| Enfoque | Ventajas | Uso habitual |
|---|---|---|
| Controlado | React conoce siempre el valor; validación y UI derivada sencillas | Formularios pequeños o comportamiento inmediato |
| No controlado | Menos actualizaciones de estado; acceso directo al DOM | Formularios simples, integración con APIs del DOM y campos de archivo |

Los campos `<input type="file">` son no controlados por diseño.

## Envío del formulario

```jsx
function handleSubmit(event) {
  event.preventDefault();

  if (!email.trim()) return;
  sendForm({ email });
}

<form onSubmit={handleSubmit}>
  <input value={email} onChange={(event) => setEmail(event.target.value)} />
  <button type="submit">Enviar</button>
</form>;
```

El evento se registra en `form`, no solo en el botón, para admitir también el envío con Enter. La validación del cliente mejora la experiencia, pero el servidor debe validar nuevamente los datos.

## Formik

Formik centraliza valores, cambios, envío, campos visitados y errores.

```console
npm install formik
```

### Formulario básico

```jsx
import { Formik } from "formik";

function LoginForm() {
  return (
    <Formik
      initialValues={{ email: "", password: "" }}
      onSubmit={(values) => console.log(values)}
    >
      {({ values, handleChange, handleSubmit }) => (
        <form onSubmit={handleSubmit}>
          <input
            name="email"
            type="email"
            value={values.email}
            onChange={handleChange}
          />
          <input
            name="password"
            type="password"
            value={values.password}
            onChange={handleChange}
          />
          <button type="submit">Entrar</button>
        </form>
      )}
    </Formik>
  );
}
```

El `name` de cada campo debe coincidir con una propiedad de `initialValues`.

### Validación manual

`validate` recibe los valores y devuelve un objeto cuyas claves son los campos con error.

```jsx
function validate(values) {
  const errors = {};

  if (!values.email) {
    errors.email = "El correo es obligatorio";
  }

  if (values.password.length < 8) {
    errors.password = "Debe tener al menos 8 caracteres";
  }

  return errors;
}
```

Formik valida al cambiar, al perder el foco y antes de enviar. `touched` permite mostrar un error solo después de que el usuario haya visitado el campo:

```jsx
<input
  name="email"
  value={values.email}
  onChange={handleChange}
  onBlur={handleBlur}
/>
{touched.email && errors.email && <p role="alert">{errors.email}</p>}
```

### Componentes de Formik

`Form`, `Field` y `ErrorMessage` reducen el código repetido:

```jsx
import { ErrorMessage, Field, Form, Formik } from "formik";

<Formik initialValues={{ email: "" }} onSubmit={handleSubmit}>
  <Form>
    <Field name="email" type="email" />
    <ErrorMessage name="email" component="p" />
    <button type="submit">Enviar</button>
  </Form>
</Formik>;
```

### Estado de envío

Durante una operación asíncrona, `isSubmitting` permite bloquear nuevos envíos. `setSubmitting(false)` finaliza manualmente ese estado cuando sea necesario.

```jsx
<Formik
  initialValues={{ email: "" }}
  onSubmit={async (values, { setSubmitting }) => {
    try {
      await sendForm(values);
    } finally {
      setSubmitting(false);
    }
  }}
>
  {({ isSubmitting }) => (
    <Form>
      <Field name="email" />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Enviando…" : "Enviar"}
      </button>
    </Form>
  )}
</Formik>
```

## Yup

Yup describe un esquema reutilizable de validación.

```console
npm install yup
```

```jsx
import * as Yup from "yup";

const loginSchema = Yup.object({
  email: Yup.string()
    .email("Introduce un correo válido")
    .required("El correo es obligatorio"),
  password: Yup.string()
    .min(8, "Debe tener al menos 8 caracteres")
    .required("La contraseña es obligatoria"),
});
```

Formik recibe el esquema mediante `validationSchema`:

```jsx
<Formik
  initialValues={{ email: "", password: "" }}
  validationSchema={loginSchema}
  onSubmit={handleSubmit}
>
  {/* formulario */}
</Formik>
```

Los nombres del esquema deben coincidir con los de `initialValues` y los campos.

## React Hook Form

React Hook Form registra los inputs y reduce los renderizados provocados por cada pulsación, por lo que resulta adecuado para formularios amplios.

```console
npm install react-hook-form
```

### Formulario básico

```jsx
import { useForm } from "react-hook-form";

function LoginForm() {
  const { register, handleSubmit, reset } = useForm({
    defaultValues: {
      email: "",
      password: "",
    },
  });

  function onSubmit(data) {
    console.log(data);
    reset();
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="email" {...register("email")} />
      <input type="password" {...register("password")} />
      <button type="submit">Entrar</button>
    </form>
  );
}
```

`register` devuelve `name`, `ref`, `onChange` y `onBlur`. El operador spread conecta todas esas propiedades con el input.

### Validaciones y errores

```jsx
const {
  register,
  handleSubmit,
  formState: { errors, isSubmitting },
} = useForm();
```

```jsx
<input
  type="email"
  aria-invalid={Boolean(errors.email)}
  {...register("email", {
    required: "El correo es obligatorio",
    pattern: {
      value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: "Introduce un correo válido",
    },
  })}
/>
{errors.email && <p role="alert">{errors.email.message}</p>}
```

Las reglas se pasan como segundo argumento de `register`. Cada regla puede incluir `value` y `message`.

### React Hook Form con Yup

```console
npm install yup @hookform/resolvers
```

```jsx
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";

const {
  register,
  handleSubmit,
  formState: { errors },
} = useForm({
  resolver: yupResolver(loginSchema),
});
```

El resolver adapta los errores producidos por Yup al formato de React Hook Form.

## Elección del enfoque

| Situación | Enfoque |
|---|---|
| Uno o pocos campos con respuesta inmediata | Estado controlado |
| Acceso puntual al valor o API del DOM | `useRef` |
| Formulario mediano con API declarativa sencilla | Formik |
| Formulario grande o sensible a renderizados | React Hook Form |
| Reglas compartidas o complejas | Yup con Formik o React Hook Form |

Una biblioteca no elimina la necesidad de diseñar estados de carga, errores del servidor, accesibilidad, desactivación durante el envío y mensajes comprensibles.
