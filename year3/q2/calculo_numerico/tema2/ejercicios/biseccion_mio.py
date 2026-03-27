from math import log

def error(a, b):
    return abs(b-a)

def calculate_r(e1,e2,e3):
    return log(e2/e3)/log(e1/e2)

def biseccion(f,a,b,tol=1.e-6,maxit=200):
    f_a, f_b = f(a), f(b)
    assert f_a * f_b < 0, "No se cumplen las condiciones"
    c = 0
    errors = []
    for i in range(maxit):
        if(error(a,b) < tol):
            break
        c = (a+b)/2
        f_c = f(c)
        if f_c * f_a < 0:
            b, f_b = c, f_c
        elif f_c * f_b < 0:
            a, f_a = c, f_c
        else:
            break

        if(len(errors) == 3):
            r = calculate_r(errors[0], errors[1], errors[2])
            print(f"{r:.4f}")
            errors.pop(0)
        
        errors.append(error(a,b))

    else:
        print(f"Numero maximo de iteraciones {maxit} alcanzado")

    return c

f = lambda x: log(x) + x

print(biseccion(f, 0.1, 1))