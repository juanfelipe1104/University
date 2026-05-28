import math

class Dual:
    """
    Número dual a + b·d con d^2 = 0.

    Atributos:
        value : parte real, valor f(x).
        deriv : parte dual, valor f'(x).
    """

    def __init__(self, value, deriv):
        self.value = value
        self.deriv = deriv

    def __add__(self, other: Dual):
        return Dual(self.value + other.value, self.deriv + other.deriv)

    def __sub__(self, other: Dual):
        return Dual(self.value - other.value, self.deriv - other.deriv)

    def __mul__(self, other: Dual):
        return Dual(
            self.value * other.value,
            self.value * other.deriv + self.deriv * other.value
        )

    def __truediv__(self, other: Dual):
        return Dual(
            self.value / other.value,
            (self.deriv * other.value - self.value * other.deriv) / (other.value**2)
        )


def sin(d: Dual):
    return Dual(math.sin(d.value), math.cos(d.value)*d.deriv)


def cos(d: Dual):
    return Dual(math.cos(d.value), -math.sin(d.value)*d.deriv)


def exp(d: Dual):
    return Dual(math.exp(d.value), math.exp(d.value)*d.deriv)


# Apartado b)

x = Dual(0.5, 1)
dos = Dual(2, 0)

# y = f(x) = e^sin(2x)

y = exp(sin(dos * x))

print("Dual")
print(f"f(x): {y.value}")
print(f"f'(x): {y.deriv}")

# Apartado c)

# f'(x) = e^sin(2x) * cos(2x) * 2

derivada_exacta = math.exp(math.sin(2*x.value)) * math.cos(2*x.value) * 2

error = abs(y.deriv - derivada_exacta)

print()
print(f"Derivada exacta: {derivada_exacta}")
print(f"Derivada dual: {y.deriv}")
print(f"Error: {error}")