from math import log
from scipy.optimize import fixed_point
def calc_r(e1, e2, e3):
    return log(e2/e3) / log(e1/e2)

def halley(f, df, d2f, x0, tol=1e-8, maxit=50, verbose=True):
    x = x0
    errors = []
    r = 0
    C = 0
    if verbose:
        print("i\t\tx\t\terror\t\tr\t\tC")
    for i in range(maxit):
        x_next = x - ((2*f(x)*df(x))/((2*(df(x)**2))-(f(x)*d2f(x))))
        error = abs(x_next - 2**(1/3))
        errors.append(error)
        
        if len(errors) >= 3:
            r = calc_r(errors[-3], errors[-2], errors[-1])
            C = errors[2] / (errors[1]**r)
            errors.pop(0)
        
        if verbose:
            print(f"{i}\t\t{x:e}\t\t{error:e}\t\t{r:.2f}\t\t{C:.2f}")

        if(error < tol):
            return x_next

        x = x_next
    return x

f = lambda x: x**3 - 2

df = lambda x: 3*(x**2)

d2f = lambda x: 6*x

def g(x):
    return x - ((2*f(x)*df(x))/((2*(df(x)**2))-(f(x)*d2f(x))))

x0 = 1.3

x = halley(f, df, d2f, x0)

x_opt = fixed_point(g, x0)

print(f"Halley: {x}")
print(f"Halley optimo: {x_opt}")

# Apartado a)
# Empezando en 1.3, halley encuentra en la segunda iteracion la raiz, viendo como el error pasa de 2.5e-5 a 7.1e-15.
# Vemos que se reduce aproximadamente en orden 3; por lo que r = 3

# Apartado b)
# El metodo de halley se puede escribir como x_k+1 = g(x_k) tal que g(x_k) = x_k - ((2*f(x_k)*f'(x_k))/((2*(f'(x_k)**2))-(f'(x_k)*f''(x_k))))
# scipy.optimize.fixed_point converge al mismo valor que el apartado a): 1.2599
