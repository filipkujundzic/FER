#!/bin/sh
rez=0
if [ $# == 2 ]; then
	echo "parametri su ok"
else
	echo -e "unos: ime kazala uzorak imena datoteka"
	exit 1
fi

echo "parametri: $1 $2"
for datoteka in $(find $1 -name "$2"); do
	broj=$(wc -w $datoteka | cut -d " " -f1)
	rez=$[$rez+broj]
done

echo "Ukupan broj redaka: $rez"

