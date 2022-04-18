import pandas as pd
import re
import matplotlib.pyplot as plt


p = pd.read_csv('value_mc.csv')
v = (p['v'])
vmc = v
for x in range(len(p['v'])):
    numbers = [float(s) for s in re.findall(r'-?\d+\.?\d*', v[x])]
    vmc[x] = numbers[1:]

p = pd.read_csv('value_c.csv')
v = (p['v'])
vc = v
for x in range(len(p['v'])):
    numbers = [float(s) for s in re.findall(r'-?\d+\.?\d*', v[x])]
    vc[x] = numbers[1:]

p = pd.read_csv('value_m.csv')
v = (p['v'])
vm = v
for x in range(len(p['v'])):
    numbers = [float(s) for s in re.findall(r'-?\d+\.?\d*', v[x])]
    vm[x] = numbers[1:]

xt = [x for x in range(5,len(vmc)+1,5)]
medianprops = dict(linestyle='solid', linewidth=3, color='red')
plt.boxplot(vmc,medianprops=medianprops, showfliers=False)

plt.ylabel('Velocidad')
plt.xticks(xt, xt)
plt.xlabel('Partículas')
plt.savefig('p9pmc.png', dpi=300)
plt.show()
plt.close()

plt.boxplot(vc,medianprops=medianprops, showfliers=False)

plt.ylabel('Velocidad')
plt.xticks(xt, xt)
plt.xlabel('Partículas')
plt.savefig('p9pc.png', dpi=300)
plt.show()
plt.close()

plt.boxplot(vm,medianprops=medianprops, showfliers=False)

plt.ylabel('Velocidad')
plt.xticks(xt, xt)
plt.xlabel('Partículas')
plt.savefig('p9pm.png', dpi=300)
plt.show()
plt.close()
