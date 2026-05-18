import numpy as np
from scipy.integrate import trapezoid
import matplotlib.pyplot as plt

x = np.arange(0.0, 1.5, 0.1)  # m
y = np.array(
    [0.0, 0.45, 1.45, 2.3, 3.1, 3.1, 3.1, 2.5, 1.1, 1.1, 1.1, 0.8, 0.6, 0.3, 0.0]
)  # N

W = trapezoid(y, x)

print(f"{W} J")  # J


def trapecio(y, x):
    h = np.diff(x)
    return 0.5 * np.sum(h * (y[:-1] + y[1:]))


def trapecio_equis(y, x):
    h = x[1] - x[0]
    return 0.5 * h * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


W = trapecio_equis(y, x)

print(f"{W} J")  # J


def mostrarArea(x, y):
    plt.plot(x, y, "o-")
    plt.fill_between(x, y, alpha=0.3)
    plt.show()


# mostrarArea(x, y)
