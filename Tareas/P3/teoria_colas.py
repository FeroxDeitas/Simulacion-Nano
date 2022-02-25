from math import ceil, sqrt
from random import shuffle
import multiprocessing
from time import time
from scipy.stats import f_oneway
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

d = 1000
h = 3000
replicas = 20
original = [x for x in range(d, h + 1)]
invertido = original[::-1]
aleatorio = original.copy()
shuffle(aleatorio)
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
    resultados1 = {'Primo 1': [], 'Primo 2': [], 'Primo 3': []}
    with multiprocessing.Pool(processes = cores-1) as pool:
        for r in range(replicas):
            t = time()
            pool.map(primo_1, original)
            resultados1['Primo 1'].append(time()-t)
            t = time()
            pool.map(primo_2, original)
            resultados1['Primo 2'].append(time()-t)
            pool.map(primo_3, original)
            resultados1['Primo 3'].append(time()-t)
    stat1, p1 = f_oneway(resultados1['Primo 1'], resultados1['Primo 2'], \
                         resultados1['Primo 3'])
    print('Variando algoritmo\n', 'stat=%.3f, p=%.3f' % (stat1, p1))
    if p1 > 0.05:
        print('Probably same distribution\n')
    else:
        print('Probably different distribution\n')

if __name__ == "__main__":
    resultados2 = {"ot": [], "it": [], "at": []}
    with multiprocessing.Pool(processes = cores-1) as pool:
        for r in range(replicas):
            t = time()
            pool.map(primo_3, original)
            resultados2["ot"].append(time() - t)
            t = time()
            pool.map(primo_3, invertido)
            resultados2["it"].append(time() - t)
            t = time()
            pool.map(primo_3, aleatorio)
            resultados2["at"].append(time() - t)
    stat2, p2 = f_oneway(resultados2['ot'], resultados2['it'], resultados2['at'])
    print('Variando orden de numeros\n', 'stat=%.3f, p=%.3f' % (stat2, p2))
    if p2 > 0.05:
        print('Probably same distribution\n')
    else:
        print('Probably different distribution\n')

fig, ax1 = plt.subplots()
ax1.violinplot(resultados1, showmeans=True)
plt.show()
