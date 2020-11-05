#!/bin/bash

datoteke_temp=*.txt

datoteke=""

for dat in $datoteke_temp;
do
	if [[ $dat =~ localhost_access_log\.[0-9]{4}-02-[0-9]{2}\.txt ]] ;
	then
			datoteke+="$dat "
	fi
done

for dat in $datoteke;
do
	touch temp
	echo "datum: $(echo "$dat"| sed -r 's/.*([0-9]{4})-([0-9]{2})-([0-9]{2}).txt/\3-\2-\1/')" 
	echo "----------------------------------------------------------------"
	sed -r 's/.*"(.*)".*/\1/g' $dat > temp
	sort temp | uniq -c | sort -rn | sed -r 's/ *([0-9]+) (.*)/  \1 : \2/'  

done
rm temp
