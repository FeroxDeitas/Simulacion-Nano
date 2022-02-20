import numpy as np
from random import random
import matplotlib.pyplot as plt
import pandas as pd

dim = [10, 15, 20] #matrix sizes
p = [0.2, 0.4, 0.6, 0.8] #initial life density
runs = 30 #replicas of the experiment
dur = 200 #iterations
vivieron = []

def mapeo(pos):
    fila = pos // lado
    columna = pos % lado
    return actual[fila, columna]

def paso(pos):
    fila = pos // lado
    columna = pos % lado
    vecindad = actual[max(0, fila - 1):min(lado, fila + 2),
                      max(0, columna - 1):min(lado, columna + 2)]
    return 1 * (np.sum(vecindad) - actual[fila, columna] == 3)

for lado in dim: #defines matrix size
    num = lado**2
    for densidad in p: #defines initial life density
        contador_viv=0
        for rep in range(runs): #starts 30 replicas
            valores = [1 * (random() < densidad) for i in range(num)] #generates initial seed
            actual = np.reshape(valores, (lado, lado)) #reshapes initial seed 'valores' into array 'actual'
            assert all([mapeo(x) == valores[x]  for x in range(num)])
            for iteracion in range(dur): #starts iteration of cell automata, 50 iterations
                valores = [paso(y) for y in range(num)] #defines new 'valores' list according to neighbor = 3 rule from 'paso'
                vivos = sum(valores)
                if vivos == 0:
                    break;
                if iteracion == (dur-1):
                    contador_viv += 1
                actual = np.reshape(valores, (lado, lado)) #reshapes the new 'valores' list into new 'actual' array
            #print(lado, densidad, rep, iteracion, f'actual: {actual}')
        print(contador_viv)
        contador_viv = ((contador_viv*100)/(rep+1))
        print('contador vivos:', contador_viv)
        vivieron.append(contador_viv)
print('lista de porcentajes de vivos:', vivieron)

P02 = vivieron[0:3]
P04 = vivieron[3:6]
P06 = vivieron[6:9]
P08 = vivieron[9:12]

sep = np.arange(3)

plt.plot(sep, P02, label = '0.2')
plt.scatter(sep, P02)
plt.plot(sep, P04, label = '0.4')
plt.scatter(sep, P04)
plt.plot(sep, P06 ,label='0.6')
plt.scatter(sep, P06)
plt.plot(sep, P08, label='0.8')
plt.scatter(sep, P08)
plt.xticks(sep , ('10', '15', '20'))
plt.ylabel('Supervivencia (%)')
plt.xlabel('Tamaño de matriz')
plt.title('Autómata Celular')
plt.legend(title='P inicial')
plt.savefig('Porcentaje.png')
plt.show()
