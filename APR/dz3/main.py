from sys import stdin, argv, maxsize
from random import uniform
import math


k = 0.5 * (math.sqrt(5) - 1)

def golden_cut(f_id, lamb, grad, a=None, b=None, x0=None, h=0.1, eps=1e-6, print_step=False):
    f = f_id
    x = list(x0)

    if a == None and b == None and x0:
        a, b = unimodal_interval(h, x0, f_id, lamb, grad) 
    elif a== None and b == None and x0 == None:
        exit(1)

    c = b - k * (b - a) 
    d = a + k * (b - a) 
    
    C = [x[0] + c * grad[0], x[1] + c * grad[1]]
    D = [x[0] + d * grad[0], x[1] + d * grad[1]]

    fc = f.calc(C)
    fd = f.calc(D)

    count_step = 0

    while (b - a) > eps:
       
        if print_step:
            print("Step: %3d | C: %s | D: %s" 
                    % (count_step, C, D))
        count_step += 1

        if fc < fd:
            b = d
            d = c
            c = b - k * (b - a) 
            C = [x[0] + c * grad[0], x[1] + c * grad[1]]
            fd = fc
            fc = f.calc(C)

        else:
            a = c
            c = d
            d = a + k * (b - a) 
            D = [x[0] + d * grad[0], x[1] + d * grad[1]]
            fc = fd
            fd = f.calc(D)

    return (a + b) / 2 

def unimodal_interval(h, x0, f_id, lamb, grad):
    x = list(x0)
    l = lamb - h 
    r = lamb + h 
    m = lamb
    step = 1

    L = [x[0] + l * grad[0], x[1] + l * grad[1]]
    R = [x[0] + r * grad[0], x[1] + r * grad[1]]
    M = [x[0] + r * grad[0], x[1] + r * grad[1]]
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
            r = lamb + h * step
            R = [x[0] + r * grad[0], x[1] + r * grad[1]]
            fr = f.calc(R)
    else:
        while fm > fl:
            r = m
            m = l
            fm = fl
            step *= 2
            l = lamb - h * step
            L = [x[0] + l * grad[0], x[1] + l * grad[1]]
            fl = f.calc(L)

    return l, r

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

def gradient_desc(x0, f_id, eps=1e-6, golden=True):
    f = f_id
    x = list(x0)
    grad = f.grad(x)
    iterations = 0
    bestIteration = f.calc(x)
    f.reduce_count(1)
     
    while math.sqrt(grad[0] ** 2 + grad[1] ** 2) > eps and iterations < 100:
        v = [-grad[0], -grad[1]]
        if golden:
            lambda_min = golden_cut(f, 0, v, x0=x, h=0.1, eps=eps)
            x = [x[0] + lambda_min * v[0], x[1] + lambda_min * v[1]]
        else:
            x = [x[0] + v[0], x[1] + v[1]]

        grad = f.grad(x)
        
        if f.calc(x) < bestIteration and abs(f.calc(x) - bestIteration) > eps:
            iterations = 0
            bestIteration = f.calc(x)
        else:
            iterations += 1
        f.reduce_count(3)

    return x

def newton_raphson(x0, f_id, eps=1e-6, golden=True):
    f = f_id
    x = list(x0)
    grad = f.grad(x)
    iterations = 0
    bestIteration = f.calc(x)
    f.reduce_count(1)

    while math.sqrt(grad[0] ** 2 + grad[1] ** 2) > eps and iterations < 100:
        inv_hesse = f.inverse_hesse(x)
        inv_multi_grad = [row[0] * grad[0] + row[1] * grad[1] for row in inv_hesse]
        norm = math.sqrt(inv_multi_grad[0] ** 2 + inv_multi_grad[1] ** 2)
        v = [- xi / norm for xi in inv_multi_grad]
        if golden:
            lambda_min = golden_cut(f, 0, v, x0=x, h=0.1, eps=eps)
            x = [x[0] + lambda_min * v[0], x[1] + lambda_min * v[1]]
        else:
            x = [x[0] + v[0], x[1] + v[1]]

        grad = f.grad(x)

        if f.calc(x) < bestIteration and abs(f.calc(x) - bestIteration) > eps:
            iterations = 0
            bestIteration = f.calc(x)
        else:
            iterations += 1
        f.reduce_count(3)

    return x

