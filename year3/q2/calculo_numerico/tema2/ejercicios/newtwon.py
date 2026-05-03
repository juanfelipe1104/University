from math import log

def calculate_r(e1,e2,e3):
    return log(e2/e3)/log(e1/e2)

def newtwon(f, df, x0, tol = 1e-6, maxit = 200):
    x1 = x0
    x2 = x0
    errors = []
    for k in range(maxit):
        x1 = x2
        x2 = x1 - (f(x1)/df(x1))
        error = abs(x2 - x1)

        errors.append(error)
        if len(errors) >= 3:
            r = calculate_r(errors[-3], errors[-2], errors[-1])
            C = errors[2]/(errors[1]**r)
            errors.pop(0)
            print(f"{r} \t\t {C}")

 
        if error < tol:
            return x2
        
        
    return x2

f = lambda x: x**2 - 2

df = lambda x: 2*x

x0 = 1.5

x = newtwon(f, df, x0)

print(x)