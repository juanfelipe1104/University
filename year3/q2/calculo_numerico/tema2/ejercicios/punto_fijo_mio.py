from math import sqrt, log

def calculate_r(e1,e2,e3):
    return log(e2/e3)/log(e1/e2)

def fixed_point(g, x0, tol=1e-6, max_iter=200, verbose=False):
    x = x0
    errors = []
    for i in range(max_iter):
        x_next = g(x)
        if verbose:
            print(f"Iteration: {i}. x: {x_next}")
        error = abs(x_next - x)
        if error < tol:
            return x_next, i + 1, True
        x = x_next
        errors.append(error)
        if len(errors) >= 3:
            r = calculate_r(errors[-3], errors[-2], errors[-1])
            print(f"{r:.6f}")
            errors.pop(0)
        
    return x, max_iter, False

f = lambda x: x**2 - x - 1
x0 = 1.5

g_1 = lambda x: x**2 - 1
g_2 = lambda x: sqrt(x+1)
g_3 = lambda x: 1 + 1/x
g_4 = lambda x: x - f(x)/(2*x - 1)

g_s = [g_1, g_2, g_3, g_4]

fixed_point_found, max_iter, reachedMaxIter = fixed_point(g_4, x0, verbose=False)

if not reachedMaxIter:
    print(f"Reached max_iter: {max_iter}. Aprox: {fixed_point_found}")
else:
    print(f"Found fixed point: {fixed_point_found} in iteration: {max_iter}")
