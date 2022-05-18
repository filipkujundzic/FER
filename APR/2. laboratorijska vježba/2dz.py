# Analiza i projektiranje racunalom
# 2DZ

import dz1 as dz1
from math import *
import numpy as np
import random


k = 0.5 * (sqrt(5) - 1)
epsilon = 1e-6

def zlatni_rez(a, b, function):

	if(len(a) == 1 and len(b) == 1):
		a = a[0]
		b = b[0]

	c = b - k * (b - a)
	d = a + k * (b - a)
	fc = function(transform(c))
	fd = function(transform(d))

	while ((b - a) > epsilon):
		if(fc < fd):
			b = d
			d = c
			c = b - k * (b - a)
			fd = fc
			fc = function(transform(c))
		else:
			a = c
			c = d
			d = a + k * (b - a)
			fc = fd
			fd = function(transform(d))
	return (a + b)/2


def unimodalni(h, tocka, function):
		
	tocka = nptransform(tocka)

	l = tocka - h
	r = tocka + h
	m = tocka
	step = 1

	fm = function(transform(tocka))
	fl = function(transform(l))
	fr = function(transform(r))

	if(fm < fr and fm < fl):
		return l, r
	elif(fm > fr):
		while(fm > fr):
			l = m
			m = r
			fm = fr
			step = step * 2
			r = tocka + h * step
			fr = function(r)
	else:
		while(fm > fl):
			r = m
			m = l
			fm = fl
			step = step * 2
			l = tocka - h * step
			fl = function(transform(l))

	return l, r


def koordinatno(x0, function):

	n = len(x0)
	x = nptransform(x0)
	ei = nptransform([0] * n)

	epsilon = nptransform([1e-6] * n)
	start = []
	flag = True

	while(flag):
		xs = x.copy()
		start.append(xs)
		for i in range(0,n):
			ei[i] = 1

			lmin, rmin = unimodalni(1, xs[i], lambda l : function(x + l * ei))
			l_zlatni = zlatni_rez(transform(lmin), transform(rmin), lambda l : function(x + l * ei))
			x = x + l_zlatni * ei
			ei[i] = 0

		if (all(abs(x - xs) <= epsilon)):
			flag = False

	return x

def istrazi(xp, dx, function):
	n = len(xp)
	x = xp.copy()
	for i in range(0, n):

		P = function(x)
		x[i] = x[i] + dx

		N = function(x)
		if(N > P):
			x[i] = x[i] - 2*dx
			N = function(x)
			if(N > P):
				x[i] = x[i] + dx

	return x			

def reflection(xc, xh):
	alpha = 1
	return (1 + alpha)*xc - alpha*xh

def expansion(xc, xr):
	gamma = 2
	return (1 - gamma) * xc + gamma * xr

def contraction(xc, xh):
	beta = 0.5
	return (1 - beta) * xc + beta * xh

def simplexNM(xstart, function, alpha = 1, shift = 1, beta = 0.5, gamma = 2, sigma = 0.5):

	n = len(xstart)
	x = nptransform([[0]*n]*(n + 1))
	x[0] = nptransform(xstart)

	for i in range(1, n + 1):
		x[i] = nptransform(xstart)
		x[i][i - 1] += shift


	fx = []
	for i in range(0, n + 1):
		t = function(x[i])
		fx.append(t)

	fx = nptransform(fx)

	flag = True
	while(flag):
		h = np.argmax(fx)
		l = np.argmin(fx)


		xc = nptransform([0]*n)
		for i in range(0,n + 1):
			if(i != h):
				xc += x[i]
		xc = xc / n

		fc = function(xc)

		xr = reflection(xc, x[h])
		fr = function(xr)
		if(fr < fx[l]):
			xe = expansion(xc, xr)
			fe = function(xe)
			if(fe < fx[l]):
				x[h] = xe
				fx[h] = fe
			else:
				x[h] = xr
				fx[h] = fr

		else:
			vs = nptransform([fx[j] for j in range(n+1) if j!=h])
			if all(fr > vs):
				if (fr < fx[h]):
					x[h] = xr
					fx[h] = fr
				xk = contraction(xc, x[h])
				fk = function(xk)
				if(fk < fx[h]):
					x[h] = xk
					fx[h] = fk
				else:
					for i in range(0, n +1):
						if(i != l):
							x[i] = sigma * x[i] + (1 - sigma) * x[l]
							fx[i] = function(x[i])
			else:
				x[h] = xr
				fx[h] = fr

		v = 0

		for i in range(0, n + 1):
			v = v + (fx[i] - fc)**2

		v = v/n
		v = sqrt(v)
		if v <= epsilon:
			flag = False


	return x[l]


