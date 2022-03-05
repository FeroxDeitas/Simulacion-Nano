import seaborn as sns
from math import sqrt
from PIL import Image, ImageColor
from random import randint, choice
import matplotlib.pyplot as plt
 
n = 100
seed = [25, 50, 75, 100, 125]
runs = 200
resultado = []

def creacion():
    semillas = []
    for s in range(k):
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
    for i in range(k):
        (xs, ys) = semillas[i]
        dx, dy = x - xs, y - ys
        dist = sqrt(dx**2 + dy**2)
        if dist < menor:
            cercano, menor = i, dist
    return cercano
 
def inicio():
    direccion = randint(0, 3)
    if direccion == 0:
        return (0, randint(0, n - 1))
    elif direccion == 1:
        return (randint(0, n - 1), 0)
    elif direccion == 2:
        return (randint(0, n - 1), n - 1)
    else:
        return (n - 1, randint(0, n - 1))
 
def propaga_n():
    prob, dificil = 0.9, 0.8
    grieta_n = voronoi.copy()
    g = grieta_n.load()
    (xn, yn) = inicio()
    negro = (0, 0, 0)
    while True:
        g[xn, yn] = negro
        frontera, interior = [], []
        for v in vecinos:
            (dx, dy) = v
            vx, vy = xn + dx, yn + dy
            if vx >= 0 and vx < n and vy >= 0 and vy < n:
               if g[vx, vy] != negro:
                   if vor[vx, vy] == vor[xn, yn]:
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
            break
    return grieta_n

def propaga_b():
    prob, dificil = 0.9, 0.8
    grieta_b = propaga_n()
    g = grieta_b.load()
    (xb, yb) = inicio()
    blanco = (255, 255, 255)
    negro = (0, 0, 0)
    while True:
        g[xb, yb] = blanco
        frontera, interior = [], []
        for v in vecinos:
            (dx, dy) = v
            vx, vy = xb + dx, yb + dy
            if vx >= 0 and vx < n and vy >= 0 and vy < n:
               if g[vx, vy] != blanco:
                   if vor[vx, vy] == vor[xb, yb]:
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
            if g[xb, yb] == negro:
                tocaron.append(1)
                break
        else:
            break
    return grieta_b

for k in seed:
    tocaron = []
    for r in range(runs):
        semillas = creacion()
        celdas = [celda(i) for i in range(n * n)]
        voronoi = Image.new('RGB', (n, n))
        vor = voronoi.load()
        c = sns.color_palette("Set3", k).as_hex()
        for i in range(n * n):
            vor[i % n, i // n] = ImageColor.getrgb(c[celdas.pop(0)])
        limite, vecinos = n, []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    vecinos.append((dx, dy))
        propaga_b()
    pr = (len(tocaron)/runs)*100
    resultado.append(pr)
print(resultado)
plt.bar(x=seed, height=resultado, width=max(seed)/len(seed), color='red',\
        edgecolor='black', tick_label=seed)
plt.xlabel('Semillas')
plt.ylabel('Probabilidad de que toquen (%)')
plt.savefig('Voronoi.png')
plt.show()
