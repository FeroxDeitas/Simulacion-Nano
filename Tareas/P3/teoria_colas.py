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
replicas = 30
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
    resultados_1 = {'Algoritmo 1': [], 'Algoritmo 2': [], 'Algoritmo 3': []}              
    resultados_2 = {'Original': [], 'Invertido': [], 'Aleatorio': []}
    with multiprocessing.Pool(processes = cores-1) as pool:
        pool.map(primo_1, original)
        for r in range(replicas):
            t = (time()*1000)
            pool.map(primo_1, original)
            resultados_1['Algoritmo 1'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_2, original)
            resultados_1['Algoritmo 2'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_3, original)
            resultados_1['Algoritmo 3'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_3, original)
            resultados_2['Original'].append((time()*1000) - t)
            t = (time()*1000)
            pool.map(primo_3, invertido)
            resultados_2['Invertido'].append((time()*1000) - t)
            t = (time()*1000)
            pool.map(primo_3, aleatorio)
            resultados_2['Aleatorio'].append((time()*1000) - t)
    df1 = pd.DataFrame(data = resultados_1)
    df2 = pd.DataFrame(data = resultados_2)
    print(df1, '\n', df2)
    stat1, p1 = f_oneway(resultados_1['Algoritmo 1'],
                         resultados_1['Algoritmo 2'],
                         resultados_1['Algoritmo 3'])
    print('Variando algoritmo\n', 'stat=%.3f, p=%.3f' % (stat1, p1))
    if p1 > 0.05:
        print('Estadísticamente no significativa\n')
    else:
        print('Estadísticamente significativa\n')
    stat2, p2 = f_oneway(resultados_2['Original'],
                         resultados_2['Invertido'],
                         resultados_2['Aleatorio'])
    print('Variando orden de numeros\n', 'stat=%.3f, p=%.3f' % (stat1, p1))
    if p1 > 0.05:
        print('Estadísticamente no significativa\n')
    else:
        print('Estadísticamente significativa\n')
    
    sns.violinplot(data = df1, scale='count')
    plt.savefig('AlgorithmVariation.png')
    plt.show()
    sns.violinplot(data = df2, scale='count')
    plt.savefig('OrderVariation.png')
    plt.show()
