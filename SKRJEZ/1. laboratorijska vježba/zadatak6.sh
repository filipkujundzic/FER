#!/bin/sh
counter=0
for var in "$@"; do
	:
done

if [ ! -d ./$var ]; then
		mkdir ./$var
		echo "Kreirano je kazalo $var."
fi

length=$(($#-1))
for var2 in "${@:1:$length}"; do
	if [ ! -f "$var2" -a -e "$var2" ]; then
		continue
	fi
	cp "$var2" "$var"
	counter=$[counter+1]
done

echo "$counter datoteka je kopirano u kazalo $var."