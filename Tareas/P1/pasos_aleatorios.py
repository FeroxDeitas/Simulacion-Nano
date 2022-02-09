from random import random, randint, getrandbits
from math import fabs, sqrt
import matplotlib.pyplot as plt

runs = 100 #replicas
dur = 1000 #pasos
results = []
for dim in range(1, 9):
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
fig, ax = plt.subplots()
ax.boxplot(results)
ax.set_xlabel('Dimension')
ax.set_ylabel('Distancia maxima')
ax.set_title('Distancia Euclideana')
plt.savefig('figuraPy.png')
plt.close()
