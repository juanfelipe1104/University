import numpy as np

error_maquina = np.finfo(float).eps
x_0 = np.pi / 2
f = lambda x: x * np.sin(x)
f_real = 1
h_values = [1e-1, 1e-2, 1e-3, 1e-4]


def calc_fd(f, x, h):
    return (f(x + h) - f(x)) / h


def calc_bd(f, x, h):
    return (f(x) - f(x - h)) / h


def calc_cd(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


def calc_error(derivative, real):
    return abs(derivative - real) / abs(real)


for h in h_values:
    dev_forward = calc_fd(f, x_0, h)
    dev_backward = calc_bd(f, x_0, h)
    dev_center = calc_cd(f, x_0, h)

    print("\n --------------------------------- \n")
    print(f"h: {h:.1e}")
    print(f"Error forward: {calc_error(dev_forward, f_real):.2e}")
    print(f"Error backward: {calc_error(dev_backward, f_real):.2e}")
    print(f"Error centrada: {calc_error(dev_center, f_real):.2e}")
