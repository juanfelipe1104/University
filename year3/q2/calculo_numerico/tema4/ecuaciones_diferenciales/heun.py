import numpy as np

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