a = 5.5
b = 89.134
c = -55.5
x = 4
y = -32
z = 65

lista = c(x, y, z)
M = matrix(c(a, b, c, 0), nrow=2)
G = matrix(c(lista, c), nrow=2)
estadistica = summary(lista)
suma = sum(lista)
maximo = max(lista)
minimo = min(lista)
ecuacion = ((suma * maximo) + (minimo**3))


print(lista)
print(suma)
print(maximo)
print(minimo)
print(ecuacion)
print(estadistica)
print(M)
print(G)

for (i in 1:10) {print(i**3)}

while (x < 10) {print("sumo uno");x = x+1}

 
