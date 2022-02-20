import numpy as np
from random import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

dim = [10, 15, 20, 25] #matrix sizes
p = [0.2, 0.4, 0.6, 0.8] #initial life density
runs = 30 #replicas of the experiment
dur = 200 #iterations
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

for lado in dim:
    num = lado**2
    for densidad in p:
        contador_viv=0
        for rep in range(runs):
            valores = [1 * (random() < densidad) for i in range(num)]
            actual = np.reshape(valores, (lado, lado))
            assert all([mapeo(x) == valores[x]  for x in range(num)])
            for iteracion in range(dur):
                valores = [paso(y) for y in range(num)]
                vivos = sum(valores)
                if vivos == 0:
                    break;
                if iteracion == (dur-1):
                    contador_viv += 1
                actual = np.reshape(valores, (lado, lado))
        vivieron = ((contador_viv*100)/(runs))
        resultados = {'Tamaño matriz': lado,
                      'P inicial': densidad,
                      'Porcentaje Supervivencia(%)': vivieron}
        datos = datos.append(resultados, ignore_index=True)
sns.lineplot(data=datos, x='Tamaño matriz', y='Porcentaje Supervivencia(%)',\
             hue='P inicial', palette='Set2')
plt.title('Autómata Celular')
plt.savefig('CellularAutomata.png')
plt.show()
