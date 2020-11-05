#!/bin/bash

if [ ! -e $1 ] ;
then 
	echo "$1 ne postoji"
	exit 1
fi
touch temp

for g in $(cut -d';' -f3 "$1" | sort | uniq );
do
	value=$(grep $g $1 | cut -d';' -f2)
	count=0
	for v in $value;
	do
		count=$(( $count + $v ))
	done
	echo "$count $g" >> temp
done
sort -n temp #| sed -re 's/([0-9]*) x(.+)/\2 \1/g'
rm temp
