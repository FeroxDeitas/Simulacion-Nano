from math import pi
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

datos = pd.read_csv('DatosReales.txt', delimiter = ' ')

F = (datos.Carga)*(10**-3)#N
d_r = datos.Deformacion
E = 85*(10**9) #Pa
R = 200*(10**-9) #m
g = 300*(10**-3) #J/m2

hertz_list = []
jkr_list = []
diffa = []

def a(F):
    return (((3*R)/(4*E))*(F + 3*g*pi*R + np.sqrt((6*g*pi*R*F) + (3*g*pi*R)**2)))**(1/3)

def d_hertz(F):
    return (((9*(F**2))/(16*(E**2)*R))**(1/3))*(10**9) #nm

def d_jkr(F, a, p1, p2):
    return (((pi*a)/(2*E))*(p1 + 2*p2))*(10**9) #nm

for f in F:
    A = a(f)
    p1 = (2*A*E)/(pi*R)
    p2 = -1 * np.sqrt((2*g*E)/(pi*A))
    hertz = d_hertz(f)
    jkr = d_jkr(f, A, p1, p2)
    hertz_list.append(hertz)
    jkr_list.append(jkr)
    diffa.append(abs(jkr - hertz))

F = datos.Carga

diffb = abs(d_r - hertz_list)
diffc = abs(d_r - jkr_list)

fig = plt.figure(figsize=(7, 3), dpi=1200)
ax = plt.subplot(111)
plt.plot(F, d_r, 'k-', label = 'Experimental')
plt.plot(F, jkr_list, 'g--', label = 'JKR')
plt.xlabel('Carga (mN)')
plt.ylabel('Deformación (nm)')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('pr_e_jkr.png', bbox_inches= 'tight')
plt.close()

fig = plt.figure(figsize=(7, 3), dpi=1200)
ax = plt.subplot(111)
plt.plot(F, d_r, 'k-', label = 'Experimental')
plt.plot(F, hertz_list, 'r--', label = 'Hertz')
plt.xlabel('Carga (mN)')
plt.ylabel('Deformación (nm)')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('pr_e_h.png', bbox_inches= 'tight')
plt.close()

fig = plt.figure(figsize=(7, 3), dpi=1200)
ax = plt.subplot(111)
plt.plot(F, diffa, 'g--')
plt.xlabel('Carga (mN)')
plt.ylabel('Error entre modelo JKR y Hertz (nm)')
plt.savefig('diferencias_jkr_hertz.png', bbox_inches = 'tight')
plt.close()

fig = plt.figure(figsize=(7, 3), dpi=1200)
ax = plt.subplot(111)
plt.plot(F, diffb, 'r--')
plt.xlabel('Carga (mN)')
plt.ylabel('Error entre datos experimentales y Hertz (nm)')
plt.savefig('diferencias_e_h.png', bbox_inches = 'tight')
plt.close()

fig = plt.figure(figsize=(7, 3), dpi=1200)
ax = plt.subplot(111)
plt.plot(F, diffc, 'b--', label = 'Experimental - JKR')
plt.xlabel('Carga (mN)')
plt.ylabel('Error entre datos experimentales y JKR (nm)')
plt.savefig('diferencias_e_jkr.png', bbox_inches = 'tight')
plt.close()
