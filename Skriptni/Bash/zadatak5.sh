#!/bin/bash

if [ ! -e $1 ] ; 
then
	echo "Nema datoteke $1"
	exit 1
fi
sum=0
datoteke=$(locate "$(pwd)/$1/$2")

for dat in $datoteke ; 
do
	sum=$(( $(wc -l $dat | cut -d' ' -f1) + sum ))
done
echo $sum
