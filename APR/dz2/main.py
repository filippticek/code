from sys import stdin, argv
from random import uniform
import math


k = 0.5 * (math.sqrt(5) - 1)

def golden_cut(axis, f_id, a=None, b=None, x0=None, eps=1e-6, print_step=False):
    f = f_id

    if a == None and b == None and x0:
        a, b = unimodal_interval(0.1, x0, axis, f_id) 
    elif a== None and b == None and x0 == None:
        exit(1)

    c = b - k * (b - a) 
    d = a + k * (b - a) 
    
    C = list(x0)
    C[axis] = c
    D = list(x0)
    D[axis] = d

    fc = f.calc(C)
    fd = f.calc(D)

    count_step = 0

    while (b - a) > eps:
       
        if print_step:
            print("Step: %3d | f(a=%s): %10.5f | f(b=%s): %10.5f | f(c=%s): %10.5f | f(d=%s): %10.5f" 
                    % (count_step, str(a), f.calc(a), str(b), f.calc(b), str(c), fc, str(d), fd))
            f.reduce_count(2)
    
        count_step += 1

        if fc < fd:
            b = d
            d = c
            c = b - k * (b - a) 
            C[axis] = c
            fd = fc
            fc = f.calc(C)

        else:
            a = c
            c = d
            d = a + k * (b - a) 
            D[axis] = d
            fc = fd
            fd = f.calc(D)

    return (a + b) / 2 

def unimodal_interval(h, x0, axis, f_id):
    tocka = x0[axis]
    l = tocka - h 
    r = tocka + h 
    m = tocka
    step = 1

    L = list(x0)
    L[axis] = l
    R = list(x0)
    R[axis] = r

    f = f_id
    fm = f.calc(x0)
    fl = f.calc(L)
    fr = f.calc(R)

    if (fm < fr) and (fm < fl):
       return l, r 
    elif fm > fr:
        while fm > fr:
            l = m 
            m = r
            fm = fr
            step *= 2
            r = tocka + h * step
            R[axis] = r
            fr = f.calc(R)
    else:
        while fm > fl:
            r = m
            m = l
            fm = fl
            step *= 2
            l = tocka - h * step
            L[axis] = l
            fl = f.calc(L)

    return l, r

def coordinate_search(x0, f_id, eps=1e-6, print_step=False):
    x = list(x0)

    while True:
        xs = list(x)
        for i in range(len(x)):
            x[i] = golden_cut(i, f_id, x0=x, eps=eps, print_step=print_step)

        substraction = [x1 - x2 for x1, x2 in zip(x, xs)]
        norm = math.sqrt(sum([sub ** 2 for sub in substraction]))
        
        if norm <= eps:
            continue
        else:
            break
    return x 

def simplex(x0, f_id, eps=1e-6, alfa=1, beta=0.5, gamma=2, sigma=0.5, shift=1, print_step=False):
    x = list([x0])
    f = f_id
    
    #Calculate simplex points
    for i in range(len(x0)):
       x_shift = list(x0)
       x_shift[i] += shift
       x.append(x_shift)

    iteration = 0
    
    while True:
        iteration += 1

        #Get index h and l
        y = list(map(f.calc, x))
        h = y.index(max(y))
        l = y.index(min(y))

        #Centroid
        n = len(x)
        xc = [0 for i in range(len(x[0]))]
        for i in range(n):
            if i != h:
                xc = [xci + xi for xci, xi in zip(xc, x[i])]
        
        xc = [xci / (n - 1) for xci in xc]
        
        if print_step:
            print("Xc:", xc)
            print("F(Xc)=", f.calc(xc))
            f.reduce_count(1)

        #Reflection

        xr = [(1 + alfa) * xci - alfa * xhi for xci, xhi in zip(xc, x[h])]
        fxr = f.calc(xr)
        fxl = f.calc(x[l])

        if fxr < fxl:
            #Expansion
            xe = [(1 - gamma) * xci + gamma * xri for xci, xri in zip(xc, xr)]

            if f.calc(xe) < fxl:
                x[h] = list(xe)
            else:
                x[h] = list(xr)

        else:
            comparison = True
            for i in range(n):
                if i != h:
                    if fxr > f.calc(x[i]):
                        continue
                    else:
                        comparison = False
                        break
            
            if comparison:
                fxh = f.calc(x[h])
                if fxr < fxh:
                    x[h] = list(xr)

                #Contraction
                xk = [(1 - beta) * xci + beta * xhi for xci, xhi in zip(xc, x[h])]
                fxk = f.calc(xk)

                if fxk < fxh:
                    x[h] = list(xk)
                else:
                    #Shift to x[l]
                    for i in range(n): 
                        if i != l:
                            x[i] = [sigma * xij + (1 - sigma) * xlj for xij, xlj in zip(x[i], x[l])]

            else:
                x[h] = list(xr)
        
        #Break condition
        substraction = [f.calc(xi) - f.calc(xc) for xi in x]
        norm = math.sqrt(sum([sub * sub for sub in substraction]) / n)
        if norm > eps:
            continue
        else:
            break
    return x[0]

def hooke_jeeves(x0, f_id, dx=0.5, eps=1e-6, print_step=False):
    xp = list(x0)
    xb = list(x0)
    f = f_id
    step_count = 0

    while True:
        xn = explore(xp, dx, f_id) 

        fxb = f.calc(xb)
        fxn = f.calc(xn)
        
        if print_step:
            print("Step: %3d | F(Xb=%s)= %10.5f | F(Xp=%s)= %10.5f | F(Xn=%s): %10.5f" 
                % (step_count, str(xb), fxb, str(xp), f.calc(xp), str(xn), fxn))
            f.reduce_count(1)    
        
        step_count += 1

        if fxn < fxb:
           xp = [2 * xni - xbi for xni, xbi in zip(xn, xb)]
           xb = list(xn)
        
        else:
           dx /= 2 
           xp = list(xb)

        if dx < eps:
            break

    return xb

