import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
from scipy.stats import expon
from scipy.stats import uniform
from scipy.stats import weibull_min

O = 7
N = 3
M = 8
Z = 1
Y = 9
X = 4

def writeCsv(first, second, third, fourth, fifth, sixth):
    with open('dist.csv', 'w', newline='') as csvfile:
        distwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(1000):
            distwriter.writerow([str(first[i]) + ',' + str(second[i]) + ',' +  str(third[i]) + ',' +  str(fourth[i]) + ',' +  str(fifth[i]) + ',' +  str(sixth[i])])

def u_uniform(x):
    return (M - N) * x + N

def u_exponential(x):
    return - np.log(1 - x) / O

def u_weibull(x):
    return X * np.power( - np.log(1 - x), 1. / Y)


U = uniform.rvs(size=1000, loc = 0, scale=1)
U1 = []
E1 = []
W1 = []
U2 = uniform.rvs(size=1000, loc = N, scale= M - N)
E2 = expon.rvs(size=1000,loc = 0, scale = 1. / O)
W2 = weibull_min.rvs(c = Y,size=1000,loc = 0, scale = X)
for x in U:
    E1.append(u_exponential(x))
    U1.append(u_uniform(x))
    W1.append(u_weibull(x))

writeCsv(U1,E1,W1,U2,E2,W2)

  
n, bins, patches = plt.hist(U1,bins=50, density=1,facecolor='red', alpha=0.5, label='User distribution')
n, bins, patches = plt.hist(U2,bins=50, density=1,facecolor='blue', alpha=0.25, label='scipy distribution')
rv = uniform(loc=N, scale=M-N)
plt.plot(bins, rv.pdf(bins), 'r--', linewidth=3)

n ,bins, patches = plt.hist(E1, bins='auto', density=1, facecolor='red', alpha=0.5, label='User distribution')
n ,bins, patches = plt.hist(E2, bins='auto', density=1, facecolor='blue', alpha=0.5, label='scipydistribution')
rv = expon(scale = 1./ O)
plt.plot(bins, rv.pdf(bins), 'r--', linewidth=3)

n ,bins, patches = plt.hist(W1, bins='auto', density=1, facecolor='green', alpha=0.5)
n ,bins, patches = plt.hist(W2, bins='auto', density=1, facecolor='blue', alpha=0.5)
rv = weibull_min(Y, scale=X)
plt.plot(bins, rv.pdf(bins), 'r--', linewidth=3)

plt.show()