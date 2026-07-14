"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { clearTokens, getAccessToken, saveTokens } from "@/lib/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadUser = useCallback(async () => {
    if (!getAccessToken()) {
      setUser(null);
      setLoading(false);
      return null;
    }
    setLoading(true);
    try {
      const data = await apiFetch("/user");
      setUser(data.user);
      return data.user;
    } catch {
      clearTokens();
      setUser(null);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(loadUser, 0);
    return () => window.clearTimeout(timer);
  }, [loadUser]);

  const value = useMemo(() => ({
    user,
    loading,
    loadUser,
    startSession(data) {
      saveTokens(data);
      setLoading(true);
      return loadUser();
    },
    endSession() {
      clearTokens();
      setUser(null);
    },
  }), [user, loading, loadUser]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth debe utilizarse dentro de AuthProvider");
  return context;
}

export function ProtectedPage({ children, requireCompany = true }) {
  const { user, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (loading) return;
    if (!user) router.replace(`/login?next=${encodeURIComponent(pathname)}`);
    else if (requireCompany && !user.company) router.replace("/onboarding");
  }, [loading, user, requireCompany, router, pathname]);

  if (loading || !user || (requireCompany && !user.company)) {
    return <main className="container"><p className="status">Comprobando sesión…</p></main>;
  }
  return children;
}
