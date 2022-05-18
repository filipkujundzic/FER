# Analiza i projektiranje racunalom
# 4DZ

import random as r
from random import randint
import numpy as np
import math
import numpy.random as npr
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

def nptransform(z):
	return np.array(z, dtype=float)

def broji(function):
	function.count += 1

def f1(x):
	broji(f1)

	x1 = x[0]
	x2 = x[1]
	return 100 * (x2 - x1**2)**2 + (1 - x1)**2

def f3(x):
	broji(f3)

	i = len(x)
	suma = 0
	for j in range(0, i):
		suma = suma + (x[j] - (j+1))**2
	return suma

def f6(x):
	broji(f6)

	xt = type(x)
	if(xt == float or xt == int):
		sumSquares = x**2
	else:
		sumSquares = 0
		for i in range(len(x)):
			sumSquares += (x[i])**2

	brojnik = (math.sin(math.sqrt(sumSquares)))**2-0.5
	nazivnik = (1 + 0.001 * sumSquares)**2

	return 0.5 + brojnik / nazivnik


def f7(x):
	broji(f7)

	x1 = np.sum(np.square(x))
	return x1**0.25 * (1 + np.sin(50 * x1**0.1)**2)

def f(x):
	return x**2

def fqad(x):
	x1 = x[0]
	x2 = x[1]

	return x1**2 + x2**2

def aritmeticko_krizanje(kromosom1, kromosom2, vj_krizanja):
	nova_jedinka = []
	for i in range(0, len(kromosom1)):
		D = vj_krizanja * kromosom1[i] + (1 - vj_krizanja) * kromosom2[i]
		nova_jedinka.append(D)
	nova_jedinka_np = nptransform(nova_jedinka)
	return nova_jedinka_np

def heuristicko_krizanje(kromosom1, kromosom2, vj_krizanja, donja_granica, gornja_granica, funkcija):
	
	nova_jedinka = []
	kromosom1_eval = funkcija(kromosom1)
	kromosom2_eval = funkcija(kromosom2)
	if(abs(kromosom1_eval) <= abs(kromosom2_eval)):
		x2 = kromosom1
		x1 = kromosom2
	else:
		x2 = kromosom2
		x1 = kromosom1
	for i in range(0, len(kromosom1)):
			vj1 = r.uniform(0, 1)
			D = vj1 * (x2[i] - x1[i]) + x2[i]
			#print(D)
			if(D >= donja_granica and D <= gornja_granica):
				D = np.clip(D, donja_granica, gornja_granica)
			nova_jedinka.append(D)
	nova_jedinka_np = nptransform(nova_jedinka)
	return nova_jedinka_np

def mutacija_pz(kromosom, vjerojatnost, donja_granica, gornja_granica):

	broj = r.uniform(0,1)
	dodaj = r.uniform(donja_granica/2, gornja_granica/2)

	mutirani = []
	for i in range(0,len(kromosom)):
		if(broj > vjerojatnost):
			if(kromosom[i] + dodaj >= donja_granica and kromosom[i] + dodaj <= gornja_granica):
				kromosom[i] = kromosom[i] + dodaj
			else:
				kromosom[i] = kromosom[i] - dodaj
			mutirani.append(kromosom[i])
		else:
			mutirani.append(kromosom[i])

	return mutirani

def dekoder(b, donja_granica, gornja_granica, broj_bitova):
	x = donja_granica + b*(gornja_granica - donja_granica)/(2**broj_bitova - 1)
	return x

def single_point_crossover(kromosom1, kromosom2, preciznost, vj_krizanja, stupanj_populacije):

	kromosom1 = kromosom1.tolist()
	kromosom2 = kromosom2.tolist()

	p = r.randint(0,preciznost-1-1)

	nova_jedinka = []
	for i in range(0, stupanj_populacije):
		x = r.uniform(0,1)
		p = r.randint(0,preciznost-1-1)
		if(x < vj_krizanja):
			nova_jedinka.append(kromosom1[i][0:(p+1)] + kromosom2[i][(p+1):])
		else:
			o = r.randint(0,1)
			if(o == 0):
				return kromosom1
			else:
				return kromosom2

	nova_jedinka = nptransform(nova_jedinka)
	return nova_jedinka

def xor_f(a,b):
	if(a == b):
		return 0
	else:
		return 1

