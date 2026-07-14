import "./globals.css";
import { AuthProvider } from "@/components/AuthProvider";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: { default: "Bildy | Albaranes digitales", template: "%s | Bildy" },
  description: "Gestión de clientes, proyectos y albaranes digitales",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body><AuthProvider><Navbar />{children}</AuthProvider></body>
    </html>
  );
}
