from math import sin, cos
import sympy
import matplotlib.pyplot as plt
# Apartado a)
def f_naive(x):
    return (1-cos(x))/(x**2)

# sen^2(x) + cos^2(x) = 1 ; f(x) = sen^2(x) + cos^2(x) - cos(x) / x^2 = sen^2(x) + cos(x)(cos(x) - 1)/x^2

def f_estable(x):
    return ((sin(x))**2 + cos(x)*(cos(x) - 1))/(x**2)

print(f_naive(1e-8)) # 0.0
print(f_estable(1e-8)) # 1.0

# Apartado B

def d2f(x,h,f):
    return (f(x+h) - 2*f(x) + f(x-h))/(h**2)

d2f_real = lambda x: -4*(x**(-3))*sin(x) + x**(-2)*cos(x) + 6*(x**(-4))*(1-cos(x))

hs = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
errors = []
x = 0.004

for h in hs:
    x_aprox = d2f(x, h, f_estable)
    x_real = d2f_real(x)
    error = abs(x_aprox - x_real)
    errors.append(error)
    print(f"h:{h:e}")
    print(f"f''(x) aprox: {x_aprox}")
    print(f"f''(x) real: {x_real}")
    print(f"error: {error:e}")
    print()
    
plt.figure()
plt.loglog(hs, errors, 'o-', label='curva A (ejemplo)')
plt.xlabel('h')
plt.ylabel('error absoluto')
plt.show()

# Apartado C
# En la grafica podemos ver que el h optimo es 10^-2 ya que a partir de ese momento el error aumenta
# porque en el denominador tenemos un cuadrado, lo que amplifica el error entre más pequeño sea h