def uniform_crossover(kromosom1, kromosom2, preciznost, vj_krizanja,stupanj_populacije):
	#R = np.random.randint(2, size = [preciznost])
	#R1 = np.random.randint(2, size = [preciznost])

	nova_jedinka = []
	for i in range(0, stupanj_populacije):
		tmp = []
		for j in range(0, preciznost):
			R = np.random.randint(2, size = [preciznost])
			#R1 = np.random.randint(2, size = [preciznost])
			z = r.uniform(0,1)
			if(z < vj_krizanja):
				tmp.append(kromosom1[i][j]*kromosom2[i][j] + R[i] * xor_f(kromosom1[i][j], kromosom2[i][j]))
			else:
				o = r.randint(0,1)
				if(o == 0):
					return kromosom1
				else: 
					return kromosom2
		nova_jedinka.append(tmp)
	nova_jedinka = nptransform(nova_jedinka)
	return nova_jedinka


def uniform_mutation(kromosom, preciznost,vj_mutacije, stupanj_populacije):
	mutirana_jedinka = []
	#print(kromosom)
	for i in range(0, stupanj_populacije):
		tmp = []
		for j in range(0, preciznost):
			p = r.uniform(0,1)
			if(p < vj_mutacije):
				tmp.append(1 - kromosom[i][j])
			else:
				tmp.append(kromosom[i][j])
		mutirana_jedinka.append(tmp)

	return mutirana_jedinka
 
def pretvori(jedinka,preciznost,donja_granica,gornja_granica,stupanj_populacije):
	evaluirano = []
	for i in range(0, stupanj_populacije):
		vrijednost = 0
		broj_bitova = preciznost - 1 
		for j in range(0, preciznost):
			vrijednost += jedinka[i][j] * (2**broj_bitova)
			broj_bitova = broj_bitova - 1
			a = dekoder(vrijednost, donja_granica, gornja_granica, preciznost)
		evaluirano.append(a)
	return evaluirano