def HookeJeeves(xstart, function):

	dx = 0.5
	n = len(xstart)
	epsilon = nptransform([1e-6]*n)

	xp = nptransform(xstart)
	xb = nptransform(xstart)

	flag = True
	while (flag):
		xn = istrazi(xp, dx, function)

		if(function(xn) < function(xb)):
			xp = 2*xn - xb
			xb = xn

		else:
			dx = dx / 2
			xp = xb

		if all(dx < epsilon):
			flag = False

	return xb

def transform(z):
	return list([z])

def nptransform(z):
	return np.array(z, dtype=float)


def f1(x):
	broji(f1)

	x1 = x[0]
	x2 = x[1]
	return 100 * (x2 - x1**2)**2 + (1 - x1)**2

def f2(x):
	broji(f2)

	x1 = x[0]
	x2 = x[1]	
	return (x1 - 4)**2 + 4 * (x2 - 2)**2


def f3(x):
	broji(f3)

	i = len(x)
	suma = 0
	for j in range(0, i):
		suma = suma + (x[j] - (j+1))**2
	return suma

def f4(x):
	broji(f4)

	x1 = x[0]
	x2 = x[1]
	return abs((x1 - x2)*(x1 + x2)) + sqrt(x1**2 + x2**2)

def f6(x):
	broji(f6)

	xt = type(x)
	if(xt == float or xt == int):
		sumSquares = x**2
	else:
		sumSquares = 0
		for i in range(len(x)):
			sumSquares += (x[i])**2

	brojnik = (sin(sqrt(sumSquares)))**2-0.5
	nazivnik = (1 + 0.001 * sumSquares)**2

	return 0.5 + brojnik / nazivnik


def broji(function):
	function.count += 1

####################
# 1. ZADATAK 
####################

def zadatak1():

	print("\n1. ZADATAK\n")

	f3.count = 0
	global demo1
	def demo1(xstart,function):
		a, b = unimodalni(1, xstart, function)
		rez = zlatni_rez(transform(a),transform(b),function)
		return rez

	print("Zlatni rez")
	for i in range(10,1000,100):
		f3.count = 0
		y = demo1(transform(i),f3)
		print(f3.count, y[0])

	global demo2	
	def demo2(xstart,function):
		cord = koordinatno(xstart,function)
		return cord

	print("\nKoordinatno")
	for i in range(10,1000,100):
		f3.count = 0
		y = demo2(transform(i),f3)
		print(f3.count, y[0])

	global demo3
	def demo3(xstart,function):
		simpl = simplexNM(xstart,function)
		return simpl

	print("\nSimplex")
	for i in range(10,1000,100):
		f3.count = 0
		y = demo3(transform(i),f3)
		print(f3.count, y[0])

	global demo4
	def demo4(xstart,function):
		hj = HookeJeeves(xstart,function)
		return hj

	print("\nHooke-Jeeves")
	for i in range(10,1000,100):
		f3.count = 0
		y = demo4(transform(i),f3)
		print(f3.count, y[0])
zadatak1()

####################
# 2. ZADATAK 
####################

