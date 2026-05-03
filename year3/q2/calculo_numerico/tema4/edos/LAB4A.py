import numpy as np
import matplotlib.pyplot as plt


def euler(f, t, y0):
    """
    Método de euler explicito para y' = f(t,y) con y(a) = y0
    """
    n = len(t)
    y = np.zeros(n)
    h = (t[-1] - t[0]) / (n - 1)
    y[0] = y0
    for i in range(n - 1):
        y[i + 1] = y[i] + h * f(t[i], y[i])
    return y


if __name__ == "__main__":
    f = lambda t, y: y
    a, b = 0, 2
    Ns = [10, 20, 50, 100, 200, 500, 1000]
    hs = [(b - a) / N for N in Ns]
    errores_euler = []
    for N in Ns:
        t = np.linspace(a, b, N)
        y = euler(f, t, 1.0)
        error_global = abs(y[-1] - np.exp(b))
        errores_euler.append(error_global)

    plt.figure()
    plt.loglog(hs, errores_euler, "-o", label="Euler")
    plt.xlabel("h")
    plt.ylabel("Error Absoluto")
    plt.title("Error de Aproximación Numérica")
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()
