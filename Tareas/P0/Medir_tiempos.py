from random import randint
from time import time
desde = 1
hasta = 1000
menor = 15
mayor = 22
for k in range(menor, mayor + 1):
    n = 2**k
    lista = [ randint(desde, hasta) for i in range(n)]
    antes = time()
    lista.sort()
    despues = time()
    diferencia = despues - antes
    print('ordenar', n, 'elementos toma', diferencia, 'segundos')
print('bye')
