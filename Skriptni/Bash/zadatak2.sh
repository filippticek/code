#!/bin/bash

grep -i  'banana\|jabuka\|jagoda\|dinja\|lubenica' namirnice.txt

grep -vi  'banana\|jabuka\|jagoda\|dinja\|lubenica' namirnice.txt > ne-voce.txt

grep -n '[A-Z]{3}[0-9]{6}' ~/projekti/*

find * -mtime +7 -a -mtime -14

for x in {1..15}; 
do
	echo $x
done