def turnirski(donja_granica, gornja_granica, velicina_populacije, prikaz_rj, vj_mutacije, vj_krizanja, broj_evaluacija, stupanj_populacije, funkcija, binarna_preciznost, ispis = 0, turnir = 3):

	if(prikaz_rj == 1):
		preciznost = np.int(math.log(np.floor(1 + (gornja_granica - donja_granica) * (10**binarna_preciznost)),10)/math.log(2,10))


	if(prikaz_rj == 0):
		populacija = []
		for i in range(0, velicina_populacije):
			tmp_lst = []
			for j in range(0, stupanj_populacije):	
				tmp = r.randint(donja_granica,gornja_granica)
				tmp_lst.append(tmp)
			populacija.append(tmp_lst)

	if(prikaz_rj == 1):
		populacija = []
		for i in range(0, velicina_populacije):
			tmp = []
			for j in range(0, stupanj_populacije):
				populacija_b = np.random.randint(2, size = [preciznost])
				tmp.append(populacija_b)
			populacija.append(tmp)

	if(prikaz_rj == 0):
		populacija = nptransform(populacija)

		populacija_eval = []
		for i in range(0, len(populacija)):
			populacija_eval.append(funkcija(populacija[i]))
		populacija_eval = nptransform(populacija_eval)

	if(prikaz_rj == 1):
		populacija = nptransform(populacija)
		
		populacija_bin_transf = []
		for i in range(0, velicina_populacije):
			
			tmp = []
			for j in range(0, stupanj_populacije):
				vrijednost = 0
				broj_bitova = preciznost - 1 
				for k in range(0, preciznost):
					vrijednost += populacija[i][j][k] * (2**broj_bitova)
					broj_bitova = broj_bitova - 1
				tmp.append(vrijednost)
			populacija_bin_transf.append(tmp)

		populacija_eval_middle = []
		for i in range(0, len(populacija_bin_transf)):
			tmp = []
			for j in range(0, stupanj_populacije):
				a = dekoder(populacija_bin_transf[i][j], donja_granica, gornja_granica, preciznost)
				tmp.append(a)
			populacija_eval_middle.append(tmp)
		populacija_eval_middle = nptransform(populacija_eval_middle)

		populacija_eval = []
		for i in range(0, len(populacija_eval_middle)):
			populacija_eval.append(funkcija(populacija_eval_middle[i]))

		populacija_eval = nptransform(populacija_eval)


	broji_eval = 0
	while True:

		broji_eval = broji_eval + 1
		if(broji_eval > broj_evaluacija):
			break

		k = 0
		najbolja = populacija_eval[0]
		for i in range(1, len(populacija_eval)):
			if(populacija_eval[i] < najbolja):
				najbolja = populacija_eval[i]
				k = i

		if(ispis == 0):
			print(funkcija.count, populacija[k], najbolja)
		if(ispis == 1):
			if(abs(najbolja) - 0 < 1e-6 or funkcija.count >= broj_evaluacija):
				print(funkcija.count)
		if(ispis == 2):
			if(abs(najbolja) - 0 < 1e-6 or funkcija.count >= broj_evaluacija):
				return najbolja


		if(abs(najbolja) - 0 < 1e-6):
			break

		if(funkcija.count >= broj_evaluacija):
			break

		for p in range(0, len(populacija)):
			
			h = len(populacija)
			turnir_arg = turnir

			uzorci = r.sample(range(0, h), turnir_arg)

			if(prikaz_rj == 0):
				populacija_eval = nptransform(populacija_eval)

			slucajne = []
			for i in uzorci:
				slucajne.append(populacija[i])

			slucajne_eval = []
			for i in uzorci:
				slucajne_eval.append(populacija_eval[i])

			a = max(slucajne_eval, key = abs)
			indeks_najlosije = slucajne_eval.index(a)

			var = slucajne[indeks_najlosije]

			#print(var)
			populacija = populacija.tolist()

			populacija_eval = populacija_eval.tolist()

			if(prikaz_rj == 0):
				populacija.remove(list(var))
			if(prikaz_rj == 1):
				
				populacija.remove(var.tolist())
				#populacija = populacija.tolist()

			if(prikaz_rj == 0):
				populacija_eval.remove(funkcija(var))
			if(prikaz_rj == 1):
				x = pretvori(var,preciznost,donja_granica,gornja_granica,stupanj_populacije)
				populacija_eval.remove(funkcija(x))

			del slucajne[indeks_najlosije]
			del slucajne_eval[indeks_najlosije]


			if(prikaz_rj == 0):
				coin = randint(0,1)
				ind = r.sample(range(0,turnir_arg-1),2)
				if(coin == 1):
					#ind = r.sample(range(0,h-1),2)
					nova_jedinka = aritmeticko_krizanje(slucajne[ind[0]], slucajne[ind[1]], vj_krizanja)
				else:
					nova_jedinka = heuristicko_krizanje(slucajne[ind[0]], slucajne[ind[1]], vj_krizanja, donja_granica, gornja_granica, funkcija)

			if(prikaz_rj == 1):
				coin = randint(0,1)
				ind = r.sample(range(0,turnir_arg-1),2)
				if(coin == 1):
					nova_jedinka = single_point_crossover(slucajne[ind[0]],slucajne[ind[1]],preciznost,vj_krizanja,stupanj_populacije)
				if(coin == 0):
					nova_jedinka = uniform_crossover(slucajne[ind[0]],slucajne[ind[1]],preciznost,vj_krizanja,stupanj_populacije)

			if(prikaz_rj == 0):
				nova_jedinka = mutacija_pz(nptransform(nova_jedinka), vj_mutacije, donja_granica, gornja_granica)
				nova_jedinka_eval = funkcija(nova_jedinka)
			if(prikaz_rj == 1):
			 	nova_jedinka = uniform_mutation(nptransform(nova_jedinka),preciznost,vj_mutacije,stupanj_populacije)
			 	
			 	evaluirano = []
			 	for i in range(0, stupanj_populacije):
			 		vrijednost = 0
			 		broj_bitova = preciznost - 1 
			 		for j in range(0, preciznost):
			 			vrijednost += nova_jedinka[i][j] * (2**broj_bitova)
			 			broj_bitova = broj_bitova - 1
			 		a = dekoder(vrijednost, donja_granica, gornja_granica, preciznost)
			 		evaluirano.append(a)
			 	nova_jedinka_eval = funkcija(evaluirano)

			populacija.append(nova_jedinka)
			populacija_eval.append(nova_jedinka_eval)
			#print(len(populacija_eval))

			#print(populacija_eval)
			populacija = nptransform(populacija)
			populacija_eval = nptransform(populacija_eval)
			
	return 0

