#!/bin/bash

proba="Ovo je proba"
echo $proba

lista_datoteka=*
echo $lista_datoteka

proba3="$proba; $proba; $proba;" 
#echo $proba3 

a=4
b=3
c=7
d=$((($a+4)*$b%$c))
#echo $d

broj_rijeci=$(wc -w *.txt | tail -n 1 | cut -d' ' -f2)
#echo $broj_rijeci

ls ~/

cut -d':' -f1,6,7 /etc/passwd 

ps -e -ouid,pid,cmd