def box(x0, f_id, eps=1e-6, alfa=1.3, implicit=[], explicit=[-maxsize, maxsize]):
    x = list([x0])
    f = f_id
    XC = centroid(x)
    
    #Get points
    for i in range(len(x0)*2):
        x_temp = [0,0]
        for j in range(len(x0)):
           x_temp[j] = uniform(explicit[0], explicit[1]) 
        
        test = True
        while test:
            for impl in implicit:
                if impl.test(x_temp) < 0:
                    x_temp = [0.5 * (x + y) for x, y in zip(XC, x_temp)]
                    test = True
                    break
                else:
                    test = False

        x.append(x_temp)
        XC = centroid(x)

    iterations = 0
    bestIteration = f.calc(XC)
    f.reduce_count(1)

    while True and iterations < 100: 
        n = len(x)
        
        #Get worst and second worst point
        fX = [f.calc(xi) for xi in x]
        H = 0
        H2 = 0
        for i in range(n):
            if fX[i] > fX[H]:
                H2 = H
                H = i
        
        #Calculate centroid
        XC = centroid(x, h=H)

        #Calculate reflection
        XR = [(1 + alfa) * xc - alfa * xh for xc, xh in zip(XC, x[H])]

        #Place the point within explicit limits
        if XR[0] < explicit[0]:
            XR[0] = explicit[0]
        if XR[1] > explicit[1]:
            XR[1] = explicit[1] 
        #Implicit tests
        test = True
        while test:
            for impl in implicit:
                if impl.test(XR) < 0:
                    XR = [0.5 * (xc + xr) for xc, xr in zip(XC, XR)]
                    test = True
                    break
                else:
                    test = False

        if f.calc(XR) > fX[H2]:
            XR = [0.5 * (xc + xr) for xc, xr in zip(XC, XR)]

        x[H] = list(XR)

        if f.calc(XC) < bestIteration and abs(f.calc(XC) - bestIteration) > eps:
            iterations = 0
            bestIteration = f.calc(XC)
        else:
            iterations += 1
        f.reduce_count(3)


        substraction = [xi[0] - XC[0] for xi in x]
        norm = math.sqrt(sum([sub * sub for sub in substraction]))
        if norm > eps:
            continue
        else:
            break

    return XC

def centroid(x, h=-1):
    n = len(x)
    xc = [0 for i in range(len(x[0]))]
    for i in range(n):
        if i != h:
            xc = [xci + xi for xci, xi in zip(xc, x[i])]
    if h != -1:
        n -= 1
    return [xci / n for xci in xc]

def mixed_transform(x0, f_id, eps=1e-6, t=1, implicit_neq=[], implicit_eq=[]):
    f = f_id
    x = list(x0)
    u = Mixed_transform(f, implicit_neq=implicit_neq, implicit_eq=implicit_eq, t=1)
    

    #Implicit tests if x0 is a inner point
    test = True
    for neq in implicit_neq:
        if neq.test(x) < 0:
            test = False
            break
    
    if not test:
        fip = Find_inner_point(implicit_neq, t=1)
        x = hooke_jeeves(x0, fip)
        print("Inner point found %s" % (str(x)))
    
    while True:
        u.set_t(t)
        x_m = hooke_jeeves(x, u)

        substraction = [xi - xm for xi, xm in zip(x, x_m)]
        norm = math.sqrt(sum([sub * sub for sub in substraction]))
        x = list(x_m)

        if norm > eps:
            t *= 10
            continue
        else:
            break

    return x

class Find_inner_point:
    implicit_neq = []
    t = 1

    def __init__(self, implicit_neq=[], t=1):
        self.implicit_neq = implicit_neq
        self.t = t

    def calc(self, x):
        gx = 0
        for neq in self.implicit_neq:
            if neq.test(x) < 0:
                gx = gx - neq.test(x) 
        return gx

