def punto_fijo(g, x0, tol=1.0e-6, maxit=200, verbose=False):
    xk = x0

    if verbose:
        print("k\t\tx_k\t\tcota error")
        print(f"0\t\t{xk:.8f}\t")

    for k in range(1, maxit):
        xprev = xk
        xk = g(xprev)

        error = abs(xk - xprev)
        if verbose:
            print(f"{k}\t\t{xk:.8f}\t{error:e}")

        if error < tol:
            break
    else:
        xk = None
        print(f"Número máximo de iteraciones {maxit} alcanzado")

    return xk

g = lambda x: (3*(x**2))/(1 + x**2)

#Apartado a)
"""
Los puntos a, c son atractores porque su pendiente es menor que 1. Por el contrario, b es punto repulsor ya que su pendiente es mayor que 1
"""

# Apartado b)
"""
Convergencia punto fijo a: Habrá convergencia unicamente en el intervalo (-b,b) ya que los valores iran descendiendo en "escalera" hacia "a"
- Ejemplo: -0.2 y 0.2 convergen a "a" ya que b es ~0.385
"""
print("Convergencia punto fijo a")
x_root1 = punto_fijo(g, -0.2, maxit=5, verbose=True)
x_root2 = punto_fijo(g, 0.2, maxit=5, verbose=True)

"""
Convergencia punto fijo b: Al ser b un punto fijo repulsor, solo habŕa convergencia en todos los valores que corten a g(x) con la recta y = b.
En este caso b y -b
"""

"""
Convergencia punto fijo c: Habrá convergencia en los intervalos (-inf, -b) y (b, inf) ya que cuando la funcion tiende a +-infinito, tiende a +- 3,
por lo que al ser la pendiente de c cercana a 0, y c ser alrededor de 2.6, todos los valores iran en "escalera" a c
"""

print("Convergencia punto fijo c")
x_root3 = punto_fijo(g, 2.5, maxit=5, verbose=True)
x_root4 = punto_fijo(g, -2.5, maxit=5, verbose=True)