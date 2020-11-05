#!/bin/bash

if [ ! -e "${!#}" ] ;
then 
	mkdir ${!#}
	echo "Kreirano je kazalo ${!#}"
fi

sum=0

for arg;
do
	if [ -d "$arg" ] ;
	then
		continue
	fi

	cp "$arg" "${!#}" 
	sum=$((1 + sum))
done

echo "$sum datoteka kopirano je u kazalo ${!#}"
