# Diferencia forward
def calc_fd(f, x, h):
    return (f(x + h) - f(x)) / h


# Diferencia backward
def calc_bd(f, x, h):
    return (f(x) - f(x - h)) / h


# Diferencia centrada
def calc_cd(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


def calc_error(derivative, real):
    return abs(derivative - real) / abs(real)
