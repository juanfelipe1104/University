# APARTADO A
print("APARTADO A")

x_int = 1234567891234567
y_int = 1234567891234566

f = lambda x, y: x**2 - y**2

result_int = f(x_int, y_int)

print(f"x**2 = {x_int**2} \t\t y**2 = {y_int**2} \t\t x**2 - y**2 = {result_int}")

# APARTADO B
print("APARTADO B")

x_float = 1234567891234567.0
y_float = 1234567891234566.0
result_float = f(x_float, y_float)

error_abs = abs(result_float - result_int)
error_rel = error_abs / abs(result_int)

print(f"x**2 = {(x_float**2):e} \t y**2 = {(y_float**2):e} \t x**2 - y**2 = {result_float:e} \t error_abs = {error_abs} \t error_rel = {error_rel}")

"""
Al usar float, se pierde presicion debido al numero de bits maximo usado para la representacion de coma flotante.
Por lo que se comete un error relativo del 0.02 al restar cantidades muy grandes
"""

# APARTADO C
print("APARTADO C")

f_2 = lambda x, y: (x-y)*(x+y)

result_float2 = f_2(x_float, y_float)

error_abs = abs(result_float2 - result_int)
error_rel = error_abs / abs(result_int)
print(f"x**2 = {(x_float**2):e} \t y**2 = {(y_float**2):e} \t x**2 - y**2 = {result_float2:e} \t error_abs = {error_abs} \t error_rel = {error_rel}")

"""
En este caso, no se comete un error ya que se suman y restan cantidades mas pequeñas, en comparacion al apartado b)
"""

