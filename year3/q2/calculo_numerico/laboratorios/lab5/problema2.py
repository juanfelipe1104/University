from math import e, exp

def integral(f, a, b):
    h = (b-a)/3
    x1 = a + h
    x2 = b
    return ((9/4)*h*f(x1)) + ((3/4)*h*f(x2))

def grado_exactitud(a, b):
    grado = 0
    error = 0
    while error == 0.0:
        f = lambda x: x**grado
        exacto = (b**(grado + 1) - a**(grado + 1)) / (grado + 1)
        aprox = integral(f, a, b)
        error = exacto - aprox
        if error == 0.0:
            grado += 1
    return grado - 1

f = lambda x: x**2 * exp(-x)

# Integral de f en [0,1]
a = 0
b = 1

# Apartado a)
grado = grado_exactitud(a, b)
print(f"Grado de exactitud: {grado}")

# Apartado b) y c)
exacto = 2 - (5/e)
aprox = integral(f, a, b)

error = abs(exacto - aprox)

print(f"Valor exacto: {exacto}")
print(f"Valor aproximado: {aprox}")
print(f"Error: {error:e}")