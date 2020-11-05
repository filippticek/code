#!/usr/bin/python
import sys

def vratiMatrice(datoteka):
    r, s = datoteka.readline().rstrip().split()
    m1 = {'redak': int(r), 'stupac': int(s)}
    line = datoteka.readline().rstrip()
    while line != "":
        var = line.split()
        m1[(int(var[0]),int(var[1]))] = float(var[2])
        line = datoteka.readline().rstrip()

    r, s = datoteka.readline().rstrip().split()
    m2 = {'redak': int(r), 'stupac': int(s)}
    line = datoteka.readline().rstrip()
    while line != "":
        var = line.split()
        m2[(int(var[0]),int(var[1]))] = float(var[2])
        line = datoteka.readline().rstrip()

    if m1['stupac'] != m2['redak']:
        print('Krive dimenzije matrica')
        sys.exit(1)
    return m1, m2

def produktMatrica(m1, m2):
    rez = {'redak': m1['stupac'], 'stupac': m2['redak']}
    for i in range(1, rez['redak']+1):
        for j in range(1, rez['stupac']+1):
            suma = 0.0
            for k in range(1, rez['redak']+1):
                if (i,k) in m1:
                    x = m1[(i,k)]
                else:
                    x = 0
                if (k, j) in m2:
                    y = m2[(k,j)]
                else:
                    y = 0
                suma += y * x
            
            if suma != 0:
                rez[(i,j)] = suma
    return rez

with open('matrice.txt', 'r') as dat:
    m1, m2 = vratiMatrice(dat)
    rez = produktMatrica(m1, m2)
    
with open('rezultat.txt', 'w') as dat:
    dat.write("{0} {1}\n".format(rez['redak'], rez['stupac']))
    for i in range(1, rez['redak']+1):
        for j in range(1, rez['stupac']+1):
            if (i,j) in rez:
                dat.write("{0} {1} {2}\n".format(i, j, rez[(i,j)]))
