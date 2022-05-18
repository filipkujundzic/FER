#!/bin/sh

if [ $# == 2 ]; then
	echo "parametri su ok"
else
	echo -e "unos: izvorisna mapa odredisna mapa"
	exit 1
fi

if [ ! -d $2 ]; then
	mkdir $2
fi

for picture in ./$1/*; do
	echo "prijenos slike $picture"
	slika=$(stat -c%y "$picture")
	godina=$(echo $slika |cut -d'-' -f1)
	mjesec=$(echo $slika |cut -d'-' -f2)
	ime="$godina-$mjesec"

	if [ ! -d ./$2/$ime ]; then
		mkdir ./$2/$ime
	fi

	mv "$picture" ./$2/$ime
done
echo "-> prijenos slika zavrsio"