class Mixed_transform:
    f = 0
    implicit_neq = []
    implicit_eq = []
    t = 1

    def __init__(self, f, implicit_neq=[], implicit_eq=[], t=1):
        self.f = f
        self.implicit_neq = implicit_neq
        self.implicit_eq = implicit_eq
        self.t = t

    def set_t(self, t):
        self.t = t
    
    def calc(self, x):
        fx = self.f.calc(x)
        gx = 0
        for neq in self.implicit_neq:
            neq_test = neq.test(x)
            if neq_test > 0:
                gx -= math.log(neq_test)
            elif neq_test == 0:
                gx -= maxsize
            else:
                gx += maxsize

        gx = gx / self.t

        hx = 0
        for eq in self.implicit_eq:
            hx += eq.test(x) ** 2
        hx = hx * self.t

        return fx + gx + hx

class Function:
    identity = 0
    count = 0 
    count_grad = 0
    count_hesse = 0
    x0 = 0

    def __init__(self, identity):
        self.identity = identity
        self.count = 0
        self.count_grad = 0
        self.count_hesse = 0

        if self.identity == 1:
            self.x0 = [-1.9, 2]
        elif self.identity == 2:
            self.x0 = [0.1, 0.3]
        elif self.identity == 3:
            self.x0 = [0.0, 0.0]
        elif self.identity == 4:
            self.x0 = [0.0, 0.0]


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

    def raise_count_grad(self):
        self.count_grad += 1

    def reduce_count_grad(self, substract):
        self.count_grad -= substract
    
    def get_count_grad(self):
        return self.count_grad

    def raise_count_hesse(self):
        self.count_hesse += 1

    def reduce_count_hesse(self, substract):
        self.count_hesse -= substract
    
    def get_count_hesse(self):
        return self.count_hesse

    def get_count_grad(self):
        return self.count_grad

    def get_count_hesse(self):
        return self.count_hesse

    def grad(self, x):
        self.raise_count_grad()
        if self.identity == 1:
            return self.f1_grad(x)
        elif self.identity == 2:
            return self.f2_grad(x)
        elif self.identity == 3:
            return self.f3_grad(x)
        elif self.identity == 4:
            return self.f4_grad(x)

    def hesse(self, x):
        self.raise_count_hesse()
        if self.identity == 1:
            return self.f1_hesse(x)
        elif self.identity == 2:
            return self.f2_hesse(x)
        elif self.identity == 3:
            return self.f3_hesse(x)
        elif self.identity == 4:
            return self.f4_hesse(x)
    
    def f1_hesse(self,x):
        return [[1200 * x[0] ** 2 - 400 * x[1] - 1, -400 * x[0]],
                [-400 * x[0], 200]]

    def f2_hesse(self,x):
        return [[2, 0],
                [0, 8]]

    def f3_hesse(self,x):
        return [[2, 0],
                [0, 2]]

    def f4_hesse(self,x):
        return [[2, 0],
                [0, 2]]

    def inverse_hesse(self, x):
        A = self.hesse(x)
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        return [[A[1][1] / det, - A[0][1] / det],
                [-A[1][0] / det, A[0][0]]]

    def f1_grad(self, x):
        return [-400 * x[0] * (x[1] - x[0] **2) - 2 - x[0], 200 * (x[1] - x[0] ** 2)]

    def f2_grad(self, x):
        return [2 * (x[0] - 4), 8 * (x[1] - 2)]

    def f3_grad(self, x):
        return [2 * (x[0] - 2), 2 * (x[1] + 3)] 

    def f4_grad(self, x):
        return [2 * (x[0] - 3), 2 * x[1]]

    def f1(self, x):
        return 100 * (x[1] - x[0] * x[0]) ** 2 + (1 - x[0]) ** 2

    def f2(self, x):
        return (x[0] - 4) ** 2 + 4 * (x[1] - 2) ** 2

    def f3(self, x):
        return (x[0] - 2) ** 2 + (x[1] + 3) ** 2

    def f4(self, x):
        return (x[0] - 3) ** 2 + (x[1]) ** 2

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

