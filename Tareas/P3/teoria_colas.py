from math import ceil, sqrt
from random import shuffle
import multiprocessing
from time import time
from scipy.stats import f_oneway
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

d = 1000
h = 3000
replicas = 20
cores = multiprocessing.cpu_count()

def primo_1(n):
    if n < 3:
        return True
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def primo_2(n):
    if n < 4:
        return True
    if n % 2 == 0:
       return False
    for i in range(3, n - 1, 2):
        if n % i == 0:
            return False
    return True

def primo_3(n):
    if n < 4:
        return True
    if n % 2 == 0:
       return False
    for i in range(3, int(ceil(sqrt(n))), 2):
        if n % i == 0:
            return False
    return True
 
if __name__ == "__main__":
    alg_int = [primo_1, primo_2, primo_3]
    original = [x for x in range(d, h + 1)]
    invertido = original[::-1]
    aleatorio = original.copy()
    shuffle(aleatorio)
    with multiprocessing.Pool(processes = cores-1) as pool:
        for n in alg_int:
            tiempos = {"ot": [], "it": [], "at": []}
            print('El algoritmo es:', n)
            for r in range(replicas):
                t = time()
                pool.map(n, original)
                tiempos["ot"].append(time() - t)
                t = time()
                pool.map(n, invertido)
                tiempos["it"].append(time() - t)
                t = time()
                pool.map(n, aleatorio)
                tiempos["at"].append(time() - t)
            stat, p = f_oneway(tiempos["ot"], tiempos["it"], tiempos["at"])
            print('stat=%.3f, p=%.3f' % (stat, p))
            if p > 0.05:
                print('Probably same distribution')
            else:
                print('Probably different distribution')