def zadatak2():
	print("\n2. ZADATAK\n")

	start_points = [[-1.9, 2], [0.1, 0.3], [0, 0, 0, 0, 0, 0, 0], [5.1, 1.1]]
	xmins = [[1, 1], [4, 2], [1, 2, 3, 4, 5, 6, 7], [0, 0]]

	a1, a2, a3 = list(), list(), list()

	print("*Simpleks")
	f1.count = 0
	y = demo3(start_points[0],f1)
	print("funkcija: f1")
	print("start: ", start_points[0])
	print("rješenje: ", xmins[0])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f1.count)
	print("-----------------------------------------")
	f2.count = 0
	y = demo3(start_points[1],f2)
	print("funkcija: f2")
	print("start: ", start_points[1])
	print("rješenje: ", xmins[1])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f2.count)
	print("-----------------------------------------")
	f3.count = 0
	y = demo3(start_points[2],f3)
	print("funkcija: f3")
	print("start: ", start_points[2])
	print("rješenje: ", xmins[2])
	print("izračunato: ", y[0], y[1], y[2], y[3], y[4], y[5], y[6])
	print("broj iteracija algoritma: ",f3.count)
	print("-----------------------------------------")
	f4.count = 0
	y = demo3(start_points[3],f4)
	print("funkcija: f4")
	print("start: ", start_points[3])
	print("rješenje: ", xmins[3])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f4.count)
	print("-----------------------------------------")


	print("\n*Koordinatno")
	f1.count = 0
	y = demo2(start_points[0],f1)
	print("funkcija: f1")
	print("start: ", start_points[0])
	print("rješenje: ", xmins[0])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f1.count)
	print("-----------------------------------------")
	f2.count = 0
	y = demo2(start_points[1],f2)
	print("funkcija: f2")
	print("start: ", start_points[1])
	print("rješenje: ", xmins[1])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f2.count)
	print("-----------------------------------------")
	f3.count = 0
	y = demo2(start_points[2],f3)
	print("funkcija: f3")
	print("start: ", start_points[2])
	print("rješenje: ", xmins[2])
	print("izračunato: ", y[0], y[1], y[2], y[3], y[4], y[5], y[6])
	print("broj iteracija algoritma: ",f3.count)
	print("-----------------------------------------")
	f4.count = 0
	y = demo2(start_points[3],f4)
	print("funkcija: f4")
	print("start: ", start_points[3])
	print("rješenje: ", xmins[3])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f4.count)
	print("-----------------------------------------")


	print("\n*Hooke-Jeeves")
	f1.count = 0
	y = demo4(start_points[0],f1)
	print("funkcija: f1")
	print("start: ", start_points[0])
	print("rješenje: ", xmins[0])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f1.count)
	print("-----------------------------------------")
	f2.count = 0
	y = demo4(start_points[1],f2)
	print("funkcija: f2")
	print("start: ", start_points[1])
	print("rješenje: ", xmins[1])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f2.count)
	print("-----------------------------------------")
	f3.count = 0
	y = demo4(start_points[2],f3)
	print("funkcija: f3")
	print("start: ", start_points[2])
	print("rješenje: ", xmins[2])
	print("izračunato: ", y[0], y[1], y[2], y[3], y[4], y[5], y[6])
	print("broj iteracija algoritma: ",f3.count)
	print("-----------------------------------------")
	f4.count = 0
	y = demo4(start_points[3],f4)
	print("funkcija: f4")
	print("start: ", start_points[3])
	print("rješenje: ", xmins[3])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f4.count)
	print("-----------------------------------------")
zadatak2()

####################
# 3. ZADATAK 
####################

def zadatak3():
	print("\n3. ZADATAK\n")
	print("*Simpleks")
	f4.count = 0
	y = demo3([5,5],f4)
	print("funkcija: f4")
	print("start: ", [5,5])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f4.count)
	print("-----------------------------------------")
	print("\n*Hooke-Jeeves")
	f4.count = 0
	y = demo4([5,5],f4)
	print("funkcija: f4")
	print("start: ", [5,5])
	print("izračunato: ", y[0], y[1])
	print("broj iteracija algoritma: ",f4.count)
	print("-----------------------------------------")
zadatak3()

####################
# 4. ZADATAK 
####################

def zadatak4():
	print("\n4. ZADATAK\n")
	lista1 = list()
	lista2 = list()
	for i in range(1,21):

		f1.count = 0
		y1 = simplexNM([0.5, 0.5], f1, shift = i)
		tmp_count = f1.count

		f1.count = 0
		y2 = simplexNM([20, 20], f1, shift = i)

		print(i, tmp_count, y1, f1.count, y2)
zadatak4()


####################
# 5. ZADATAK 
####################

def zadatak5():
	print("\n5. ZADATAK\n")

	counter = 0
	for i in range(0, 1000):
		a = random.randrange(-50,50)
		b = random.randrange(-50,50)

		f6.count = 0
		y = demo3([a,b],f6) 

		if all(y < 1e-4):
			counter = counter + 1

	print("Counter: " + str(counter))
	print("postotak: ", (counter/1000), '%\n')

zadatak5()