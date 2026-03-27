from math import cos

def aprox_linealf(a, fa, b, fb):
    v_x = b-a
    v_y = fb-fa
    m = v_y / v_x
    r = lambda y: (y - fa)/m + a

    return r(0)


def biseccion(f, a, b, tol=1.0e-6, maxit=20, verbose=False, aprox_lineal=False):
    fa, fb = f(a), f(b)
    assert fa * fb < 0, "No se cumplen condiciones para aplicar M. de Bisección"
    if verbose:
        print("k\t\tx_k\t\tcota error")
    for k in range(0, maxit):
        if aprox_lineal:
            c = aprox_linealf(a,fa,b,fb)
        else:
            c = (a + b) / 2
        fc = f(c)
        if fa * fc < 0:
            b, fb = c, fc
        elif fc * fb < 0:
            a, fa = c, fc
        else:  # fc == 0
            if verbose:
                print(f"raíz exacta: x*: {c}")
            break

        error = b - a
        if verbose:
            print(f"{k}\t\t{c:.8f}\t{error:e}")

        if error < tol:
            break
    else:
        print(f"Número máximo de iteraciones {maxit} alcanzado")

    return c




f = lambda x: x - cos(x)
eps = 1.0e-6
x_raiz = biseccion(f, -1, 1, tol=eps, verbose=True, aprox_lineal=True)
x_raiz2 = biseccion(f, -1, 1, tol=eps, verbose=True)
print(f"x* = {x_raiz}")
print(f"f(x*) = {f(x_raiz)}")
print(f"x* = {x_raiz2}")
print(f"f(x*) = {f(x_raiz2)}")

"""
El metodo de la biseccion usando aproximacion lineal encuentra la aproximacion exacta del resultado, funciona mejor
"""