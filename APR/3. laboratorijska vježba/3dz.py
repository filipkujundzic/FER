# Analiza i projektiranje racunalom
# 3DZ

import numpy as np
from math import *
import numpy.linalg as l
from random import random
from functools import partial

k = 0.5 * (sqrt(5) - 1)
epsilon = 1e-6
shift=1
alpha=1
beta=0.5
gamma=2
sigma=0.5


def nptransform(z):
	return np.array(z, dtype=float)

def transform(z):
	return list([z])	

def makeMatrix(dataset):
	return nptransform(dataset)

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

def reflection(xc, xh):
	alpha = 1
	return (1 + alpha)*xc - alpha*xh

def expansion(xc, xr):
	gamma = 2
	return (1 - gamma) * xc + gamma * xr

def contraction(xc, xh):
	beta = 0.5
	return (1 - beta) * xc + beta * xh

def simplexNelderMead(function, x0):
    
    n = len(x0)
    x = nptransform([[0]*n]*(n+1))
    x[0] = nptransform(x0)
    for i in range(1, n+1):
        x[i] = nptransform(x0)
        x[i][i-1] += shift

    fx = nptransform([function(x[i]) for i in range(n+1)])

    flag = True
    while flag:

        h = np.argmax(fx)
        l = np.argmin(fx)

        xc = nptransform([0]*n)
        for i in range(n+1):
            if (i != h):
                xc += x[i]
        xc /= n

        fc = function(xc)

        xr = reflection(xc, x[h])
        fr = function(xr)
        if (fr < fx[l]):
            xe = expansion(xc, xr)
            fe = function(xe)
            if (fe < fx[l]):
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
                if (fk < fx[h]):
                    x[h] = xk
                    fx[h] = fk
                else:
                    for i in range(n+1):
                        if (i != l):
                            x[i] = sigma*(x[l] + x[i])
                            fx[i] = function(x[i])

            else:
                x[h] = xr
                fx[h] = fr

        v = 0
        for i in range(n+1):
            v += (fx[i]-fc)**2

        v /= n
        v = sqrt(v)

        if (v <= epsilon):
            flag = False

    return x[l]

def broji(function):
	function.count += 1

def f1(x):
	broji(f1)

	x1 = x[0]
	x2 = x[1]
	return 100 * (x2 - x1**2)**2 + (1 - x1)**2

def gradient_f1(x):
	broji(gradient_f1)

	x1 = x[0]
	x2 = x[1]

	gradient = list()
	gradient.append(-400 * x1 * (x2 - x1**2) - 2 * (1 - x1))
	gradient.append(200 * (x2 - x1**2))
	return gradient

def hf1(x):
    x1 = x[0]
    x2 = x[1]
    hessian = list()
    hessian.append([1200 * x1**2 - 400 * x2 + 2, -400 * x1])
    hessian.append([-400 * x1, 200])
    return hessian

def f1u1(x):
    x1, x2 = x[0], x[1]
    return x2-x1
    
def f1u2(x):
    x1 = x[0]
    return 2-x1

def f2(x):
	broji(f2)

	x1 = x[0]
	x2 = x[1]	
	return (x1 - 4)**2 + 4 * (x2 - 2)**2

def gradient_f2(x):

    x1 = x[0]
    x2 = x[1]

    gradient = list()
    gradient.append(2 * x1 - 8)
    gradient.append(8 * x2 - 16)
    return gradient


def hf2(x):

    x1 = x[0]
    x2 = x[1]

    hessian = list()
    hessian.append([2, 0])
    hessian.append([0, 8])
    return hessian

def f3(x):

	broji(f3)


	x1 = x[0]
	x2 = x[1]
	return (x1 - 2)**2 + (x2 + 3)**2


def gradient_f3(x):
	broji(gradient_f3)

	x1 = x[0]
	x2 = x[1]

	gradient = list()
	gradient.append(2 * x1 - 4)
	gradient.append(2 * x2 + 6)
	return gradient


def hf3(x):
    return [[2, 0], [0, 2]]

def f4(x):
	broji(f4)

	x1 = x[0]
	x2 = x[1]
	return (x1 - 3)**2 + (x2)**2

def f4u1(x):
    x1, x2 = x[0], x[1]
    return 3 - x1 - x2
    
def f4u2(x):
    x1, x2 = x[0], x[1]
    return 3 + 1.5 * x1 - x2
    
def f4h1(x):
    x2 = x[1]
    return x2 - 1


