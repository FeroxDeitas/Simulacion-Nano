import numpy as np
from random import random
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

dim = [10, 15, 20] #matrix sizes
p = [0.2, 0.4, 0.6, 0.8] #initial life density
runs = 30 #replicas of the experiment
dur = 50 #iterations
#seq = 0
datos = pd.DataFrame()
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
        for rep in range(runs): #starts 30 replicas
            viven = 0
            valores = [1 * (random() < densidad) for i in range(num)] #generates initial seed
            actual = np.reshape(valores, (lado, lado)) #reshapes initial seed 'valores' into array 'actual'
            assert all([mapeo(x) == valores[x]  for x in range(num)])
            for iteracion in range(dur): #starts iteration of cell automata, 50 steps
                valores = [paso(y) for y in range(num)] #defines new 'valores' list according to neighbor = 3 rule from 'paso'
                actual = np.reshape(valores, (lado, lado)) #reshapes the new 'valores' list into new 'actual' array
            print(lado, densidad, rep, iteracion, f'actual: {actual}')
            resultado = { 'Tamaño': lado,
                      'P' : densidad,
                      'Viven': np.sum(actual) > 3}
            datos = datos.append(resultado, ignore_index=True)
print(datos)
#fig = plt.figure()
#plt.imshow(actual, interpolation='nearest', cmap=cm.Greys)
#fig.suptitle('Estado inicial')
#plt.savefig('p2_t0_p.png')
#plt.close()

    #fig = plt.figure()
    #plt.imshow(actual, interpolation='nearest', cmap=cm.Greys)
    #fig.suptitle('Paso {:d}'.format(iteracion + 1))
    #plt.savefig('p2_t{:d}_p.png'.format(seq))
    #seq += 1
    #plt.close()
