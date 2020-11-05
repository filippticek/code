#!/bin/bash

if [ ! -e $1 ] ; 
then
	echo "Nema foldera sa slikama"
	exit 1
fi

if [ ! -e $2 ] ;
then
	mkdir "$2"
fi

for picture in $1/* ;
do
	temp=$(stat --format=%y $picture | sed -r 's/(.{7}).*/\1/')
	if [ ! -e $2/$temp ] ;
	then 
		mkdir "$2/$temp"
	fi

	mv $picture $2/$temp/

done
