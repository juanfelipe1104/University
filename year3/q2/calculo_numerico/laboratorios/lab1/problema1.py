from math import sqrt

# APARTADO A

print("APARTADO A")

f = lambda x: 1 / (sqrt(x**2 + 1) - x)

x = [1e4, 1e5, 1e6, 1e7, 1e8]

for x_i in x:
    try:
        print(f"x_i: {x_i:e} \t\t f(x_i): {f(x_i):e}")
    except Exception as e:
        print(f"Excepcion: {e}")
        print(f"x_i genera error: {x_i:e}")

"""
En f(1e8) se produce una division entre 0 (error) porque se produce el fenomeno cancelacion catastrofica.
Este fenomeno se produce en el denominador porque al elevar 1e8 al cuadrado, tenemos 1e16 que es un numero muy grande por lo que 1e16 + 1 seguira siendo 1e16.
Luego aplicas una raiz cuadrada tal que el denominador queda 1e8 - 1e8 = 0.
Por lo que a partir de 1e8, el +1 dentro de la raiz es insignificante debido a que x**2 supera el rango de la representacion en coma flotante
"""


# APARTADO B

print("APARTADO B")

f_2 = lambda x: (sqrt(x**2 + 1) + x)

for x_i in x:
    try:
        error_abs = abs(f(x_i) - f_2(x_i))
        error_rel = error_abs / abs(f_2(x_i))
        print(f"x_i: {x_i:e} \t\t f(x_i): {f_2(x_i):e} \t\t error_abs: {error_abs} \t\t error_rel: {error_rel}")
    except Exception as e:
        print(f"Excepcion: {e}")
        print(f"No se puede calcular el error absoluto para x_i: {x_i:e}")

print(f"1e8 funciona en f_2 (funcion que evita el fenomeno). f_2: {f_2(1e8):e}")

"""
Para evitar la cancelacion catastrofica del apartado a), se multiplica por el conjugado del denominador.

"""
