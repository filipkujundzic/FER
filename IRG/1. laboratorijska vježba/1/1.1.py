#!/usr/bin/env python3
import numpy

a = numpy.array([2,3,-4])
b = numpy.array([-1,4,-1])

print("\n*Zbrajanje:")
v1 = a + b
print("v1 = {} + {}".format(a,b))
print("v1 = {}".format(v1))

print("\n*Mnozenje:")
s = v1 * b
print("s = {} * {}".format(v1, b))
print("s = {}".format(s))

print("\n*Vektorski produkt:")
v2 = numpy.cross(v1,numpy.array([2,2,4]))
print("v2 = {} x {}".format(v1, numpy.array([2,2,4])))
print("v2 = {}".format(v2))

print("\n*Normiranje")
v3 = numpy.sqrt((v2*v2).sum())
print("v3 = |{}|".format(v2))
print("v3 = {}".format(v3))

print("\n*Vektor suprotnog smjera:")
v4 = -v2
print("v4 = -v2")
print("v4 = {}".format(v4))

print("\n*Zbrajanje matrica:")
m1 = numpy.matrix(((1,2,3),(2,1,3),(4,5,1)))
print(m1)
print()
m2 = numpy.matrix(((-1,2,-3),(5,-2,7),(-4,-1,3)))
print(m2)
print()
M1 = m1 + m2
print("Rezultat = Matrica M1:")
print(M1)

print("\n*Umnozak matrice i transponirane matrice:")
print("\nprva matrica:")
print(m1)
m3 = numpy.matrix(((-1,2,-3),(5,-2,7),(-4,-1,3)))
print("\ndruga matrica:")
print(m3)
print("\ntransponirana druga matrica:")
print(m3.transpose())
print("\nNjihov umnozak:")
M2 = m1 * m3.transpose()
print(M2)

print("\n*Umnozak matrice i neke invertirane matrice:")
print("prva matrica:")
print(m1)
print("\ndruga matrica:")
print(m3)
print("\ninvertirana druga matrica:")
print(m3.I)
print("\nNjihov umnozak:")
M3 = m1 * m3.I
print(M3)