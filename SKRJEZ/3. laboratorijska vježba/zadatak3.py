#!/usr/bin/python

import os
br = []

for dat in os.listdir(".\\treci_a"):
	if(dat != "studenti.txt"):
		br.append(dat)
br.sort()
broj = int((br[-1]).split("_")[1]) #broj laboratorija
print(broj)

naslov = "JMBAG\t\tPrezime,Ime\t"
for i in range(1,broj+1):
	naslov += "L" + str(i) + "\t"


print(naslov)

svi = {}
with open(".\\treci_a\\studenti.txt") as f:
	for line in f:
		tmp = line.strip().split()
		svi[tmp[0]] = [tmp[1],tmp[2],[]]


for dat in os.listdir(".\\treci_a"):
	if(dat != "studenti.txt"):
		broj = int((str(dat).split("_"))[1])
		with open(".\\treci_a"+"\\"+dat) as f:
			for line in f:
				lista = line.strip().split()
				svi[str(lista[0])][2].extend((" "," "))
				svi[str(lista[0])][2][broj-1] = lista[1]
	

for key,value in svi.items():
	tp = ""
	for l in value[2]:
		tp += str(l) + "\t"
	p = key + "\t" +value[0] + "," + value[1] + "\t" + str(tp)
	print(p)