def main():
	x = input("Zadatak: ")
	if(int(x) == 1):
		x1 = input("Funkcija: ")
		if(int(x1) == 1):
			x2 = input("Prikaz: ")
			if(int(x2) == 0):
				#ZADATAK1
				# - f1
				#pomicna tocka
				donja_granica = -50
				gornja_granica = 150
				velicina_populacije = 100
				stupanj_populacije = 2
				vj_mutacije = 0.8
				vj_krizanja = 0.7
				broj_evaluacija = 1000000
				f1.count = 0
				prikaz_rj = 0
				turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f1,2)
			if(int(x2) == 1):
				#ZADATAK1
				# - f1
				#binarno
				donja_granica = -50
				gornja_granica = 150
				velicina_populacije = 100
				stupanj_populacije = 2
				vj_mutacije = 0.5
				vj_krizanja = 0.7
				broj_evaluacija = 1000000
				f1.count = 0
				binarna_preciznost = 3
				prikaz_rj = 1
				turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f1,binarna_preciznost)
		if(int(x1) == 3):
			x2 = input("Prikaz: ")
			if(int(x2) == 0):
				#ZADATAK1
				# - f3
				#pomicna tocka
				donja_granica = -50
				gornja_granica = 150
				velicina_populacije = 100
				stupanj_populacije = 2
				vj_mutacije = 0.5
				vj_krizanja = 0.7
				broj_evaluacija = 1000000
				f3.count = 0
				binarna_preciznost = 7
				prikaz_rj = 0
				turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f3,binarna_preciznost)
			if(int(x2) == 1):
				#ZADATAK1
				# - f3
				#binarno
				donja_granica = -50
				gornja_granica = 150
				velicina_populacije = 100
				stupanj_populacije = 2
				vj_mutacije = 0.5
				vj_krizanja = 0.7
				broj_evaluacija = 1000000
				f3.count = 0
				binarna_preciznost = 7
				prikaz_rj = 1
				turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f3,binarna_preciznost)
		if(int(x1) == 6):
			x2 = input("Prikaz: ")
			if(int(x2) == 0):
				#ZADATAK1
				# - f6
				#pomicna tocka
				donja_granica = -50
				gornja_granica = 150
				velicina_populacije = 100
				stupanj_populacije = 2
				vj_mutacije = 0.7
				vj_krizanja = 0.4
				broj_evaluacija = 1000000
				f6.count = 0
				binarna_preciznost = 7
				prikaz_rj = 0
				turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost)
			if(int(x2) == 1):
				#ZADATAK1
				# - f6
				#binarno
				donja_granica = -50
				gornja_granica = 150
				velicina_populacije = 100
				stupanj_populacije = 2
				vj_mutacije = 0.7
				vj_krizanja = 0.4
				broj_evaluacija = 1000000
				f6.count = 0
				binarna_preciznost = 7
				prikaz_rj = 1
				turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost)
		if(int(x1) == 7):
			x2 = input("Prikaz: ")
			if(int(x2) == 0):
				#ZADATAK1
				# - f7
				#pomicna tocka
				donja_granica = -50
				gornja_granica = 150
				velicina_populacije = 100
				stupanj_populacije = 2
				vj_mutacije = 0.5
				vj_krizanja = 0.7
				broj_evaluacija = 1000000
				f7.count = 0
				binarna_preciznost = 7
				prikaz_rj = 0
				turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f7,binarna_preciznost)
			if(int(x2) == 1):
				#ZADATAK1
				# - f7
				#binarno
				donja_granica = -50
				gornja_granica = 150
				velicina_populacije = 300
				stupanj_populacije = 2
				vj_mutacije = 0.89
				vj_krizanja = 0.8
				broj_evaluacija = 1000000
				f7.count = 0
				binarna_preciznost = 12
				prikaz_rj = 1
				turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f7,binarna_preciznost)
	if(int(x) == 2):
		dim = [1,3,6,10]
		for i in dim:
			print("Dimenzionalnost: " + str(i))
			print("Funkcija 6 => ",end='')
			donja_granica = -50
			gornja_granica = 150
			velicina_populacije = 100
			stupanj_populacije = i
			vj_mutacije = 0.7
			vj_krizanja = 0.4
			broj_evaluacija = 1000000
			f6.count = 0
			binarna_preciznost = 7
			prikaz_rj = 0
			turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 1)
			print("Funkcija 7 => ",end='')
			donja_granica = -50
			gornja_granica = 150
			velicina_populacije = 100
			stupanj_populacije = i
			vj_mutacije = 0.5
			vj_krizanja = 0.7
			broj_evaluacija = 1000000
			f7.count = 0
			binarna_preciznost = 7
			prikaz_rj = 0
			turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f7,binarna_preciznost,ispis = 1)
	if(int(x) == 3):

		donja_granica = -50
		gornja_granica = 150
		velicina_populacije = 100
		vj_mutacije = 0.3
		vj_krizanja = 0.8
		broj_evaluacija = 100000
		binarna_preciznost = 4

		print("Funkcija f6 - pomični zarez - dimenzija: 3")

		lista_f6_pz_3 = []
		stupanj_populacije = 3
		broj_pogodaka = 0
		for i in range(0,10):

			f6.count = 0
			prikaz_rj = 0
			tmp = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
			if(abs(tmp) < 1e-6):
				broj_pogodaka = broj_pogodaka + 1
			
			lista_f6_pz_3.append(tmp)
		
		print("Broj pogodaka: " + str(broj_pogodaka))
		print("Median: " + str(np.median(lista_f6_pz_3)))
 
		print("Funkcija f6 - pomični zarez - dimenzija: 6")

		lista_f6_pz_6 = []
		stupanj_populacije = 6
		broj_pogodaka = 0
		for i in range(0,10):
			
			f6.count = 0
			prikaz_rj = 0
			tmp = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
			if(abs(tmp) < 1e-6):
				broj_pogodaka = broj_pogodaka + 1
			
			lista_f6_pz_6.append(tmp)

		print("Broj pogodaka: " + str(broj_pogodaka))
		print("Median: " + str(np.median(lista_f6_pz_3)))

		print("Funkcija f7 - pomični zarez - dimenzija: 3")

		lista_f7_pz_3 = []
		stupanj_populacije = 3
		broj_pogodaka = 0
		for i in range(0,10):
		
			f7.count = 0
			prikaz_rj = 0
			tmp = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
			if(abs(tmp) < 1e-6):
				broj_pogodaka = broj_pogodaka + 1
			
			lista_f7_pz_3.append(tmp)
		
		print("Broj pogodaka: " + str(broj_pogodaka))
		print("Median: " + str(np.median(lista_f7_pz_3)))

		print("Funkcija f7 - pomični zarez - dimenzija: 6")

		lista_f7_pz_6 = []
		stupanj_populacije = 6
		broj_pogodaka = 0
		for i in range(0,10):
			
			f7.count = 0
			prikaz_rj = 0
			tmp = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
			if(abs(tmp) < 1e-6):
				broj_pogodaka = broj_pogodaka + 1
			
			lista_f7_pz_6.append(tmp)
		
		print("Broj pogodaka: " + str(broj_pogodaka))
		print("Median: " + str(np.median(lista_f7_pz_6)))


		print("Funkcija f6 - binarno - dimenzija: 3")
		binarna_preciznost = 4

		lista_f6_bin_3 = []
		stupanj_populacije = 3
		broj_pogodaka = 0
		for i in range(0,10):
			
			f6.count = 0
			prikaz_rj = 1
			tmp = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
			if(abs(tmp) < 1e-6):
				broj_pogodaka = broj_pogodaka + 1
			
			lista_f6_bin_3.append(tmp)
		
		print("Broj pogodaka: " + str(broj_pogodaka))
		print("Median: " + str(np.median(lista_f6_bin_3)))

		print("Funkcija f6 - binarno - dimenzija: 6")
		binarna_preciznost = 4

		lista_f6_bin_6 = []
		stupanj_populacije = 6
		broj_pogodaka = 0
		for i in range(0,10):
			
			f6.count = 0
			prikaz_rj = 1
			tmp = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
			
			lista_f6_bin_6.append(tmp)
		
		print("Broj pogodaka: " + str(broj_pogodaka))
		print("Median: " + str(np.median(lista_f6_bin_6)))

		print("Funkcija f7 - binarno - dimenzija: 3")
		binarna_preciznost = 4

		lista_f7_bin_3 = []
		stupanj_populacije = 3
		broj_pogodaka = 0
		for i in range(0,10):
			
			f7.count = 0
			prikaz_rj = 1
			tmp = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
			
			lista_f7_bin_3.append(tmp)
	
		print("Broj pogodaka: " + str(broj_pogodaka))
		print("Median: " + str(np.median(lista_f7_bin_3)))

		print("Funkcija f7 - binarno - dimenzija: 6")
		binarna_preciznost = 4

		lista_f7_bin_6 = []
		stupanj_populacije = 6
		broj_pogodaka = 0
		for i in range(0,10):
			
			f7.count = 0
			prikaz_rj = 1
			tmp = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
			
			lista_f7_bin_6.append(tmp)
		
		print("Broj pogodaka: " + str(broj_pogodaka))
		print("Median: " + str(np.median(lista_f7_bin_6)))
	if(int(x) == 4):
		donja_granica = -50
		gornja_granica = 150
		stupanj_populacije = 2
		vj_krizanja = 0.9
		vj_mutacije = 0.7
		broj_evaluacija = 1000000
		f6.count = 0
		binarna_preciznost = 7
		prikaz_rj = 0
		
		velicina_populacije = [30,50,100,200]
		vj_mutacije_lista = [0.1,0.3,0.6,0.9]

		populacija_boxplot = []
		lista_medijana = []
		for i in range(0, len(velicina_populacije)):
			lista_najboljih = []
			for j in range(0,30):
				x = turnirski(donja_granica,gornja_granica,velicina_populacije[i],prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
				lista_najboljih.append(x)
			populacija_boxplot.append(lista_najboljih)
			lista_medijana.append(np.median(lista_najboljih))

		print("Traženje idealnog parametra za veličinu populacije")
		print("Lista medijana (populacija): ")
		print(lista_medijana)
		najmanji = min(lista_medijana)
		indeks_najmanjeg = lista_medijana.index(najmanji)
		print("Idealni parametar za veličinu populacije je: " + str(velicina_populacije[indeks_najmanjeg]))

		print("Traženje idealnog parametra za vjerojatnost mutacije uz veličinu populacije: " + str(velicina_populacije[indeks_najmanjeg]))
		lista_medijana = []
		for i in range(0, len(vj_mutacije_lista)):
			lista_najboljih = []
			for j in range(0,30):
				x = turnirski(donja_granica,gornja_granica,velicina_populacije[indeks_najmanjeg],prikaz_rj,vj_mutacije_lista[i],vj_krizanja,broj_evaluacija,stupanj_populacije,f6,binarna_preciznost,ispis = 2)
				lista_najboljih.append(x)
			lista_medijana.append(np.median(lista_najboljih))
		print("Lista medijana (vjerojatnost križanja): ")
		print(lista_medijana)
		najmanji = min(lista_medijana)
		indeks_najmanjeg = lista_medijana.index(najmanji)
		print("Idealni parametar za vjerojatnost mutacije je: " + str(vj_mutacije_lista[indeks_najmanjeg]))


		#print(populacija_boxplot)
		fig1, ax1 = plt.subplots()
		ax1.boxplot(populacija_boxplot)
		plt.xticks([1, 2, 3, 4], [str(30), str(50), str(100), str(200)])
		plt.xlabel('Veličina populacije')
		plt.ylabel('Minimum')
		plt.show()
	if(int(x) == 5):
		donja_granica = -50
		gornja_granica = 150
		velicina_populacije = 100
		stupanj_populacije = 2
		vj_mutacije = 0.5
		vj_krizanja = 0.7
		broj_evaluacija = 1000000
		f7.count = 0
		binarna_preciznost = 7
		prikaz_rj = 0

		print("Turnir: 3")
		najbolji = []
		for i in range(0,30):
			x = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f7,binarna_preciznost,ispis = 2, turnir = 3)
			najbolji.append(x)
		print(np.median(najbolji))

		print("Turnir: 5")
		najbolji = []
		for i in range(0,30):
			x = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f7,binarna_preciznost,ispis = 2, turnir = 5)
			najbolji.append(x)
		print(np.median(najbolji))

		print("Turnir: 10")
		najbolji = []
		for i in range(0,30):
			x = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f7,binarna_preciznost,ispis = 2, turnir = 10)
			najbolji.append(x)
		print(np.median(najbolji))

		print("Turnir: 30")
		najbolji = []
		for i in range(0,30):
			x = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f7,binarna_preciznost,ispis = 2, turnir = 30)
			najbolji.append(x)
		print(np.median(najbolji))

		print("Turnir : 50")
		najbolji = []
		for i in range(0,30):
			x = turnirski(donja_granica,gornja_granica,velicina_populacije,prikaz_rj,vj_mutacije,vj_krizanja,broj_evaluacija,stupanj_populacije,f7,binarna_preciznost,ispis = 2, turnir = 50)
			najbolji.append(x)
		print(np.median(najbolji))
#3,5,10,30,50

main()








