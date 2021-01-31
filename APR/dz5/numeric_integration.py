from matrica import Matrica
from sys import stdin, argv
import matplotlib.pyplot as plt
from math import cos, sin

def runge_kutta(A, x, T, tmax, B=None, r=None, print_step=0):
    B = B if B != None else 0#Matrica([[0 for _ in range(A.get_dimension())] for _ in range(A.get_dimension())])
    t = 0
    xk = x
    x1 = []
    x2 = []
    t_array = []
    i=1
    while t <= tmax:
        t_array.append(t)
        r1 = Matrica([[t],[t]]) if r==None else r
        m1 = A * xk + B * r1
        r2 = Matrica([[t + T / 2],[t + T / 2]]) if r==None else r
        m2 = A * (xk + m1 * (T / 2)) + B * r2
        r3 = Matrica([[t + T / 2],[t + T / 2]]) if r==None else r
        m3 = A * (xk + m2 * (T / 2)) + B * r3
        r4 = Matrica([[t + T],[t + T]]) if r==None else r
        m4 = A * (xk + m3 * T) + B * r4
        xk1 = xk + (m1 + m2 * 2 + m3 * 2 + m4) * T * (1.0 / 6)
        xk = xk1
        x1.append(xk1[0][0])
        x2.append(xk1[1][0])
        t += T
        if i % print_step == 0: 
            print("xk+1:" + str(xk1[0][0]) + ", " + str(xk1[1][0]))

    return x1, x2, t_array

def trapeze(A, x, T, tmax, B=None, r=None, print_step=0):
    U = indentity_matrix(A.get_dimension())
    R = (~(U - A * 0.5 * T)) * (U + A * 0.5 * T)
    S = (~(U - A * 0.5 * T)) * 0.5 * T * B if B != None else 0

    t = 0
    xk = x
    x1 = []
    x2 = []
    t_array = []
    i=1
    while t <= tmax:
        t_array.append(t)
        r = Matrica([[2 * t + T],[2 * t + T]]) if r==None else r
        xk1 = R * xk + S * r
        xk = xk1
        x1.append(xk1[0][0])
        x2.append(xk1[1][0])
        t += T
        if i % print_step == 0: 
            print("xk+1:" + str(xk1[0][0]) + ", " + str(xk1[1][0]))

    return x1, x2, t_array

def euler(A, x, T, tmax, B=None, r=None, print_step=0):
    U = indentity_matrix(A.get_dimension())
    M = U + A * T
    N = B * T if B != None else 0

    t = 0
    xk = x
    x1 = []
    x2 = []
    t_array = []
    i=1
    while t <= tmax:
        t_array.append(t)
        r = Matrica([[t],[t]]) if r==None else r
        xk1 = M * xk + N * r
        xk = xk1
        x1.append(xk1[0][0])
        x2.append(xk1[1][0])
        t += T
        if i % print_step == 0: 
            print("xk+1:" + str(xk1[0][0]) + ", " + str(xk1[1][0]))

    return x1, x2, t_array

def reverse_euler(A, x, T, tmax, B=None, r=None, print_step=0):
    U = indentity_matrix(A.get_dimension())
    P = ~(U - A * T)
    Q = (~(U - A * T)) * B * T if B != None else 0

    t = 0
    xk = x
    x1 = []
    x2 = []
    t_array = []
    i=1
    while t <= tmax:
        t_array.append(t)
        r = Matrica([[t + T],[t + T]]) if r==None else r
        xk1 = P * xk + Q * r
        xk = xk1
        x1.append(xk1[0][0])
        x2.append(xk1[1][0])
        t += T
        if i % print_step == 0: 
            print("xk+1:" + str(xk1[0][0]) + ", " + str(xk1[1][0]))

    return x1, x2, t_array

def pece(A, x, T, tmax, B=None, r=None, print_step=0):
    U = indentity_matrix(A.get_dimension())
    M = U + A * T
    N = B * T if B != None else 0
    R = (~(U - A * 0.5 * T)) * (U - A * 0.5 * T)
    S = (~(U - A * 0.5 * T)) * 0.5 * T * B if B != None else 0

    t = 0
    xk = x
    x1 = []
    x2 = []
    t_array = []
    i=1
    while t <= tmax:
        t_array.append(t)
        #Euler
        r = Matrica([[t],[t]]) if r==None else r
        x_p = M * xk + N * r

        #Trapeze
        r = Matrica([[2 * t + T],[2 * t + T]]) if r==None else r
        xk1 = R * x_p + S * r

        xk = xk1
        x1.append(xk1[0][0])
        x2.append(xk1[1][0])
        t += T
        if i % print_step == 0: 
            print("xk+1:" + str(xk1[0][0]) + ", " + str(xk1[1][0]))

    return x1, x2, t_array