class Implicit:
    identity = 0

    def __init__(self, identity):
        self.identity = identity

    def test(self, x):
        if self.identity == 1:
            return self.f1(x)
        elif self.identity == 2:
            return self.f2(x)
        elif self.identity == 3:
            return self.f3(x)
        elif self.identity == 4:
            return self.f4(x)
        elif self.identity == 5:
            return self.f5(x)

    def f1(self, x):
        return x[1] - x[0] 

    def f2(self, x):
        return 2 - x[0] 

    def f3(self, x):
        return 3 - x[0] - x[1] 

    def f4(self, x):
        return 3 + 1.5 * x[0] - x[1] 

    def f5(self, x):
        return x[1] - 1 

def first():
    f_id = Function(3)

    print("Gradient descend with golden cut    | Xmin: %-45s | grad_count = %6d"
            % (str(gradient_desc(f_id.get_x0(), f_id, golden=True)), f_id.get_count_grad()))
    f_id.reduce_count_grad(f_id.get_count_grad())
    print("Gradient descend withouth golden cut| Xmin: %-45s | grad_count = %6d"
            % (str(gradient_desc(f_id.get_x0(), f_id, golden=False)), f_id.get_count_grad()))  
    

def second():
    f_id = [Function(1), Function(2)]
    x0 = [f.get_x0() for f in f_id]

    for procedure in [gradient_desc, newton_raphson]:
        for i in range(2):
            print("Procedura: %-17s | F%d | Xmin: %-45s | f_count = %6d | f_count_gradient = %6d | f_count_hesse = %6d "  
                    % (procedure.__name__, i + 1, str(procedure(x0[i], f_id[i], golden=True)), f_id[i].get_count(), f_id[i].get_count_grad(), f_id[i].get_count_hesse()))
            f_id[i].reduce_count(f_id[i].get_count())
            f_id[i].reduce_count_grad(f_id[i].get_count_grad())
            f_id[i].reduce_count_hesse(f_id[i].get_count_hesse())


def third():
    f_id = [Function(1), Function(2)]
    implicit = [Implicit(1), Implicit(2)]

    for i in range(2):
        print("Box | F%d | Xmin: %-45s | f_count %6d | " 
                % (i+1, str(box(f_id[i].get_x0(), f_id[i], implicit=implicit, explicit=[-100, 100])), f_id[i].get_count()))
        f_id[i].reduce_count(f_id[i].get_count())

def fourth():
    f_id = [Function(1), Function(2)]
    implicit = [Implicit(1), Implicit(2)]

    for i in range(2):
        print("Mixed transformation | X0 = %-10s | F%d | Xmin: %-45s | f_count= %6d" 
            % (str(f_id[i].get_x0()), i+1, str(mixed_transform(f_id[i].get_x0(), f_id[i], t=1, implicit_neq=implicit)), f_id[i].get_count()))
        f_id[i].reduce_count(f_id[i].get_count())

    x0 = [2,2]
    for i in range(2):
        print("Mixed transformation | X0 = %-10s | F%d | Xmin: %-45s | f_count= %6d" 
            % (str(x0), i+1, str(mixed_transform(x0, f_id[i], t=1, implicit_neq=implicit)), f_id[i].get_count()))
        f_id[i].reduce_count(f_id[i].get_count())

def fifth():
    f_id = Function(4)
    implicit_neq = [Implicit(3), Implicit(4)]
    implicit_eq = [Implicit(5)]
    x0 = [5,5]
    
    print("Mixed transformation | X0 = %-10s | F4 | Xmin: %-45s | f_count= %6d" % 
            (str(x0), str(mixed_transform(x0, f_id, t=1, implicit_neq=implicit_neq, implicit_eq=implicit_eq)), f_id.get_count()))

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


