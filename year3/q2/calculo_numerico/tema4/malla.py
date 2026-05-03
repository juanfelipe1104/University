def calc_fd(f_x, f_next, h):
    return (f_next - f_x) / h


def calc_bd(f_x, f_prev, h):
    return (f_x - f_prev) / h


def calc_cd(f_next, f_prev, h):
    return (f_next - f_prev) / (2 * h)


# Sacar derivadas de una malla (puntos (x, f(x))) equispaciada (distancia h)
# Malla de puntos
malla: list = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]  # Array de tuplas con formato (x, f(x))
h = malla[1][0] - malla[0][0]  # Distancia entre puntos (asumiendo que es constante)


# Función para calcular la derivada usando diferencias finitas
def derivada(malla, h):
    if len(malla) < 2:
        raise ValueError("La malla debe tener al menos 2 puntos")
    if h == 0:
        raise ValueError("h no puede ser 0")

    # Verifica que la malla sea equiespaciada con el h indicado
    for i in range(1, len(malla)):
        dx = malla[i][0] - malla[i - 1][0]
        if abs(dx - h) > 1e-12:
            raise ValueError("La malla no es equiespaciada o h no coincide con la malla")

    derivadas = []
    for k in range(0, len(malla)):
        if k == 0:
            # Primer punto: diferencia hacia adelante
            derivadas.append(calc_fd(malla[k][1], malla[k + 1][1], h))
        elif k == len(malla) - 1:
            # Último punto: diferencia hacia atrás
            derivadas.append(calc_bd(malla[k][1], malla[k - 1][1], h))
        else:
            # Puntos interiores: diferencia central
            derivadas.append(calc_cd(malla[k + 1][1], malla[k - 1][1], h))

    return derivadas


derivadas = derivada(malla, h)
print("Derivadas en cada punto de la malla:")
for i, (x, f_x) in enumerate(malla):
    print(f"x: {x}, f(x): {f_x}, Derivada: {derivadas[i]}")
