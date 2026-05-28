# Se necesitan n + 1 puntos para n subintervalos tal que n es par

import numpy as np
from scipy.integrate import simpson

x = np.arange(0.0, 1.5, 0.1)
y = np.array(
    [0.0, 0.45, 1.45, 2.3, 3.1, 3.1, 3.1, 2.5, 1.1, 1.1, 1.1, 0.8, 0.6, 0.3, 0.0]
)

W = simpson(y, x)

print(f"{W} J")  # J


def simpson_for(y, x):
    n = len(x) - 1
    if n % 2 != 0:
        raise ValueError("Se necesita una cantidad par de subintervalos")

    h = x[1] - x[0]

    area = 0

    for i in range(0, n, 2):
        area += h * (y[i] + 4 * y[i + 1] + y[i + 2]) / 3

    return area


W = simpson_for(y, x)

print(f"{W} J")  # J


def simpson_equis_for(y, x):
    n = len(x) - 1
    if n % 2 != 0:
        raise ValueError("Se necesita una cantidad par de subintervalos")

    h = x[1] - x[0]

    suma = y[0] + y[-1]

    for i in range(1, n):
        if i % 2 == 1:
            suma += 4 * y[i]
        else:
            suma += 2 * y[i]

    return h * suma / 3


W = simpson_equis_for(y, x)

print(f"{W} J")  # J