def gradijentni(function, grad_function, xstart, opt = 0):

    n = len(xstart)
    x = nptransform(xstart)
    minf = None
    count = 0
    while(True):
    
        if (count >= 100):
            print('Divergence!')
            break

        grad = nptransform(grad_function(x))
        if np.linalg.norm(grad) < epsilon:
            break
        
        v = -1 * grad
        l_min = 1
        if (opt == 1):
        		v = v  / np.linalg.norm(v)
        		for i in range(0,n):
        			lmin, rmin = unimodalni(1, xstart[i], lambda l : function(x + l * v))
        			l_zlatni = zlatni_rez(transform(lmin), transform(rmin), lambda l : function(x + l * v))
        			l_min = l_zlatni       

        x = x + l_min * v
        
        fx = function(x)
        if minf == None:
            minf = fx
        elif fx < minf:
            minf = fx
            count = 0
        else:
            count += 1

    return x

def newtonRaphson(function, grad_function, hess_function, xstart, opt = 0):

    n = len(xstart)
    x = nptransform(xstart)

    minf = None
    count = 0
    while(True):
    
        if count >= 100:
            print('Divergence!')
            break
    
        grad = nptransform(grad_function(x))
        hess_inv = l.inv(makeMatrix(hess_function(x)))
        v = -1 * np.dot(hess_inv, grad)
        l_min = 1

        if (opt == 1):
            v = v  / np.linalg.norm(v)
            for i in range(0,n):
	            lmin, rmin = unimodalni(1, xstart[i], lambda l : function(x + l * v))
	            l_zlatni = zlatni_rez(transform(lmin), transform(rmin), lambda l : function(x + l * v))
	            l_min = l_zlatni

        if np.linalg.norm(l_min * v) < epsilon:
            break

        x = x + l_min * v
            
        fx = function(x)
        if minf == None:
            minf = fx
        elif fx < minf:
            minf = fx
            count = 0
        else:
            count+=1
            
    return x

def box(function, xstart, xDonja, xGornja, g, alpha=2):
	
	if not ((all(nptransform([xDonja]*2) <= xstart) and all(xstart <= nptransform([xGornja]*2)))):
		return

	if not(all(nptransform(g(xstart))) >= 0):
		return

	x0 = nptransform(xstart)
	Xc = xstart
	n = xstart.shape[0]
	X = np.random.uniform(xDonja, xGornja, size=[2*n, n])

	for i in range(2*n):
		while np.any(g(X[i]) < 0):
			X[i] = 0.5 * (X[i] + Xc)

	while np.mean(np.linalg.norm(X - Xc, axis=0)) > epsilon:
		y = nptransform([function(x) for x in X])
		hh = np.argsort(y)
		h = hh[-1]
		h2 = hh[-2]
		Xc = np.mean(X[hh[:-1]], axis=0)

		Xr = (1 + alpha)*Xc - alpha*X[h]
		Xr = np.clip(Xr, xDonja, xGornja)

		while np.any(g(Xr) < 0):
			Xr = 0.5 * (Xr + Xc)

		while function(Xr) > y[h2]:
			Xr = 0.5 * (Xr + Xc)

		X[h] = Xr
	return Xc

def transf_problem(function, xstart, alg, hs, gs, t = 1):
    
    n = len(xstart)
    
    def G(t, x):
        sum2 = 0
        for i, g in enumerate(gs):
            if g(x)>=0:
                pass
            else:
                sum2 -= t[i] * g(x)
                
        return sum2
                
    x = alg(partial(G, [10]*len(gs)), xstart)

    print(x)

    if not all([g(x)>=0 for g in gs]):
        print('problem wiht x0')
        return None
    
    prev_x = nptransform(xstart)

    epsilon = nptransform([1e-6]*n)
        
    def U(t, x):
        sum2 = function(x)
        
        for g in gs:
            if (g(x)>=0):
                pass
            else:
                sum2 += 1e6
                
        for h in hs:
            sum2 += t * h(x)**2
            
        return sum2
         
    minf = None
    count = 0
    while(True):
    
        if (count >= 100):
            print('Divergence!')
            break
    
        curr_x = alg(partial(U, t), prev_x)
        if all([abs(curr_x[i]-prev_x[i])<epsilon[i] for i in range(n)]):
            break;
        
        fx = U(t, curr_x)
        t *= 10
        
        if (minf == None):
            minf = fx
        elif (fx < minf):
            minf = fx
            count = 0
        else:
            count+=1
        
        
    return curr_x


####################
# 1. ZADATAK 
####################