def explore(xp, dx, f_id):
    x = list(xp)
    f = f_id

    for i in range(len(x)):
        p = f.calc(x)
        x[i] += dx
        n = f.calc(x)

        if n > p:
            x[i] -= (2 * dx)
            n = f.calc(x)

            if n > p:
                x[i] += dx

    return x

class Function:
    identity = 0
    count = 0 
    x0 = 0

    def __init__(self, identity):
        self.identity = identity
        self.count = 0

        if self.identity == 1:
            self.x0 = [-1.9, 2]
        elif self.identity == 2:
            self.x0 = [0.1, 0.3]
        elif self.identity == 3:
            self.x0 = [0]
        elif self.identity == 4:
            self.x0 = [5.1, 1.1]
        elif self.identity == 6:
            self.x0 = 0


    def raise_count(self):
        self.count += 1

    def get_id(self):
        return self.identity

    def get_count(self):
        return self.count

    def reduce_count(self, substract):
        self.count -= substract

    def get_x0(self):
        return self.x0

    def f1(self, x):
        return 100 * (x[1] - x[0] * x[0]) ** 2 + (1 - x[0]) ** 2

    def f2(self, x):
        return (x[0] - 4) ** 2 + 4 * (x[1] - 2) ** 2

    def f3(self, x):
        total_sum = 0
        for xi, i in enumerate(x, start=1):
            total_sum += (xi - i) ** 2

        return total_sum

    def f4(self, x):
        return abs((x[0] - x[1]) * (x[0] + x[1])) + math.sqrt(x[0] * x[0] + x[1] * x[1])

    def f6(self, x):
        quadratic_sum = sum([xi * xi for xi in x])
        numerator = math.sin(math.sqrt(quadratic_sum)) ** 2 - 0.5
        denominator = (1 + 0.001 * quadratic_sum) ** 2

        return 0.5 + numerator / denominator

    def calc(self, x):
        self.raise_count()
        if self.identity == 1:
            return self.f1(x)
        elif self.identity == 2:
            return self.f2(x)
        elif self.identity == 3:
            return self.f3(x)
        elif self.identity == 4:
            return self.f4(x)
        elif self.identity == 6:
            return self.f6(x)


def first():
    f_id = Function(3)
    
    for x0 in [10, 30, 50]:
        print("X0: %s | F3" % (str([x0, 0, 0])))
        for procedure in [coordinate_search, simplex, hooke_jeeves]:
            print("Procedura: %-17s | Xmin: %-60s | f_count = %4d"  
                    % (procedure.__name__, str(procedure([x0, 0, 0], f_id)), f_id.get_count()))

            f_id.reduce_count(f_id.get_count())

def second():
    f_id = [Function(1), Function(2), Function(3), Function(4)]
    x0 = [f.get_x0() for f in f_id]
    x0[2] = x0[2] * 5

    for procedure in [simplex, hooke_jeeves, coordinate_search]:
        for i in range(4):
            print("Procedura: %-17s | F%d | Xmin: %-100s | f_count = %4d"  
                    % (procedure.__name__, i + 1, str(procedure(x0[i], f_id[i])), f_id[i].get_count()))
            f_id[i].reduce_count(f_id[i].get_count())


def third():
    f_id = Function(4)
    x0 = [5, 5]
    
    print("X0: %s | F4" % (str(x0)))
    for procedure in [hooke_jeeves, simplex]:
        print("Procedura: %-17s | Xmin: %-60s | f_count = %4d"  
                % (procedure.__name__, str(procedure(x0, f_id)), f_id.get_count()))
        f_id.reduce_count(f_id.get_count())

def fourth():
    f_id = Function(1)
    shifts = [i for i in range(1, 21)]
    x0 = [0.5, 0.5]
    print("X0: %s | F1" % (str(x0)))

    for shift in shifts:
        print("Procedura: simplex | shift: %2d | Xmin: %-40s | f_count = %4d"  
                % (shift, str(simplex(x0, f_id, shift=shift)), f_id.get_count()))
        f_id.reduce_count(f_id.get_count())
        
    x0 = [20, 20]     
    print("X0: %s | F1" % (str(x0)))

    for shift in shifts:
        print("Procedura: simplex | shift: %2d | Xmin: %-40s | f_count = %4d"  
                % (shift, str(simplex(x0, f_id, shift=shift)), f_id.get_count()))
        f_id.reduce_count(f_id.get_count())

def fifth():
    f_id = Function(6)
    count_found_fmin = 0
    max_steps = 10000
    x0 = [0, 0]
    procedure = simplex

    for i in range(max_steps):
        x0[0] = uniform(-50.0, 50.0)
        x0[1] = uniform(-50.0, 50.0)

        xmin = procedure(x0, f_id)

        if abs(f_id.calc(xmin)) < 1e-4:
            count_found_fmin += 1

    print("Procedura: %s | F6 | Iterations: %d" % (procedure.__name__, max_steps))
    print("Probability of finding fmin: %.2f%%" % (count_found_fmin * 100 / max_steps ))




while True:
    print("Choose between assignment 1-5 or 0 for exit.")
    zad = stdin.readline().strip()
    
    if zad == '1':
        first()
    elif zad == '2':
        second()
    elif zad == '3':
        third()
    elif zad == '4':
        fourth()
    elif zad == '5':
        fifth()
    else:
        exit(0)
