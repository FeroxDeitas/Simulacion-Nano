from math import exp, pi
import numpy as np
import pandas as pd

pd.options.display.float_format = "{:,.18f}".format

def compare_strings(a, b):
    a = str(a)
    b = str(b)
    
    if a is None or b is None:
        return 0
    
    size = min(len(a), len(b)) # Finding the minimum length
    count = 0 # A counter to keep track of same characters

    for i in range(size):
        if a[i] == b[i]:
            count += 1 # Updating the counter when characters are same at an index
        else:
            break

    return count

def g(x):
    return (2  / (pi * (exp(x) + exp(-x))))

wolfram = 0.048834111126049311
vg = np.vectorize(g)
X = np.arange(-8, 8, 0.05) # ampliar y refinar
Y = vg(X) # mayor eficiencia
 
from GeneralRandom import GeneralRandom
generador = GeneralRandom(np.asarray(X), np.asarray(Y))
desde = 3
hasta = 7
pedazo = 50000
cuantos = [500, 5000, 50000]

def parte(replica):
    V = generador.random(pedazo)[0]
    return ((V >= desde) & (V <= hasta)).sum()
 
import multiprocessing
if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        resultados = {'Absolute': [],
                      'Square': [],
                      'Decimals': []}
        for c in cuantos:
            montecarlo = pool.map(parte, range(c))
            integral = sum(montecarlo) / (c * pedazo)
            valor = (pi / 2) * integral
            ae = abs(valor - wolfram)
            se = ((valor - wolfram)**2)
            dec = compare_strings(wolfram, valor) - 2
            resultados['Absolute'].append(ae)
            resultados['Square'].append(se)
            resultados['Decimals'].append(dec)
        df = pd.DataFrame(resultados, index = cuantos)
        print(df)
