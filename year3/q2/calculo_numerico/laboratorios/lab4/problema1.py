from math import sin, pi


def calc_5p(f, x, h):
    return (f(x - 2.0 * h) - 8.0 * f(x - h) + 8.0 * f(x + h) - f(x + 2.0 * h)) / (12.0 * h)


f = lambda x: x * sin(x)

f = lambda x: x * sin(x)
x = pi / 2.0
exacto = 1

# Apartado B
"""
El orden de convergencia es O(h^4). Vemos que el error se reduce en 10^4 por cada iteración hasta llegar al h optimo 10^-3
"""

h_s = [10 ** (-i) for i in range(1, 4)]
for h in h_s:
    derivada = calc_5p(f, x, h)
    error = abs(derivada - exacto)
    print(f"f' = {derivada} \t\t error = {error}")

# Apartado C
"""
En estas iteraciones lo que ocurre es que el error aumenta a partir de h 10^-4
porque, al tener un orden de convergencia O(h^4), nos acercamos a valores cercanos a 10^-16,
produciendo una cancelación catastrofica en el numerador, amplificada por dividir por una cantidad muy pequeña 
"""

h_s = [10 ** (-i) for i in range(4, 7)]
for h in h_s:
    derivada = calc_5p(f, x, h)
    error = abs(derivada - exacto)
    print(f"f' = {derivada} \t\t error = {error}")
