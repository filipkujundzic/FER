#!/usr/bin/python3

import sys

def simuliraj_korak(prijelaz, stanja, znak):
    novastanja = set()
    for stanje in stanja:
        for novo in prijelaz[stanje, znak]:
            novastanja.add(novo)    

    return novastanja

def simuliraj_epsilon(prijelaz, stanja):

    novastanja = set(stanja)
    gotovo = False
    while not gotovo:
        noviskup = set()
        #print (novastanja)
        for stanje in novastanja:
            for novo in prijelaz[stanje, "$"]:
                noviskup.add(novo)
        gotovo = True
        
        for novo in noviskup:
            if novo not in novastanja:
                novastanja.add(novo)
                gotovo = False
    return novastanja
    
fin = sys.stdin
#fin = open("test16/test.a")
inputs = fin.readline().strip().split("|")
stanja = fin.readline().strip().split(",")
simboli = fin.readline().strip().split(",")
prihvatljiva = fin.readline().strip().split(",")
pocetno = fin.readline().strip()

prijelaz = {}
for stanje in stanja:
    for znak in simboli:
        prijelaz[stanje, znak] = []
    prijelaz[stanje, "$"] = []

for line in fin.readlines():
    lijevo, desno = line.strip().split('->')
    stanje, znak = lijevo.split(',')
    if desno != "#":
        prijelaz[stanje, znak].extend(desno.split(","))

#print (prijelaz)

for ulaz in inputs:
    znakovi = ulaz.split(",")
    stanja = {pocetno}
    stanja = simuliraj_epsilon(prijelaz,stanja)
    for znak in znakovi:
        if len(stanja) == 0:
            print ("#|", end ='')
        else:
            print (",".join(sorted(stanja)), end='|')
        stanja = simuliraj_korak(prijelaz, stanja, znak)
        stanja = simuliraj_epsilon(prijelaz,stanja)
    if len(stanja) == 0:
        print ("#")
    else:
        print (",".join(sorted(stanja)))

#print([inputs, stanja, simboli, prihvatljiva, pocetno])
#print (prijelaz)

