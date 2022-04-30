import numpy as np
import pandas as pd
from random import random, randint, sample
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import expon

def knapsack(peso_permitido, pesos, valores):
    assert len(pesos) == len(valores)
    peso_total = sum(pesos)
    valor_total = sum(valores)
    if peso_total < peso_permitido: 
        return valor_total
    else:
        V = dict()
        for w in range(peso_permitido + 1):
            V[(w, 0)] = 0
        for i in range(len(pesos)):
            peso = pesos[i]
            valor = valores[i]
            for w in range(peso_permitido + 1):
                cand = V.get((w - peso, i), -float('inf')) + valor
                V[(w, i + 1)] = max(V[(w, i)], cand)
        return max(V.values())
 
def factible(seleccion, pesos, capacidad):
    return np.inner(seleccion, pesos) <= capacidad
  
def objetivo(seleccion, valores):
    return np.inner(seleccion, valores)
 
def normalizar(data):
    menor = min(data)
    mayor = max(data)
    rango  = mayor - menor
    data = data - menor # > 0
    return data / rango # entre 0 y 1
  
def generador_pesos2(valores, low, high):
    cant = 1 / valores
    return np.round(((normalizar(cant))) * (high - low) + low)
 
def generador_valores2(pesos, low, high):
    cant = np.arange(0, pesos)  
    return np.round(normalizar(expon.pdf(cant))  * (high - low) + low)
 
def poblacion_inicial(n, tam):
    pobl = np.zeros((tam, n))
    for i in range(tam):
        pobl[i] = (np.round(np.random.uniform(size = n))).astype(int)
    return pobl
 
def mutacion(sol, n):
    pos = randint(0, n - 1)
    mut = np.copy(sol)
    mut[pos] = 1 if sol[pos] == 0 else 0
    return mut
  
def reproduccion(x, y, n):
    pos = randint(2, n - 2)
    xy = np.concatenate([x[:pos], y[pos:]])
    yx = np.concatenate([y[:pos], x[pos:]])
    return (xy, yx)
 
n = 100
tmax = 150
iteraciones = 20

#####Combinacion 1#####

pm, rep, init = 0.05, 50, 100
resultados1 = []


for runs in range(iteraciones):
    valores = generador_valores2(n, 10, 500)
    pesos = generador_pesos2(valores, 15, 80)
    capacidad = int(round(sum(pesos) * 0.65))
    optimo = knapsack(capacidad, pesos, valores)
    p = poblacion_inicial(n, init)
    tam = p.shape[0]
    assert tam == init
    mejor = None
    mejores = []
    for t in range(tmax):
        for i in range(tam): # mutarse con probabilidad pm
            if random() < pm:
                p = np.vstack([p, mutacion(p[i], n)])
        for i in range(rep):  # reproducciones
            padres = sample(range(tam), 2)
            hijos = reproduccion(p[padres[0]], p[padres[1]], n)
            p = np.vstack([p, hijos[0], hijos[1]])
        tam = p.shape[0]
        d = []
        for i in range(tam):
            d.append({'idx': i, 'obj': objetivo(p[i], valores),
                      'fact': factible(p[i], pesos, capacidad)})
        d = pd.DataFrame(d).sort_values(by = ['fact', 'obj'], ascending = False)
        mantener = np.array(d.idx[:init])
        p = p[mantener, :]
        tam = p.shape[0]
        assert tam == init
        factibles = d.loc[d.fact == True,]
        mejor = max(factibles.obj)
        mejores.append(mejor)
    resultados1.append((optimo - mejor) / optimo)

    if runs == 0:
        plt.figure(figsize=(7, 3), dpi=300)
        plt.plot(range(tmax), mejores, 'ks--', linewidth=1, markersize=5)
        plt.axhline(y = optimo, color = 'green', linewidth=3)
        plt.xlabel('Paso')
        plt.ylabel('Mayor valor')
        plt.ylim(0.95 * min(mejores), 1.05 * optimo)
        plt.savefig('p10p_I2_C1.png', bbox_inches='tight') 
        plt.close()
        print(optimo, mejor, (optimo - mejor) / optimo)
print('\nMejores Resultados de Combinacion 1: ', resultados1)

#####Combinacion 2#####

pm, rep, init = 0.1, 100, 50
resultados2 = []

for runs in range(iteraciones):
    valores = generador_valores2(n, 10, 500)
    pesos = generador_pesos2(valores, 15, 80)
    capacidad = int(round(sum(pesos) * 0.65))
    optimo = knapsack(capacidad, pesos, valores)
    p = poblacion_inicial(n, init)
    tam = p.shape[0]
    assert tam == init
    mejor = None
    mejores = []
    for t in range(tmax):
        for i in range(tam): # mutarse con probabilidad pm
            if random() < pm:
                p = np.vstack([p, mutacion(p[i], n)])
        for i in range(rep):  # reproducciones
            padres = sample(range(tam), 2)
            hijos = reproduccion(p[padres[0]], p[padres[1]], n)
            p = np.vstack([p, hijos[0], hijos[1]])
        tam = p.shape[0]
        d = []
        for i in range(tam):
            d.append({'idx': i, 'obj': objetivo(p[i], valores),
                      'fact': factible(p[i], pesos, capacidad)})
        d = pd.DataFrame(d).sort_values(by = ['fact', 'obj'], ascending = False)
        mantener = np.array(d.idx[:init])
        p = p[mantener, :]
        tam = p.shape[0]
        assert tam == init
        factibles = d.loc[d.fact == True,]
        mejor = max(factibles.obj)
        mejores.append(mejor)
    resultados2.append((optimo - mejor) / optimo)

    if runs == 0:
        plt.figure(figsize=(7, 3), dpi=300)
        plt.plot(range(tmax), mejores, 'ks--', linewidth=1, markersize=5)
        plt.axhline(y = optimo, color = 'green', linewidth=3)
        plt.xlabel('Paso')
        plt.ylabel('Mayor valor')
        plt.ylim(0.95 * min(mejores), 1.05 * optimo)
        plt.savefig('p10p_I2_C2.png', bbox_inches='tight') 
        plt.close()
        print(optimo, mejor, (optimo - mejor) / optimo)
print('\nMejores Resultados de Combinacion 2: ', resultados2)

df  = pd.DataFrame({'Combinación 1': resultados1, 'Combinación 2': resultados2})
print(df)

sns.violinplot(data=df)
plt.ylabel('Proporción')
plt.savefig('p10p_I2.png', bbox_inches='tight')
plt.close
