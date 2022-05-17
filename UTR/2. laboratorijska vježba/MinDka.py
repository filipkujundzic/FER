#!/usr/bin/python3

import sys

dobrastanja = set()
prijelaz = {}

def izbaci_stanja(stanje):
	dobrastanja.add(stanje)
	for z in abeceda:
		i = prijelaz[stanje,z]
		if( i not in dobrastanja):
			izbaci_stanja(i)
	return 


def predstavnik(dobrastanja,neistovjetna,p):
	for q in dobrastanja:
		if (p,q) not in neistovjetna and (q,p) not in neistovjetna:
			return q

	print("greska")


fin = sys.stdin

stanja = fin.readline().strip().split(",")
abeceda = fin.readline().strip().split(",")
prihvatljiva = fin.readline().strip().split(",")
pocetno = fin.readline().strip()

for line in fin.readlines():
	lijevo, desno = line.strip().split('->')
	stanje, znak = lijevo.split(',')
	prijelaz[stanje,znak] = desno

izbaci_stanja(pocetno)

my_list = list(dobrastanja)
my_list.sort()


neistovjetna = set()

for i in my_list:
	for j in my_list:
		if(i<j):
			if(((i in prihvatljiva) and (j not in prihvatljiva) or ((i not in prihvatljiva) and (j in prihvatljiva)))):	
				neistovjetna.add((i,j))

lista_parova = {}
for p in my_list:
	for q in my_list:
		if(p<q):
			lista_parova[p,q] = []

def oznaci(stanje1,stanje2):
	neistovjetna.add((stanje1,stanje2)) 
	for s1,s2 in lista_parova[stanje1,stanje2]:
		oznaci(s1,s2)
	lista_parova[stanje1,stanje2] = []


for p in my_list:
	for q in my_list:
		if(p<q):
			for a in abeceda:
				pp = prijelaz[p,a]
				qq = prijelaz[q,a]
				if(qq < pp):
					pp,qq = qq,pp
				if (pp,qq) in neistovjetna:
					oznaci(p,q)
				elif pp != qq:
					lista_parova[pp,qq].append((p,q))

konacnastanja = []
for p in my_list:
	if (p == predstavnik(my_list,neistovjetna,p)):
		konacnastanja.append(p)


print (",".join(konacnastanja))
print (",".join(abeceda))

konacnaprihvatljiva = []
for p in prihvatljiva:
	if(p in konacnastanja):
		konacnaprihvatljiva.append(p)

print (",".join(konacnaprihvatljiva))
print (predstavnik(my_list,neistovjetna,pocetno))

for p in konacnastanja:
	for znak in abeceda:
		print ("{},{}->{}".format(p,znak,predstavnik(my_list,neistovjetna,prijelaz[p,znak])))