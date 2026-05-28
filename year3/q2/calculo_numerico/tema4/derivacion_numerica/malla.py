def calc_fd(f_x, f_next, h):
    return (f_next - f_x) / h


def calc_bd(f_x, f_prev, h):
    return (f_x - f_prev) / h


def calc_cd(f_next, f_prev, h):
    return (f_next - f_prev) / (2 * h)


malla: list = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
h = malla[1][0] - malla[0][0]


# Función para calcular la derivada usando diferencias finitas
def derivada(malla, h):
    derivadas = []
    for k in range(0, len(malla)):
        if k == 0:
            # Primer punto: diferencia forward
            derivadas.append(calc_fd(malla[k][1], malla[k + 1][1], h))
        elif k == len(malla) - 1:
            # Último punto: diferencia backward
            derivadas.append(calc_bd(malla[k][1], malla[k - 1][1], h))
        else:
            # Puntos interiores: diferencia central
            derivadas.append(calc_cd(malla[k + 1][1], malla[k - 1][1], h))

    return derivadas


derivadas = derivada(malla, h)
print("Derivadas en cada punto de la malla:")
for i, (x, f_x) in enumerate(malla):
    print(f"x: {x}, f(x): {f_x}, Derivada: {derivadas[i]}")