def pece2(A, x, T, tmax, B=None, r=None, print_step=0):
    U = indentity_matrix(A.get_dimension())
    M = U + A * T
    N = B * T if B != None else 0
    P = ~(U - A * T)
    Q = (~(U - A * T)) * B * T if B != None else 0

    t = 0
    xk = x
    x1 = []
    x2 = []
    t_array = []
    i=1
    while t <= tmax:
        t_array.append(t)
        #Euler
        r = Matrica([[t],[t]]) if r==None else r
        x_p = M * xk + N * r

        #Reverse Euler
        r = Matrica([[t + T],[t + T]]) if r==None else r
        x_c = P * x_p + Q * r

        #Reverse Euler
        xk1 = P * x_c + Q * r

        xk = xk1
        x1.append(xk1[0][0])
        x2.append(xk1[1][0])
        t += T
        if i % print_step == 0: 
            print("xk+1:" + str(xk1[0][0]) + ", " + str(xk1[1][0]))

    return x1, x2, t_array

def indentity_matrix(n):
    return Matrica([[1 if i == j else 0 for j in range(n)] for i in range(n)])



def first():
    A = Matrica([[0,1],[-1,0]])
    x = Matrica([[1],[1]])
    r = 0
    T = 0.01
    tmax = 10
    f = [runge_kutta,euler, reverse_euler, trapeze, pece, pece2]
   
    t = 0
    xa1 = []
    xa2 = []
    while t<=tmax:
        xa1.append(x[0][0] * cos(t) + x[1][0] * sin(t))
        xa2.append(x[1][0] * cos(t) - x[0][0] * sin(t))
        t += T

    fig, ax = plt.subplots(7)
    fig.suptitle("First task")
    fig.set_size_inches(10,10)

    i = 0
    for fi in f:
        print(fi.__name__)
        x1, x2, t = fi(A,x,T,tmax, r=r,print_step=tmax/T)
        ax[i].plot(t, x1)
        ax[i].plot(t, x2)
        ax[i].set_title(fi.__name__)
        ax[i].set_xlabel("time")
        ax[i].set_ylabel("X")
        i +=1
        
        error = 0
        for j in range(len(x1)):
            error += abs(xa1[j] - x1[j]) + abs(xa2[j] - x2[j])

        print(fi.__name__ + " Error: " + str(error))

    ax[6].plot(t, xa1)
    ax[6].plot(t, xa2)
    ax[6].set_title("Analitical")
    ax[6].set_xlabel("time")
    ax[6].set_ylabel("X")


    plt.show()


def second():
    A = Matrica([[0,1],[-200,-102]])
    x = Matrica([[1],[-2]])
    r = 0
    T = 0.1
    tmax = 1

    f = [runge_kutta,euler, reverse_euler, trapeze, pece, pece2]
    fig, ax = plt.subplots(6)
    fig.suptitle("Second task")
    fig.set_size_inches(10,10)
    i = 0

    for fi in f:
        print(fi.__name__)
        x1, x2, t = fi(A,x,T,tmax, r=r,print_step=10000)
        ax[i].plot(t, x1)
        ax[i].plot(t, x2)
        ax[i].set_title(fi.__name__)
        ax[i].set_xlabel("time")
        ax[i].set_ylabel("X")
        i +=1

    plt.show()

def third():
    A = Matrica([[0,-2],[1,-3]])
    B = Matrica([[2,0],[0,3]])
    x = Matrica([[1],[3]])
    r = Matrica([[1],[1]])
    T = 0.01
    tmax = 10

    f = [runge_kutta,euler, reverse_euler, trapeze, pece, pece2]
    fig, ax = plt.subplots(6)
    fig.suptitle("Third task")
    fig.set_size_inches(10,10)
    i = 0

    for fi in f:
        print(fi.__name__)
        x1, x2, t = fi(A,x,T,tmax, B=B, r=r,print_step=tmax/T)
        ax[i].plot(t, x1)
        ax[i].plot(t, x2)
        ax[i].set_title(fi.__name__)
        ax[i].set_xlabel("time")
        ax[i].set_ylabel("X")
        i +=1

    plt.show()
    
def fourth():
    A = Matrica([[1,-5],[1,-7]])
    B = Matrica([[5,0],[0,3]])
    x = Matrica([[-1],[3]])
    T = 0.01
    tmax = 10

    f = [runge_kutta,euler, reverse_euler, trapeze, pece, pece2]
    fig, ax = plt.subplots(6)
    fig.suptitle("Fourth task")
    fig.set_size_inches(10,10)
    i = 0

    for fi in f:
        print(fi.__name__) 
        x1, x2, t = fi(A,x,T,tmax,B=B,r=None,print_step=tmax/T)
        ax[i].plot(t, x1)
        ax[i].plot(t, x2)
        ax[i].set_title(fi.__name__)
        ax[i].set_xlabel("time")
        ax[i].set_ylabel("X")
        i +=1

    plt.show()


while True:
    print("Choose between assignment 1-5 or 0 for exit.")
    zad = stdin.readline().strip()
#zad = argv[1].strip()

    if zad == '1':
        first()
    elif zad == '2':
        second()
    elif zad == '3':
        third()
    elif zad == '4':
        fourth()
    else:
        exit(0)
