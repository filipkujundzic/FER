#!/usr/bin/python

def ucitaj(lista):
	d = {}
	for i in lista:
		p = list(i)
		v = p.pop()
		tmp = tuple(p)
		d[tmp] = v

	return d


probnalista = []
with open("proba44.txt") as f:
	for line in f:
		pass
		zadnja = line


matirca1 = {}
matrica2 = {}
dimenzije = []

with open("proba44.txt") as f:
	for line in f:
		if(line != '\n'):
			tmp = list(line.strip().split())
			if(len(tmp) > 2):
				probnalista.append(line.strip().split())
			else:
				dimenzije.append(tmp)
		else:
			matrica1 = ucitaj(probnalista)
			probnalista = []
		if(line == zadnja):
			matrica2 = ucitaj(probnalista)
			probnalista = []

print("Matrica 1: ",matrica1)
print("Matrica 2: ",matrica2)

matrica3 = {}

n1 = int(dimenzije[0][0])
m1 = int(dimenzije[0][1])
n2 = int(dimenzije[1][0])
m2 = int(dimenzije[1][1])

if (m1 == n2):
	for i in range(1,n1+1):
		for j in range(1,m2+1):
			suma = 0
			for k in range(1, m1+1):
				suma += int(matrica1.get((str(i),str(k)),0))*int(matrica2.get((str(k),str(j)),0))
			matrica3[i,j] = suma
else:
	print("Matrice nisu ulancane, nije ih moguce mnoziti")

print("Rezultantna matrica:",matrica3)


with open("rezultat.txt", 'w') as out:
	out.write(str(n1)+' '+str(m2)+"\n")
	for i in range(1,n1+1):
		for j in range(1,m2+1):
			if(int(matrica3.get((i,j)) != 0)):
				out.write(str(i)+' ' + str(j) + ' ' + str(matrica3[i,j]) + "\n")
	out.write("\n")
