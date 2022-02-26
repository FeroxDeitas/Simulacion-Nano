from math import ceil, sqrt
from random import shuffle
import multiprocessing
from time import time
from scipy.stats import f_oneway
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

d = 1000
h = 5000
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
    resultados = {'Primo 1': [], 'Primo 2': [], 'Primo 3': [], \
                   'Original': [], 'Invertido': [], 'Aleatorio': []}
    with multiprocessing.Pool(processes = cores-1) as pool:
        for r in range(replicas):
            t = (time()*1000)
            pool.map(primo_1, original)
            resultados['Primo 1'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_2, original)
            resultados['Primo 2'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_3, original)
            resultados['Primo 3'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_3, original)
            resultados['Original'].append((time()*1000) - t)
            t = (time()*1000)
            pool.map(primo_3, invertido)
            resultados['Invertido'].append((time()*1000) - t)
            t = (time()*1000)
            pool.map(primo_3, aleatorio)
            resultados['Aleatorio'].append((time()*1000) - t)
    df = pd.DataFrame(data = resultados)
    print(df)
    stat1, p1 = f_oneway(resultados['Primo 1'], resultados['Primo 2'], \
                         resultados['Primo 3'])
    print('Variando algoritmo\n', 'stat=%.3f, p=%.3f' % (stat1, p1))
    if p1 > 0.05:
        print('Estadísticamente no significativa\n')
    else:
        print('Estadísticamente significativa\n')
    stat2, p2 = f_oneway(resultados['Original'], resultados['Invertido'], \
                         resultados['Aleatorio'])
    print('Variando orden de numeros\n', 'stat=%.3f, p=%.3f' % (stat1, p1))
    if p1 > 0.05:
        print('Estadísticamente no significativa\n')
    else:
        print('Estadísticamente significativa\n')
    
    sns.violinplot(data = df, cut = 0, scale = 'count')
    plt.show()
