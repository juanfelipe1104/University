import numpy as np

def simpson38(f, a, b, N):          # N múltiplo de 3
    assert N % 3 == 0, "N debe ser multiplo de 3"
    x = np.linspace(a, b, N + 1)
    y = f(x)
    h = (b - a) / N
    w = np.ones(N + 1)
    w[1:-1:3] = 3
    w[2:-1:3] = 3
    w[3:-1:3] = 2
    return (3 * h / 8) * np.dot(w, y)

def grado_exactitud(a, b):
    error = 0
    grado = 0
    while error == 0:
        integral_exacta = (b**(grado+1))/(grado+1) - (a**(grado+1))/(grado+1)
        integral_aprox = simpson38(lambda x: x**grado, a, b, 3)
        error = abs(integral_aprox - integral_exacta)
        print(f"Grado: {grado}")
        print(f"Error: {error}")
        if error == 0:
            grado += 1

    return grado - 1

print(grado_exactitud(0,1))

# El grado de exactitud es 2