from math import sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

Fmax = 50
E = 85
R = 200
g = 0.2

F = np.arange(0, Fmax + 0.5, 0.5).tolist()

hertz = []
jkr = []


def a(F):
    return (((3*R)/(4*E))*(F + 6*g*pi*R + sqrt((12*g*pi*R*F) + (6*g*pi*R)**2)))**(1/3)

def d_hertz(F):
    return ((9*(F**2))/(16*(E**2)*R))**(1/3)

def d_jkr(F, a, p1, p2):
    return ((pi*a)/(2*E))*(p1 + 2*p2)

for f in F:
    A = a(f)
    p1 = (2*A*E)/(pi*R)
    p2 = -1 * sqrt((4*g*E)/(pi*A))
    hertz.append(d_hertz(f))
    jkr.append(d_jkr(f, A, p1, p2))
#print('Lista de deformaciones Hertz:\n', hertz)
#print('\nLista de deformaciones JKR:', jkr)

plt.figure(figsize=(7, 3), dpi=1200)
plt.plot(F, hertz)
plt.plot(F, jkr)
plt.xlabel('Carga (mN)')
plt.ylabel('Deformación (nm)')
plt.savefig('proyecto.png', bbox_inches= 'tight')
plt.close()
