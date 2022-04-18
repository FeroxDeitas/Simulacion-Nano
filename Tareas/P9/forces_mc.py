import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colorbar as colorbar
from matplotlib.colors import LinearSegmentedColormap

paso = 256 // 10
niveles = [i/256 for i in range(0, 256, paso)]
colores = [(niveles[i], 0, niveles[-(i + 1)]) for i in range(len(niveles))]
palette = LinearSegmentedColormap.from_list('tonos', colores, N = len(colores))
 
from math import fabs, sqrt, floor, log
eps = 0.001
G = 0.025 #En este universo, la constante gravitacional es 0.025
def fuerza(i, shared):
    p = shared.data
    n = shared.count
    pi = p.iloc[i]
    xi = pi.x
    yi = pi.y
    ci = pi.c
    mi = pi.m
    fx1, fy1 = 0, 0
    fx2, fy2 = 0, 0
    for j in range(n):
        pj = p.iloc[j]
        cj = pj.c
        mj = pj.m
        dire = (-1)**(1 + (ci * cj < 0))
        dx = xi - pj.x
        dy = yi - pj.y
        factor = dire * fabs(ci - cj) / (sqrt(dx**2 + dy**2) + eps)
        factor1 = G * ((mi * mj) / (sqrt(dx**2 + dy**2) + eps))
        fx1 = fx1 - dx * factor
        fy1 = fy1 - dy * factor
        fx2 = fx2 - dx * factor1
        fy2 = fy2 - dy * factor1
    
    fx = fx1 + fx2
    fy = fy1 + fy2
    return (fx, fy)

 
def actualiza(pos, fuerza, de):
    return max(min(pos + de * fuerza, 1), 0)

def velocidad(p, pa):
    ppa = pa.data
    n = pa.count
    for i in range(n):
      p1 = p.iloc[i]
      p2 = ppa.iloc[i]
      x1 = p1.x
      x2 = p2.x
      y1 = p1.y
      y2 = p2.y
      va = p2.v
      v = []
      v.extend(va)
      vel = (sqrt(((x2 - x1)**2) + ((y2 - y1)**2)))
      v.append(vel)
      p['v'][i] = v
    
import multiprocessing
from itertools import repeat

if __name__ == "__main__":
    n = 25
    p = pd.read_csv('values.csv')
    x = p['x']
    y = p['y']
    g = p['g']
    m = p['m']
    c = p['c']
    p['v'] = [[0]]*n
    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    ns.data = p # compartido entre el pool
    ns.count = n 
    tmax = 59
    digitos = floor(log(tmax, 10)) + 1
    fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
    pos = plt.scatter(p.x, p.y, c = p.g, s = (10*m), cmap = palette)
    fig.colorbar(pos, ax=ax)
    plt.title('Estado inicial')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    fig.savefig('p9pmc_t0.png')
    plt.close()

    for t in range(tmax):
        with multiprocessing.Pool() as pool: # rehacer para que vea cambios en p
            f = pool.starmap(fuerza, [(i, ns) for i in range(n)])
            delta = 0.02 / max([max(fabs(fx), fabs(fy)) for (fx, fy) in f])
            p['x'] = pool.starmap(actualiza, zip(p.x, [v[0] for v in f], repeat(delta)))
            p['y'] = pool.starmap(actualiza, zip(p.y, [v[1] for v in f], repeat(delta)))
            velocidad(p, ns)
            fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
            pos = plt.scatter(p.x, p.y, c = p.g, s = (10*m), cmap = palette)
            fig.colorbar(pos, ax=ax)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.xlim(-0.1, 1.1)
            plt.ylim(-0.1, 1.1)            
            plt.title('Paso {:d}'.format(t + 1))
            fig.savefig('p9pmc_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
            plt.close()
            ns.data = p 
    p['v'].to_csv('value_mc.csv')
