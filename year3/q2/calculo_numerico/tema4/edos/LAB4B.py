import numpy as np
import matplotlib.pyplot as plt


def euler(f, t, y0):
    """Método de Euler explícito para y' = f(t,y) con y(a) = y0"""
    n = len(t)
    y = np.zeros(n)
    y[0] = y0
    for i in range(n - 1):
        h = t[i + 1] - t[i]
        y[i + 1] = y[i] + h * f(t[i], y[i])
    return y


def heun(f, t, y0):
    """
    Método de Heun (Euler mejorado) para y' = f(t,y) con y(a) = y0
    Predictor:  ỹ_{i+1} = y_i + h·f(t_i, y_i)          (Euler)
    Corrector:  y_{i+1} = y_i + h/2·[f(t_i, y_i) + f(t_{i+1}, ỹ_{i+1})]
    """
    n = len(t)
    y = np.zeros(n)
    h = (t[-1] - t[0]) / (n - 1)
    y[0] = y0
    for i in range(n - 1):
        k1 = f(t[i], y[i])
        k2 = f(t[i + 1], y[i] + h * k1)
        y[i + 1] = y[i] + (h / 2) * (k1 + k2)
    return y


if __name__ == "__main__":
    f = lambda t, y: y
    a, b = 0, 2
    y_exact = np.exp(b)

    N_values = [10, 20, 50, 100, 200, 500, 1000]

    h_values = []
    errors_euler = []
    errors_heun = []

    print(f"{'N':>6}  {'h':>9}  {'Error Euler':>13}  {'Error Heun':>13}")
    print("-" * 48)

    for N in N_values:
        t = np.linspace(a, b, N + 1)  # N+1 nodos → N pasos, h = 2/N
        h = (b - a) / N

        y_euler = euler(f, t, 1.0)
        y_heun = heun(f, t, 1.0)

        err_euler = abs(y_euler[-1] - y_exact)
        err_heun = abs(y_heun[-1] - y_exact)

        h_values.append(h)
        errors_euler.append(err_euler)
        errors_heun.append(err_heun)

        print(f"{N:>6}  {h:>9.5f}  {err_euler:>13.2e}  {err_heun:>13.2e}")

    # ---------- Gráfica log-log ----------
    h_arr = np.array(h_values)
    e_arr = np.array(errors_euler)
    he_arr = np.array(errors_heun)

    # Ajuste lineal en escala log → pendiente ≈ orden del método
    slope_euler = np.polyfit(np.log(h_arr), np.log(e_arr), 1)[0]
    slope_heun = np.polyfit(np.log(h_arr), np.log(he_arr), 1)[0]

    # Rectas de referencia O(h) y O(h²)
    C1 = np.exp(np.polyfit(np.log(h_arr), np.log(e_arr), 1)[1])
    C2 = np.exp(np.polyfit(np.log(h_arr), np.log(he_arr), 1)[1])
    ref_euler = C1 * h_arr**slope_euler
    ref_heun = C2 * h_arr**slope_heun

    plt.figure(figsize=(8, 5))

    plt.loglog(
        h_arr,
        e_arr,
        "o-",
        color="steelblue",
        label=f"Euler  (pendiente ≈ {slope_euler:.2f})",
    )
    plt.loglog(
        h_arr,
        ref_euler,
        "--",
        color="steelblue",
        alpha=0.5,
        label=f"Ref. $O(h^{{{slope_euler:.2f}}})$",
    )

    plt.loglog(
        h_arr,
        he_arr,
        "s-",
        color="tomato",
        label=f"Heun   (pendiente ≈ {slope_heun:.2f})",
    )
    plt.loglog(
        h_arr,
        ref_heun,
        "--",
        color="tomato",
        alpha=0.5,
        label=f"Ref. $O(h^{{{slope_heun:.2f}}})$",
    )

    plt.xlabel("$h$", fontsize=13)
    plt.ylabel("$|y_N - e^2|$", fontsize=13)
    plt.title("Convergencia: Euler vs Heun", fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, which="both", ls=":")
    plt.tight_layout()
    plt.savefig("euler_heun_convergencia.png", dpi=150)
    plt.show()

    print(f"\nPendiente Euler ≈ {slope_euler:.4f}  → O(h)")
    print(f"Pendiente Heun  ≈ {slope_heun:.4f}  → O(h²)")
