import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from random import randint, random
from math import exp, floor, log
from numpy.random import shuffle
from scipy.stats import f_oneway

 
clusters = [2500, 5000, 10000]
particles = [250000, 500000, 1000000]
filtersize = 100
runs = 100
dur = 50
digitos = floor(log(dur, 10)) + 1
 
def rotura(x, c, d):
    return 1 / (1 + exp((c - x) / d))
 
def union(x, c):
    return exp(-x / c)
 
def romperse(tam, cuantos):
    if tam == 1:
        return [tam] * cuantos
    res = []
    for cumulo in range(cuantos):
        if random() < rotura(tam, c, d):
            primera = randint(1, tam - 1)
            segunda = tam - primera
            assert primera > 0
            assert segunda > 0
            assert primera + segunda == tam
            res += [primera, segunda]
        else:
            res.append(tam)
    assert sum(res) == tam * cuantos
    return res
 
def unirse(tam, cuantos):
    res = []
    for cumulo in range(cuantos):
        if random() < union(tam, c):
            res.append(-tam)
        else:
            res.append(tam)
    return res

guardar = 0

for k in clusters:
    resultados = pd.DataFrame()
    for n in particles:
        filtrados = []
        for r in range(runs):
            filtro = 0
            orig = np.random.normal(size = k)
            cumulos = orig - min(orig)
            cumulos += 1
            cumulos = cumulos / sum(cumulos)
            cumulos *= n
            cumulos = np.round(cumulos).astype(int)
            diferencia = n - sum(cumulos)
            cambio = 1 if diferencia > 0 else -1
            while diferencia != 0:
                p = randint(0, k - 1)
                if cambio > 0 or (cambio < 0 and cumulos[p] > 0):
                    cumulos[p] += cambio
                    diferencia -= cambio
            assert all(cumulos != 0)
            assert sum(cumulos) == n

            c = np.median(cumulos)
            d = np.std(cumulos) / 4
            
            for paso in range(dur):
                assert sum(cumulos) == n
                assert all([c > 0 for c in cumulos]) 
                (tams, freqs) = np.unique(cumulos, return_counts = True)
                cumulos = []
                assert len(tams) == len(freqs)
                for i in range(len(tams)):
                    cumulos += romperse(tams[i], freqs[i]) 
                assert sum(cumulos) == n
                assert all([c > 0 for c in cumulos]) 
                (tams, freqs) = np.unique(cumulos, return_counts = True)
                cumulos = []
                assert len(tams) == len(freqs)
                for i in range(len(tams)):
                    cumulos += unirse(tams[i], freqs[i])
                cumulos = np.asarray(cumulos)
                neg = cumulos < 0
                a = len(cumulos)
                juntarse = -1 * np.extract(neg, cumulos)
                cumulos = np.extract(~neg, cumulos).tolist()
                assert a == len(juntarse) + len(cumulos)
                nt = len(juntarse)
                if nt > 1:
                    shuffle(juntarse)
                j = juntarse.tolist()
                while len(j) > 1:
                    cumulos.append(j.pop(0) + j.pop(0))
                if len(j) > 0:
                    cumulos.append(j.pop(0))
                assert len(j) == 0
                assert sum(cumulos) == n
                assert all([c != 0 for c in cumulos])

                if guardar == 0:
                    cortes = np.arange(min(cumulos), max(cumulos), 50)
                    plt.hist(cumulos, bins = cortes, align = 'right', density = True)
                    plt.xlabel('Tamaño')
                    plt.ylabel('Frecuencia relativa')
                    plt.ylim(0, 0.05)
                    plt.title('Paso {:d} con ambos fenómenos'.format(paso + 1))
                    plt.savefig('p8p_ct' + format(paso, '0{:d}'.format(digitos)) + '.png')
                    plt.close()

            guardar = 1

            for p in cumulos:
                if p >= filtersize:
                    filtro += 1
            porcentaje = (filtro / sum(cumulos)) * 100
            filtrados.append(porcentaje)

        resultados['n: ' + str(n) + ', k: ' + str(k)] = pd.DataFrame(filtrados)
    
    resultados.to_csv('urnas_{:d}.csv'.format(k))

res1 = pd.read_csv('urnas_2500.csv', usecols=['n: 250000, k: 2500',
                                               'n: 500000, k: 2500',
                                               'n: 1000000, k: 2500'])
porc11 = res1['n: 250000, k: 2500']
porc12 = res1['n: 500000, k: 2500']
porc13 = res1['n: 1000000, k: 2500']

res2 = pd.read_csv('urnas_5000.csv', usecols=['n: 250000, k: 5000',
                                               'n: 500000, k: 5000',
                                               'n: 1000000, k: 5000'])
porc21 = res2['n: 250000, k: 5000']
porc22 = res2['n: 500000, k: 5000']
porc23 = res2['n: 1000000, k: 5000']

res3 = pd.read_csv('urnas_10000.csv', usecols=['n: 250000, k: 10000',
                                               'n: 500000, k: 10000',
                                               'n: 1000000, k: 10000'])
porc31 = res3['n: 250000, k: 10000']
porc32 = res3['n: 500000, k: 10000']
porc33 = res3['n: 1000000, k: 10000']

print('######### k = 2500 #########')
stat1, p1 = f_oneway(porc11, porc12, porc13)
print('stat=%.3f, p=%.3f' % (stat1, p1))
if p1 > 0.05:
	print('Estadísticamente no significativa')
else:
	print('Estadísticamente significativa')

print('######### k = 5000 #########')
stat2, p2 = f_oneway(porc21, porc22, porc23)
print('stat=%.3f, p=%.3f' % (stat2, p2))
if p2 > 0.05:
	print('Estadísticamente no significativa')
else:
	print('Estadísticamente significativa')

print('######### k = 10000 #########')
stat3, p3 = f_oneway(porc31, porc32, porc33)
print('stat=%.3f, p=%.3f' % (stat3, p3))
if p3 > 0.05:
	print('Estadísticamente no significativa')
else:
	print('Estadísticamente significativa')

sns.violinplot(data=res1, scale='area')
plt.xlabel('Relación n:k')
plt.ylabel('Porcentaje de cúmulos filtrados (%)')
plt.savefig('Porcentajes_2500.png')
plt.close()

sns.violinplot(data=res2, scale='area')
plt.xlabel('Relación n:k')
plt.ylabel('Porcentaje de cúmulos filtrados (%)')
plt.savefig('Porcentajes_5000.png')
plt.close()

sns.violinplot(data=res3, scale='area')
plt.xlabel('Relación n:k')
plt.ylabel('Porcentaje de cúmulos filtrados (%)')
plt.savefig('Porcentajes_10000.png')
plt.close()
