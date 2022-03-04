import seaborn as sns
from math import sqrt
from scipy.stats import describe
from PIL import Image, ImageColor
from random import randint, choice
 
size = [80, 90, 100]
seed = 50
runs = 5

def creacion():
    semillas = []
    for s in range(seed):
        while True:
            x, y = randint(0, n - 1), randint(0, n - 1)
            if (x, y) not in semillas:
                semillas.append((x, y))
                break
    return semillas

def celda(pos):
    if pos in semillas:
        return semillas.index(pos)
    x, y = pos % n, pos // n
    cercano = None
    menor = n * sqrt(2)
    for i in range(seed):
        (xs, ys) = semillas[i]
        dx, dy = x - xs, y - ys
        dist = sqrt(dx**2 + dy**2)
        if dist < menor:
            cercano, menor = i, dist
    return cercano
 
def inicio():
    direccion = randint(0, 3)
    if direccion == 0: # vertical abajo -> arriba
        return (0, randint(0, n - 1))
    elif direccion == 1: # izq. -> der
        return (randint(0, n - 1), 0)
    elif direccion == 2: # der. -> izq.
        return (randint(0, n - 1), n - 1)
    else:
        return (n - 1, randint(0, n - 1))
 
def propaga_n():
    prob, dificil = 0.9, 0.8
    grieta_n = voronoi.copy()
    g = grieta_n.load()
    (xn, yn) = inicio()
    largo_n = 0
    negro = (0, 0, 0)
    while True:
        g[xn, yn] = negro
        largo_n += 1
        frontera, interior = [], []
        for v in vecinos:
            (dx, dy) = v
            vx, vy = xn + dx, yn + dy
            if vx >= 0 and vx < n and vy >= 0 and vy < n: # existe
               if g[vx, vy] != negro: # no tiene grieta por el momento
                   if vor[vx, vy] == vor[xn, yn]: # misma celda
                       interior.append(v)
                   else:
                       frontera.append(v)
        elegido = None
        if len(frontera) > 0:
            elegido = choice(frontera)
            prob = 1
        elif len(interior) > 0:
            elegido = choice(interior)
            prob *= dificil
        if elegido is not None:
            (dx, dy) = elegido
            xn, yn = xn + dx, yn + dy
        else:
            break # ya no se propaga
    print('Largo de grieta negra:', largo_n)
    return grieta_n

def propaga_b():
    prob, dificil = 0.9, 0.8
    grieta_b = propaga_n()
    g = grieta_b.load()
    (xb, yb) = inicio()
    largo_b = 0
    blanco = (255, 255, 255)
    while True:
        g[xb, yb] = blanco
        largo_b += 1
        frontera, interior = [], []
        for v in vecinos:
            (dx, dy) = v
            vx, vy = xb + dx, yb + dy
            if vx >= 0 and vx < n and vy >= 0 and vy < n: # existe
               if g[vx, vy] != blanco: # no tiene grieta por el momento
                   if vor[vx, vy] == vor[xb, yb]: # misma celda
                       interior.append(v)
                   else:
                       frontera.append(v)
        elegido = None
        if len(frontera) > 0:
            elegido = choice(frontera)
            prob = 1
        elif len(interior) > 0:
            elegido = choice(interior)
            prob *= dificil
        if elegido is not None:
            (dx, dy) = elegido
            xb, yb = xb + dx, yb + dy
        else:
            break # ya no se propaga
    print('Largo de grieta blanca:', largo_b)
    return grieta_b

for n in size:
    for r in range(runs):
        semillas = creacion()
        celdas = [celda(i) for i in range(n * n)]
        voronoi = Image.new('RGB', (n, n))
        vor = voronoi.load()
        c = sns.color_palette("Set3", seed).as_hex()
        for i in range(n * n):
            vor[i % n, i // n] = ImageColor.getrgb(c[celdas.pop(0)])
        limite, vecinos = n, []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    vecinos.append((dx, dy))
        visual = propaga_b().resize((10 * n,10 * n))
        visual.save("p4pgbn_{:d}_{:d}.png".format(n, r))
