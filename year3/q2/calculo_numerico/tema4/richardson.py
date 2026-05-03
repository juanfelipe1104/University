import numpy as np
from Lab4A import calc_bd, calc_cd, calc_fd, calc_error

error_maquina = np.finfo(float).eps
x_0 = np.pi/2
f = lambda x: x * np.sin(x)
f_real = 1
h_values = [1e-1, 1e-2, 1e-3, 1e-4]



def richard_fd(f, x, h):
    p = 1
    return (2**p*calc_fd(f,x,h/2) - calc_fd(f,x,h))/(2**p - 1)

def richard_cd(f,x,h):
    p = 2
    return (2**p*calc_cd(f,x,h/2) - calc_cd(f,x,h))/(2**p - 1)

def richard_bd(f,x,h):
    p = 1
    return (2**p*calc_bd(f,x,h/2) - calc_bd(f,x,h))/(2**p - 1)

for h in h_values:
    dev_forward = richard_fd(f, x_0, h)
    dev_backward = richard_bd(f, x_0, h)
    dev_center = richard_cd(f, x_0, h)

    print("\n --------------------------------- \n")
    print(f"h: {h:.1e}")
    print(f"Error forward: {calc_error(dev_forward, f_real):.2e}")
    print(f"Error backward: {calc_error(dev_backward, f_real):.2e}")
    print(f"Error centrada: {calc_error(dev_center, f_real):.2e}")