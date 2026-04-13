import numpy as np
import matplotlib.pyplot as plt

error_maquina = np.finfo(float).eps
x_0 = 0.5
f = lambda x: np.exp(np.sin(2*x))
f_derivative = lambda x: 2 * np.cos(2*x) * np.exp(np.sin(2*x))
f_real = f_derivative(x_0)
h_values = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12, 1e-13, 1e-14, 1e-15]

def calc_fd(f, x, h):
    return (f(x +h) -f(x)) / h 
def calc_bd(f, x, h):
    return (f(x) - f(x - h)) / h
def calc_cd(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)
def calc_error_relative(derivative, real):
    return abs(derivative - real)/ abs(real)
def calc_error(derivative, real):
    return abs(derivative - real)

for h in h_values:
    dev_forward = calc_fd(f, x_0, h)
    dev_backward = calc_bd(f, x_0, h)
    dev_center = calc_cd(f, x_0, h)


    print("\n --------------------------------- \n")
    print(f"h: {h:.1e}")
    print(f"Error forward: {calc_error(dev_forward, f_real):.2e}")
    print(f"Error backward: {calc_error(dev_backward, f_real):.2e}")
    print(f"Error centrada: {calc_error(dev_center, f_real):.2e}")

plt.figure()
plt.loglog(h_values, [calc_error(calc_fd(f, x_0, h), f_real) for h in h_values], 'o-', label='Forward')
plt.loglog(h_values, [calc_error(calc_bd(f, x_0, h), f_real) for h in h_values], 's-', label='Backward')
plt.loglog(h_values, [calc_error(calc_cd(f, x_0, h), f_real) for h in h_values], '^-', label='Centered')
plt.xlabel('h')
plt.ylabel('Error Absoluto')
plt.title('Error de Aproximación Numérica')
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()
plt.show()
