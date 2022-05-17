#!/usr/bin/env python3
import sys
import numpy

print("Unesite podatke o sustavu jednadzbi:")
lines = sys.stdin.readline().split()

a = 1
prva = []
druga = []
pomocni = []
for i in lines:
	if(i != " "):
		if(a % 4 == 0 and a != 1):
			druga.append(float(i))
			tuple(pomocni)
			prva.append(pomocni)
			pomocni = []
		else:
			pomocni.append(float(i))
		a+=1

a = numpy.array(prva)
b = numpy.array(druga)

print("[x y z] = ",numpy.linalg.solve(a,b))