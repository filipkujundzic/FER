#!/usr/bin/python3
import sys
fin = sys.stdin
ulnizovi = fin.readline().strip().split("|")
stanja = fin.readline().strip().split(",")
abeceda = fin.readline().strip().split(",")
znakovistoga = fin.readline().strip().split(",")
prihvstanja = fin.readline().strip().split(",")
pocetnost = fin.readline().strip()
pocetniznakstoga = fin.readline().strip()

def cmp(a, b):
    return (a > b) - (a < b) 


def prvi(pocetnost,pocetniznakstoga):
	r = pocetnost + "#" + pocetniznakstoga + "|"
	return r

def racunaj(pocetnost,znaktrake,vrhstoga):
	novostanje,zavrsetakstoga = prijelaz[pocetnost,znaktrake,vrhstoga]

	obradi_stog(zavrsetakstoga)
	s = ""
	s = ispisi_stog()
	r = novostanje + "#" + s + "|"
	return r

def kraj(stanje):
	if stanje in prihvstanja:
		return "1"
	else:
		return "0"

def postoji(stanje,znak,vrhstoga):
	tmp = [stanje,znak,vrhstoga]
	r = 0
	for i in prijelaz:
		a = list(i)
		if(cmp(tmp,a) == 0):
			r = 1
	return r

pomocni = []
def obradi(niz):
	niz2 = niz[:-1]
	pomocni = niz2.split("#")
	return pomocni


stog = []
def obradi_stog(znak):
	stog.pop()
	if znak == "$":
		return
	for c in znak[::-1]:
		stog.append(c)

def ispisi_stog():
	if len(stog) == 0:
		return "$"
	ispis =""
	tmp = list(stog)
	for i in tmp[::-1]:
		ispis += tmp.pop()
	return ispis



ulaz = []
for i in ulnizovi:
	a = i.strip().split(',')
	ulaz.append(a)


ulaz_kon = []

for i in ulaz:
	for j in i:
		ulaz_kon.append(j)

prijelaz = {}
for line in fin.readlines():
	lijevo, desno = line.strip().split('->')
	stanje, znak, vrhstoga = lijevo.split(',')
	novostanje, zavrsetakstoga = desno.split(',')
	prijelaz[stanje,znak,vrhstoga] = [novostanje,zavrsetakstoga]
	


flag = 0 
kon = prvi(pocetnost,pocetniznakstoga)
stog.append(pocetniznakstoga)

i = 0
for t in ulaz_kon:
	while(len(stog) > 0 and postoji(pocetnost,"$",pocetniznakstoga[0]) == 1):
		temp = racunaj(pocetnost,"$",pocetniznakstoga[0])
		kon += temp
		pocetnost, pocetniznakstoga = obradi(temp) 
	if(len(stog) > 0 and postoji(pocetnost,t,pocetniznakstoga[0]) == 1 and t != "$"):
		temp = racunaj(pocetnost,t,pocetniznakstoga[0])
		kon += temp
		pocetnost, pocetniznakstoga = obradi(temp) 
	else:
		kon += "fail|0"
		flag = 1
		break
while(len(stog) > 0 and postoji(pocetnost,"$",pocetniznakstoga[0]) == 1):
	temp = racunaj(pocetnost,"$",pocetniznakstoga[0])
	kon += temp
	pocetnost, pocetniznakstoga = obradi(temp) 

if (flag == 0):
	kon += kraj(pocetnost)
print(kon)
