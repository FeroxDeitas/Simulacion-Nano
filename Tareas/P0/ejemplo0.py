a = 5.5
b = 89.134
c = -55.5
x = 4
y = -32
z = 65

import numpy as np
from scipy.stats import describe
from numpy.random import rand

lista = [x, y, z]
datos = [a, b, c]
M = np.matrix([lista, datos])
suma = sum(lista)
maximo = max(lista)
minimo = min(lista)
ecuacion = ((suma * maximo) + (minimo**3))
estadistica = describe(lista)
s = np.arange(1, 100, 5)
aleatorio = rand(10)

print(lista)
print(suma)
print(ecuacion)
print(estadistica)
print(M)
print(s)
print(s[-6:])
print(aleatorio)

while y<=0:
    print("sumo uno, ahora y es:", y)
    y+=1
