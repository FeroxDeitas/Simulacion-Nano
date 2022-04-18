import numpy as np
import pandas as pd

n = 25
x = np.random.normal(size = n)
y = np.random.normal(size = n)
c = np.random.normal(size = n)
m = np.random.normal(size = n)
xmax = max(x)
xmin = min(x)
x = (x - xmin) / (xmax - xmin) # de 0 a 1
ymax = max(y)
ymin = min(y)
y = (y - ymin) / (ymax - ymin) 
cmax = max(c)
cmin = min(c)
c = 2 * (c - cmin) / (cmax - cmin) - 1 # entre -1 y 1
mmax = max(m)
mmin = min(m)
m = 10 * ((m - mmin) / (mmax - mmin) + 0.1)
m = np.round(m).astype(int)
v = [[0]]*n
g = np.round(5 * c).astype(int)
p = pd.DataFrame({'x': x, 'y': y, 'c': c, 'm':m, 'g':g, 'v':v})
p.to_csv('values.csv')
