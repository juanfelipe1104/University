def factorial(x):
    result = 1.0
    for i in range(1,x+1):
        result *= i
    return result

def binom_factorial(a,b):
    return factorial(a) / (factorial(b) * factorial(a-b))

# Apartado A
a = 1
b = a // 2
# No se como se escribe NaN en python (pruebo valores hasta dar con el 171)
for i in range(171):
    binom = binom_factorial(a,b)
    print(f"a: {a}")
    print(f"binom: {binom}")
    a += 1
    b = a // 2

# El mayor alcanzable con binomio factorial es a = 170 con binom = 9.14e49

# Apartado B
a = 1
b = a // 2
def formula_producto(a,b):
    producto = 1.0
    for i in range(1,b):
        producto *= ((a-b+i)/i)
    return producto

# No se como se escribe NaN en python (pruebo valores hasta dar con el 1031)
for j in range(1031):
    binom = formula_producto(a,b)
    print(f"a: {a}")
    print(f"binom: {binom}")
    a += 1
    b = a // 2

# El mayor alcanzable con formula_producto es a = 1030 con binom = 1.42e308

# Apartado C

# No son las mismas formulas, la primera es a!/b!(a-b)! y la segunda es a^b + (-1)^b * (b-1)! / b!
# La diferencia se debe a que ... (relacionado con el error de redondeo)