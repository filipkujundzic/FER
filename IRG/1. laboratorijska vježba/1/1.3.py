#!/usr/bin/env python3
import sys
import numpy


print("Unesite podatke:")
i = input("Koordinate točke A: ")
a = list(map(int, i.split()))

i = input("Koordinate točke B: ")
b = list(map(int, i.split()))

i = input("Koordinate točke C: ")
c = list(map(int, i.split()))

i = input("Koordinate točke T: ")
t = list(map(int, i.split()))

matrica = []
for i in range(3):
	pomocni = []
	pomocni.append(a[i])
	pomocni.append(b[i])
	pomocni.append(c[i])
	matrica.append(pomocni)


matrica = numpy.matrix(matrica)
rjesenje = list(t)

d = numpy.linalg.det(matrica)
if (d > 0):
	print("[t1 t2 t3] = ",numpy.linalg.solve(matrica,rjesenje))
else:
	print("matrica je singularna, nije ju moguće invertirati, det(matrica) = 0")