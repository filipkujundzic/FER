#!/bin/sh

proba="Ovo je proba"
echo $proba

lista_datoteka=$(ls *)
echo $lista_datoteka

proba3="${proba}. ${proba}. ${proba}."
echo $proba3

a=4
b=3
c=7
d=$(((a+4)*b%c))
echo $d

broj_rijeci=$(wc -w *txt)
echo $broj_rijeci

echo ~

cut -d: -f 1,6,7 /etc/passwd

ps | tr -s " " | cut -d " " -f 2,3,9