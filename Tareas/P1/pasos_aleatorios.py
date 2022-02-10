# -*- coding: utf-8 -*-

from random import random, randint, getrandbits
from math import fabs, sqrt
import matplotlib.pyplot as plt
import numpy as np

runs = 30 #replicas
caminatas = [100, 1000, 10000] #pasos
results = [] #almacena las dimensiones
group = [] #almacena grupos de caminatas

for i in range(3):
    dur = caminatas [i]
    for dim in range(1, 6): #de una a cinco dimensiones
        mayores = []
        for rep in range(runs):
            pos = [0] * dim
            mayor = 0
            for paso in range(dur):
                eje = randint(0, dim - 1)
                if random() < 0.5:
                    pos[eje] += 1
                else:
                    pos[eje] -= 1
                mayor = max(mayor, sqrt(sum([p**2 for p in pos])))
            mayores.append(mayor)
        results.append(mayores)
    group.append(results)
#print(results, '\n')
#print('results tiene', len(results), 'elementos\n')
#print(group)
#print('group tiene', len(group), 'elementos\n')

ticks = ['1', '2', '3', '4', '5']

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)

plt.figure()

bpl = plt.boxplot(group[0], positions=np.array(range(len(group[0])))*3.0-0.4, sym='', widths=0.6)
bpc = plt.boxplot(group[1], positions=np.array(range(len(group[1])))*3.0, sym='', widths=0.6)
bpr = plt.boxplot(group[2], positions=np.array(range(len(group[2])))*3.0+0.4, sym='', widths=0.6)
set_box_color(bpl, '#D7191C')
set_box_color(bpc, '#2CB62C')
set_box_color(bpr, '#2C7BB6')

plt.plot([], c='#D7191C', label='100 pasos')
plt.plot([], c='#2CB62C', label='1000 pasos')
plt.plot([], c='#2C7BB6', label='10000 pasos')
plt.legend()

plt.xticks(range(0, len(ticks) * 2, 2), ticks)
plt.xlim(-2, len(ticks)*2)
plt.tight_layout()
#plt.savefig('boxcompare.png')
plt.show()

#fig, ax = plt.subplots()
#ax.boxplot(group[1])
#ax.set_xlabel('Dimension')
#ax.set_ylabel('Distancia maxima')
#ax.set_title('Distancia Euclideana')
#plt.savefig('figuraPy.png')
#plt.show()
