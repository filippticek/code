#!/usr/bin/python
import sys

with open('ulaz.txt', 'r') as dat:
    print ("Hyp#Q10#Q20#Q30#Q30#Q40#Q50#Q60#Q70#Q80#Q90")
    j = 1
    for line in dat:
        vrijednosti = [float(i) for i in line.rstrip().split()]
        vrijednosti.sort()
        length = len(vrijednosti)
        ispis = "%03d" % (j)
        j += 1
        for i in range(1, 10):
            ispis += "#%.2f" % (vrijednosti[int(length*i/10)])
            
        print(ispis)
           

