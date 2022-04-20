import pandas as pd
import re
from scipy.stats import f_oneway

df1 = pd.read_csv('value_mc.csv')
df2 = pd.read_csv('value_m.csv')
df3 = pd.read_csv('value_c.csv')

v1 = df1.loc[24, 'v']
v2 = df2.loc[24, 'v']
v3 = df3.loc[24, 'v']

n1 = [float(s) for s in re.findall(r'-?\d+\.?\d*', v1)]
n2 = [float(s) for s in re.findall(r'-?\d+\.?\d*', v2)]
n3 = [float(s) for s in re.findall(r'-?\d+\.?\d*', v3)]


print('######### Analisis Estadistico #########')
stat, p = f_oneway(n1, n2, n3)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Estadísticamente no significativa')
else:
	print('Estadísticamente significativa')