def zadatak1():
	print("\n1. ZADATAK\n")

	print("Bez određivanja optimalnog iznosa koraka:\n")

	f3.count = 0
	gradient_f3.count = 0
	y = gradijentni(f3, gradient_f3, [0,0])

	print("Broj poziva funkcije: " + str(f3.count))
	print("Broj poziva gradijenta: " + str(gradient_f3.count))
	print("Interval: " + str(y))
	print("Vrijednost f(y): " + str(f3(y)))

	print("\nUz određivanje optimalnog iznosa koraka:\n")

	f3.count = 0
	gradient_f3.count = 0
	y = gradijentni(f3, gradient_f3, [0,0], opt = 1)

	print("Broj poziva funkcije: " + str(f3.count))
	print("Broj poziva gradijenta: " + str(gradient_f3.count))
	print("Interval: " + str(y))
	print("Vrijednost f(y): " + str(f3(y)))

zadatak1()


####################
# 2. ZADATAK 
####################

def zadatak2():
	print("\n2. ZADATAK\n")

	print("Gradijentni i Newton-Raphson za f1 i f2 uz određivanje optimalnog koraka\n")
	print("Funkcija 1 - gradijentni -> xmin[1,1]")

	f1.count = 0
	gradient_f1.count = 0
	y = gradijentni(f1, gradient_f1, [-1.9,2], opt = 1)

	print("Broj poziva funkcije: " + str(round(f1.count/2)))
	print("Broj poziva gradijenta: " + str(gradient_f1.count))
	print("Interval: " + str(y))
	print("Vrijednost f(y): " + str(f1(y)))

	print("\nFunkcija 1 - Newton-Raphson  -> xmin[1,1]")
	f1.count = 0
	gradient_f1.count = 0
	y = newtonRaphson(f1, gradient_f1, hf1, [-1.9,2], opt = 1)

	print("Broj poziva funkcije: " + str(round(f1.count/2)))
	print("Broj poziva gradijenta: " + str(gradient_f1.count))
	print("Interval: " + str(y))
	print("Vrijednost f(y): " + str(f1(y)))

	print("\nFunkcija 2 - gradijentni -> xmin[4,2]")

	f2.count = 0
	gradient_f2.count = 0
	y = gradijentni(f2, gradient_f2, [0.1,0.3], opt = 1)

	print("Broj poziva funkcije: " + str(round(f2.count/2)))
	print("Broj poziva gradijenta: " + str(gradient_f1.count))
	print("Interval: " + str(y))
	print("Vrijednost f(y): " + str(f2(y)))

	print("\nFunkcija 2 - Newton-Raphson  -> xmin[4,2]")
	f2.count = 0
	gradient_f2.count = 0
	y = newtonRaphson(f2, gradient_f2, hf2, [0.1,0.3], opt = 1)

	print("Broj poziva funkcije: " + str(round(f2.count/2)))
	print("Broj poziva gradijenta: " + str(gradient_f2.count))
	print("Interval: " + str(y))
	print("Vrijednost f(y): " + str(f2(y)))

zadatak2()

####################
# 3. ZADATAK 
####################

def zadatak3():
	print("\n3. ZADATAK\n")
	print("Postupak po Boxu s ograničenjima - funkcija 1 - min[1,1]")
	x = nptransform([1.9,2])

	f1.count = 0
	y = box(f1, x , -100,100, lambda x:nptransform([x[1] - x[0], 2 - x[0]]))
	print(y)

	print("Postupak po Boxu s ograničenjima - funkcija 2 - min[4,2]")
	x = np.array([0.1, 0.3])
	f2.count = 0
	y = box(f2, x , -100,100, lambda x:nptransform([x[1] - x[0], 2 - x[0]]))
	print(y)

zadatak3()

####################
# 4. ZADATAK 
####################

def zadatak4():
	print("\n4. ZADATAK\n")

	x = (-1.9, 2)
	# min = (1, 1)

	print("Transformacija u problem bez ograničenja uz postupak simpleks - funkcija 1 - min[1,1]")
	y = transf_problem(f1, x, alg = simplexNelderMead, hs=[], gs=[f1u1, f1u2])
	print(y, f1(y))

	print("Transformacija u problem bez ograničenja uz postupak simpleks - funkcija 2 - min[4,2]")
	x = (0.1, 0.3)
	y = transf_problem(f2, x, alg=simplexNelderMead, hs=[], gs=[f1u1, f1u2])
	print(y, f2(y))

zadatak4()

####################
# 5. ZADATAK 
####################

def zadatak5():
	print("\n5. ZADATAK\n")

	x = (0, 0)
	# min = (3, 0)
	print("Transformacija u problem bez ograničenja uz postupak simpleks - funkcija 4 -  min (3,0)")

	f4.count = 0
	y = transf_problem(f4, x, alg=simplexNelderMead, hs=[f4h1], gs=[f4u1, f4u2])
	print(y, f4(y))

	
	x = (5, 5)
	f4.count = 0
	y = transf_problem(f4, x, alg=simplexNelderMead, hs=[f4h1], gs=[f4u1, f4u2])
	print(y, f4(y))
	print()
	

zadatak5()