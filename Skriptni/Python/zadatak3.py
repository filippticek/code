#!/usr/bin/python
import sys
import os
import re

with open('studenti.txt', 'r') as dat:
    studenti = {}
    for line in dat:
        jmbag, prezime, ime = line.rstrip().split()
        studenti[jmbag] = (prezime, ime)

bodovi = {}
labosi = []
for datoteka in os.listdir("."):
    if re.match(r'Lab', datoteka) is not None:
         m = re.match(r'Lab_([0-9]+)_g[0-9]+.txt',datoteka)
         lab = int(m.group(1))
         if lab not in labosi:
             labosi.append(lab)

         with open(datoteka, 'r') as dat:
            for line in dat:
                jmbag, rez = line.rstrip().split()
                if (jmbag, lab) in bodovi:
                    print("Duplikat JMBAG:{0} Labos:{1}".format(jmbag, lab))
                else:
                    bodovi[(jmbag,lab)] = rez

ispis = "%-10s   %-20s  " % ("JMBAG", "Prezime, Ime")
labosi.sort()
for lab in labosi:
    ispis += "L%-3s  " % (lab)
print (ispis)

for student in studenti.keys():
    ispis = "%-10s   %-20s  " % (student, ','.join(studenti[student]))
    for lab in labosi:
        if (student,lab) in bodovi:
            ispis += "%-4s  " % (bodovi[(student,lab)])
        else :
            ispis += "-     "
    print(ispis)
