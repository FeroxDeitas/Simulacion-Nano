import matplotlib.colorbar as colorbar
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from random import uniform
from math import cos, sin, floor, log
 
def g(x, y):
    px = (cos(x))**2 + 0.3 * x
    py = (sin(y))**2 - 0.6 * y
    return -(px * py)
 
low = -10
high = -low
step = 0.05
tmax = 10
digitos = floor(log(tmax, 10)) + 1
replicas = 5
curr = [uniform(low, high), uniform(low, high)]
best = curr
print('La posicion inicial es:', best)
print('El valor de la funcion en la posicion inicial es:', g(best[0], best[1]))
p = np.arange(low, high, step)
n = len(p)
print(n)
z = np.zeros((n, n), dtype=float)
for i in range(n):
    x = p[i]
    for j in range(n): 
        y = p[n - j - 1] # voltear
        z[i, j] = g(x, y)
t = range(0, n, 40)
print(t)
l = ['{:.1f}'.format(low + i * step) for i in t]

#for i in range(replicas):
#    curr.append(uniform(low, high), uniform(low, high))

for tiempo in range(tmax):
    dx = uniform(0, 0.3)
    dy = uniform(0, 0.3)
    print('\nLas deltas son:', (dx, dy))
    left = curr[0] - dx
    right = curr[0] + dx
    down = curr[1] - dy
    up = curr[1] + dy
    gl = g(left, curr[1])
    print('El valor de la funcion desplazada hacia la izquierda es:', gl)
    gr = g(right, curr[1])
    print('El valor de la funcion desplazada hacia la derecha es:', gr)
    gd = g(curr[0], down)
    print('El valor de la funcion desplazada hacia abajo es:', gd)
    gu = g(curr[0], up)
    print('El valor de la funcion desplazada hacia arriba es:', gu)
    curr[0] = left if gl < gr else right
    curr[1] = down if gd < gu else up
    if g(curr[0], curr[1]) < g(best[0], best[1]):  # minimizamos
        best = curr
        print('Actualmente el valor minimo de la funcion es:', g(best[0], best[1]))
    fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
    pos = ax.imshow(z)
    ax.axvline(x = best[0], color = 'green')
    ax.axhline(y = best[1], color = 'green')
    ax.scatter(curr[0], curr[1], marker = 'o', color = 'red')
    plt.xticks(t, l)
    plt.yticks(t, l[::-1]) # arriba-abajo
    fig.colorbar(pos, ax=ax)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Paso {:d}'.format(tiempo + 1))
    plt.savefig('p7p_t' + format(tiempo, '0{:d}'.format(digitos)) + '.png')
    plt.close()
print('\nEl valor minimo final de la funcion es:', g(best[0], best[1]))
