import numpy as np
import pandas as pd
from math import sqrt
from random import random, choice
 
m = 7
vx = (2 * (np.random.uniform(size = m) < 0.5) - 1) * np.random.uniform(low = 0.01, high = 0.04, size = m)
vy = (2 * (np.random.uniform(size = m) < 0.5) - 1) * np.random.uniform(low = 0.01, high = 0.04, size = m)
x = np.random.uniform(size = m)
y = np.random.uniform(size = m)
r = np.random.uniform(low = 0.05, high = 0.1, size = m)
bolas = pd.DataFrame({'x': x, 'y': y, 'dx': vx, 'dy': vy, 'r': r})
n = 50
vx = (2 * (np.random.uniform(size = n) < 0.5) - 1) * np.random.uniform(low = 0.02, high = 0.05, size = n)
vy = (2 * (np.random.uniform(size = n) < 0.5) - 1) * np.random.uniform(low = 0.02, high = 0.05, size = n)
x = np.random.uniform(size = n)
y = np.random.uniform(size = n)
print(x)
r = np.random.uniform(low = 0.01, high = 0.03, size = n)
particulas = pd.DataFrame({'x': x, 'y': y, 'dx': vx, 'dy': vy, 'r': r, 'v': [1] * n, 'a': [1] * n})
for t in range(25):
    
    for i in range(n):
        p = particulas.iloc[i]
        v = p.v
        
        if v > 0:
            pr = p.r
            px = p.x
            py = p.y
            conteo = 0
            for k in range(m):
                pk = bolas.iloc[k]
                pkr = pk.r
                pkx = pk.x
                pky = pk.y
                dx = px - pkx
                dy = py - pky
                dr = pkr + pr
                d = sqrt(dx**2 + dy**2)
                if d < dr:
                    conteo += 1
            if conteo >= 2:
                conteo2 = 0
                for j in range(n):
                    if i != j:
                        pj = particulas.iloc[j]
                        pjr = pj.r
                        pjx = pj.x
                        pjy = pj.y
                        dx = px - pjx
                        dy = py - pjy
                        dr = pjr + pr
                        d = sqrt(dx**2 + dy**2)
                        if d < dr: # Unir particulas
                            conteo2 += 1
                            a1 = np.pi * (pr**2)
                            a2 = np.pi * (pjr**2)
                            a = a1 + a2
                            rt = sqrt(a/np.pi)
                            particulas.at[i, 'r'] = rt
                            particulas.at[j, 'v'] = -1
                if conteo2 == 0: # Romper particulas
                    v = random()
                    v1 = 1 - v
                    vx1 = p.dx * -1
                    vy1 = p.dy * -1
                    a = np.pi * (pr**2)
                    a1 = a * v
                    a2 = a * v1
                    r1 = sqrt(a1/np.pi)
                    r2 = sqrt(a2/np.pi)
                    particulas.at[i, 'r'] = r1
                    particulas = particulas.append({'x': px, 'y': py, 'dx': vx1, 'dy': vy1, 'r': r2, 'v': 1, 'a': 1}, ignore_index=True)

                    
    particulas = particulas.loc[particulas['v'] > 0] # se eliminan las que no existen
    n = particulas.shape[0]
    particulas.to_csv('p_part_{:d}.dat'.format(t), header = False, index = False)
    bolas.to_csv('p_bola_{:d}.dat'.format(t), header = False, index = False)
    for i in range(m):
        b = bolas.iloc[i]
        br = b.r
        bx = b.x
        by = b.y
        vx = b.dx
        vy = b.dy
        x = bx + vx
        y = by + vy
        if 0 >= (x-br):
            x = 0 + br
            bolas.at[i, 'dx'] = vx * -1
        elif (x+br) >= 1:
            x = 1 - br
            bolas.at[i, 'dx'] = vx * -1
        if 0 >= (y-br):
            y = 0 + br
            bolas.at[i, 'dy'] = vy * -1
        elif (y+br) >= 1:
            y = 1 - br
            bolas.at[i, 'dy'] = vy * -1
        
        bolas.at[i, 'x'] = x
        bolas.at[i, 'y'] = y
        

    for i in range(n):
        b = particulas.iloc[i]
        br = b.r
        bx = b.x
        by = b.y
        vx = b.dx
        vy = b.dy
        x = bx + vx
        y = by + vy
        if 0 >= (x-br):
            x = 0 + br
            particulas.at[i, 'dx'] = vx * -1
        elif (x+br) >= 1:
            x = 1 - br
            particulas.at[i, 'dx'] = vx * -1
        if 0 >= (y-br):
            y = 0 + br
            particulas.at[i, 'dy'] = vy * -1
        elif (y+br) >= 1:
            y = 1 - br
            particulas.at[i, 'dy'] = vy * -1
        
        particulas.at[i, 'x'] = x
        particulas.at[i, 'y'] = y
