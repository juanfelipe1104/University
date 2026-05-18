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
    L = -10.0
    f = lambda t, y: L*y
    a, b = 0, 2
    N = 20
    t = np.linspace(a, b, N)
    y = euler(f, t, 1.0)
    plt.plot(t,y, "o-", label="Euler")
    plt.plot(t, np.exp(t), "d-", label="Exacta")
    plt.xlabel("t")
    plt.ylabel("y")
    plt.legend()
    plt.show()
