# Analiza i projektiranje racunalom
# 5DZ

import prvadz as dz1
import math
import numpy as np
'''
C = dz1.loadMatrix("A.txt")
print(C)
dz1.print_matrix(C)
'''
def Euler(matrixA, pocetno_stanje, T, t_max, function):
	print("Euler")

	lista_x1 = []
	lista_x2 = []

	lista_x1.append(pocetno_stanje[0][0] + T * calc_x1k(matrixA, pocetno_stanje[0][0], pocetno_stanje[1][0]))
	lista_x2.append(pocetno_stanje[1][0] + T * calc_x2k(matrixA, pocetno_stanje[0][0], pocetno_stanje[1][0]))

	zero = function(T)
	error = abs(zero[0] - lista_x1[0]) + abs(zero[1] - lista_x2[0])

	n_iter = t_max/T

	flag = True
	i = 1
	arg = 0
	while(flag):
		arg += T
		t_max = t_max - T
		if(t_max - T < 0):
			flag = False
			print(i,lista_x1[i - 1], lista_x2[i - 1], error)
			return
		lista_x1.append(lista_x1[i - 1] + T * calc_x1k(matrixA, lista_x1[i - 1], lista_x2[i - 1]))
		lista_x2.append(lista_x2[i - 1] + T * calc_x2k(matrixA, lista_x1[i - 1], lista_x2[i - 1]))
		tmp_f = function(arg)
		error += abs(tmp_f[0] - lista_x1[i]) + abs(tmp_f[1] - lista_x2[i])
		i += 1
		if(i % 100 == 0 and i < n_iter):
			print(i, lista_x1[i - 1], lista_x2[i - 1], error)
		
def RungeKutta4(matrixA, pocetno_stanje, T, t_max, function):
	print("RK4")

	lista_x1 = []
	lista_x2 = []

	lista_x1.append(pocetno_stanje[0][0] + T * calc_x1k(matrixA, pocetno_stanje[0][0], pocetno_stanje[1][0]))
	lista_x2.append(pocetno_stanje[1][0] + T * calc_x2k(matrixA, pocetno_stanje[0][0], pocetno_stanje[1][0]))

	zero = function(T)
	error = abs(zero[0] - lista_x1[0]) + abs(zero[1] - lista_x2[0])

	n_iter = t_max/T
	i = 1
	arg = 0
	while(flag):
		arg += T
		t_max = t_max - T
		if(t_max - T < 0):
			flag = False
			print(i,lista_x1[i - 1], lista_x2[i - 1], error)
			return
		


def calc(matrixA, x1, x2, i):
	if(i == 0):
		return matrixA[0][0] * x1 + matrixA[0][1] * x2
	if(i == 1):
		return matrixA[1][0] * x1 + matrixA[1][1] * x2

def calc_x1k(matrixA, x1, x2):
	return matrixA[0][0] * x1 + matrixA[0][1] * x2

def calc_x2k(matrixA, x1, x2):
	return matrixA[1][0] * x1 + matrixA[1][1] * x2

def mat_njihalo(t):
	rez = []
	rez.append(math.cos(t) + math.sin(t))
	rez.append(math.cos(t) - math.sin(t))
	return rez

def f(A,B,x):
	return np.dot(A,x) + B

def main():
	A = dz1.loadMatrix("A.txt")
	B = dz1.loadMatrix("B.txt")
	x = dz1.loadMatrix("x.txt")

	Euler(A, x, 0.01, 10.0, mat_njihalo)
	#rez2 = RungeKutta4(A, B, x, 0.01, 10.0, f)
	#print(rez2)

main()
