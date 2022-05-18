#!/bin/sh

for datoteka in $(ls | grep -iE '[a-z]{9}*[a-z]{6}*[a-z]{3}.[0-9]{4}-02-[0-9]{2}'); do
	godina=$(echo $datoteka | cut -d'.' -f2 | cut -d'-' -f1)
	mjesec=$(echo $datoteka | cut -d'.' -f2 | cut -d'-' -f2)
	dan=$(echo $datoteka | cut -d'.' -f2 | cut -d'-' -f3)

	rez="datum: ${dan}-${mjesec}-${godina}"

	echo $rez
	echo "----------------------"
	cut -d'"' -f2 $datoteka |sort | uniq -c |sort -nr  |  tr -s " "  | sed 's/ / : /2'
	
done

