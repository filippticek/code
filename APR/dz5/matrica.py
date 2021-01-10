from copy import copy, deepcopy
from numbers import Number


class Matrica:
    array = []
    row_count = 0
    row_count = 0

    def __init__(self, data, from_file=False):
        self.array = []
        
        if from_file:
            read_from_file(self, data)
        else:
            for numbers in data:
                row = []
                for number in numbers:
                    row.append(float(number))
                self.array.append(row)    

            self.row_count = len(data)
            self.column_count = len(data[0])

    def get_dimension(self):
        return self.row_count
        
    def read_from_file(self, file_name):
        f = open(file_name, 'r')
        lines = f.readlines()

        for line in lines:
            row = []
            for number in line.strip().split(' '):
                row.append(float(number))

            self.array.append(row)

        self.row_count = len(self.array)
        self.column_count = len(self.array[0])

    def write_to_file(self, file_name):
        f = open(file_name, 'w')
        f.write(str(self))
        f.close()
    
    def transpose(self):
        matrix = []
        
        for j in range(self.column_count):
            new_row = []
            for i in range(self.row_count):
                new_row.append(self[i][j])
            matrix.append(new_row)
        return Matrica(matrix)

    def forward_substitution(self, vector):
        matrix = []

        if self.row_count != vector.row_count:
            raise TypeError("Matrix and vector dont have the same row count")

        for i in range(vector.row_count):
            total_sum = vector[i][0]
            for j in range(i):
                total_sum -= self[i][j] * matrix[j][0]
            matrix.append([total_sum])    
            
        return Matrica(matrix)

    def backwards_substitution(self, vector):
        matrix = [0] * vector.row_count

        if self.row_count != vector.row_count:
            raise TypeError("Matrix and vector dont have the same row count")

        for i in reversed(range(vector.row_count)):
            total_sum = vector[i][0]
            for j in range(i+1,vector.row_count):
                total_sum -= self[i][j]*matrix[j]

            total_sum /= self[i][i]
            matrix[i] = total_sum
        

        return Matrica([matrix]).transpose()

    def lu(self):
        if self. row_count != self.column_count:
            raise TypeError("Not a square matrix")

        for i in range(self.row_count - 1):
            for j in range(i+1, self.row_count):
                try:
                    self[j][i] = self[j][i] * 1/self[i][i]
                except ZeroDivisionError:
                    raise ZeroDivisionError("Divison by zero")

                for k in range(i+1, self.row_count):
                    self[j][k] -= self[j][i] * self[i][k]

        L = []
        U = []
        for i in range(self.row_count):
            new_row_L = []
            new_row_U = []
            for j in range(self.row_count):
                new_row_U.append(self[i][j] if i<=j else 0)
                if i > j:
                    new_row_L.append(self[i][j])
                else:
                    new_row_L.append(1 if i==j else 0)
            L.append(new_row_L)
            U.append(new_row_U)

        return Matrica(L), Matrica(U)

    def lup(self):
        if self.row_count != self.column_count:
            raise TypeError("Not a square matrix")
        p = []
        for i in range(self.row_count):
            new_row = []
            for j in range(self.row_count):
                new_row.append(1 if i==j else 0)
            p.append(new_row)
        p = Matrica(p)
       
        count_permutations = 0
        for i in range(self.row_count - 1):
            pivot = i
            
            for j in range(i+1, self.row_count):
                if abs(self[j][i]) > abs(self[pivot][i]):
                    pivot = j
            if i != pivot:
                p[i], p[pivot] = p[pivot], p[i]
                self[i], self[pivot] = self[pivot], self[i]
                count_permutations += 1

            for j in range(i+1, self.row_count):
                try:
                    self[j][i] = self[j][i] / self[i][i]
                except ZeroDivisionError:
                    raise ZeroDivisionError("Divison by zero")
                
                for k in range(i+1,self.row_count):
                    self[j][k] -= self[j][i] * self[i][k]
        
        L = []
        U = []
        for i in range(self.row_count):
            new_row_L = []
            new_row_U = []
            for j in range(self.row_count):
                new_row_U.append(self[i][j] if i<=j else 0)
                if i > j:
                    new_row_L.append(self[i][j])
                else:
                    new_row_L.append(1 if i==j else 0)
            L.append(new_row_L)
            U.append(new_row_U)

        return Matrica(L), Matrica(U), Matrica(p.array), count_permutations

    def calculate_lup_determinant(self):
        _, U, _, count_permutations = self.lup()
        determinant = 1
        for i in range(self.row_count):
            determinant *= U[i][i]    

        if count_permutations % 2 == 1:
            determinant = -determinant

        return determinant
        

    """Operator overloads"""
    def __str__(self):
        str_array = ''
        for row in self.array:
            for number in row:
                str_array += (str(number) + ' ')
            str_array += '\n'
        return str_array[:-1]
    
    def __getitem__(self, key):
        return self.array[key]
    
    def __setitem__(self, key, value):
        self.array[key] = value
    
    def __eq__(self, other):
        if other == None:
            return False
        for i in range (self.row_count):
            for j in range(self.column_count):
                if abs(self[i][j] - other[i][j]) > pow(10, -6):
                    return False

        return True

    def __add__(self, other):
        matrix = []

        if isinstance(other, Number):
            for row in self.array:
                new_row = []
                for number in row:
                   new_row.append(number + other) 
                matrix.append(new_row)
        
        elif isinstance(other, Matrica):
            self.dimension_check(other)
            
            for i in range(self.row_count):
                new_row = []
                for j in range(self.column_count):
                    new_row.append(self[i][j] + other[i][j])
                matrix.append(new_row)

        else:
            raise TypeError("Wrong type")

        return Matrica(matrix)


    def __sub__(self, other):
        matrix = []

        if isinstance(other, Number):
            for row in self.array:
                new_row = []
                for number in row:
                   new_row.append(number - other) 
                matrix.append(new_row)
        
        elif isinstance(other, Matrica):
            self.dimension_check(other)
            
            for i in range(self.row_count):
                new_row = []
                for j in range(self.column_count):
                    new_row.append(self[i][j] - other[i][j])
                matrix.append(new_row)

        else:
            raise TypeError("Wrong type")

        return Matrica(matrix)

    def __mul__(self, other):
        matrix = []

        if isinstance(other, Number):
            for row in self.array:
                new_row = []
                for number in row:
                   new_row.append(number * other) 
                matrix.append(new_row) 
        
        elif isinstance(other, Matrica):
            if self.column_count != other.row_count:
                raise TypeError("Can't multiply. Different column and row counts")

            for i in range(self.row_count):
                new_row = [] 
                for j in range(other.column_count):
                    total_sum = 0
                    for k in range(self.column_count):
                        total_sum += self[i][k] * other[k][j]
                    new_row.append(float(total_sum))
                matrix.append(new_row)
        else:
            raise TypeError("Wrong type")

        return Matrica(matrix)
    
    def __neg__(self):
        matrix = []

        for row in self.array:
            new_row = []
            for number in row:
                new_row.append(-number)
            matrix.append(new_row)

        return Matrica(matrix)

    def __invert__(self):
        L,U,P, _ = self.lup()
       
        total = 1
        for i in range(self.row_count):
            total *= U[i][i]

        if abs(total) < pow(10, -6):
            raise TypeError("Matrix is singular")

        E = []
        for i in range(self.row_count):
            new_row = []
            for j in range(self.row_count):
                new_row.append(1 if i==j else 0)
            E.append(Matrica([new_row]).transpose())
            
        X = []    
        for i in range(self.row_count):
            y = L.forward_substitution(P * E[i])
            x = U.backwards_substitution(y)
            X.append(x)

        matrix = []
        for i in range(self.row_count):
            new_row = []
            for j in range(self.row_count):
                new_row.append(X[j][i][0])
            matrix.append(new_row)

        return Matrica(matrix)
                

    def dimension_check(self, other):
        if self.row_count != other.row_count:
            raise TypeError("Number of rows don't match")
        elif self.column_count != other.column_count:
            raise TypeError("Number of columns don't match")
"""
write_file = False
print("Prvi zadatak\n")

Prvi = Matrica([[3.123,2301203.414,6.12341],[4.101010,12.123,12.21347085],[1,-1,1]])
Prvi_kopija = Prvi
Prvi = Prvi * (1/1249081928409)
Prvi = Prvi * 1249081928409
print(Prvi == Prvi_kopija)

print("\nDrugi zadatak")
Drugi = Matrica([[3,9,6],[4,12,12],[1,-1,1]])
print("LU dekompozicija")
try:
    L, U = Drugi.lu()
except ZeroDivisionError as e:
    print(e)
print("\nLUP dekompozicija")
    L,U,P,_ =Drugi.lup()

y = L.forward_substitution(Matrica([[12],[12],[1]]))
x = U.backwards_substitution(y)
print("Rješenje sustava")
print(x)

print("\nTreći zadatak")
Treci = Matrica([[1,2,3],[4,5,6],[7,8,9]])

print("LU dekompozicija")
L,U = Treci.lu()
try:
    y = L.forward_substitution(Matrica([[12],[12],[1]]))
    x = U.backwards_substitution(y)
    print("Rješenje sustava")
    print(x)
except ZeroDivisionError as e:
    print("Division by zero")

print("\nLUP dekompozicija")
L,U,P,_ = Treci.lup()
try:
    y = L.forward_substitution(Matrica([[12],[12],[1]]))
    x = U.backwards_substitution(y)
    print("Rješenje sustava")
    print(x)
except ZeroDivisionError as e:
    print("Division by zero")

print("\nČetvrti zadatak")

Cetvrti = Matrica([[0.000001,3000000,2000000],[1000000,2000000,3000000],[2000000,1000000,2000000]])

print("LU dekompozicija")
L,U = Cetvrti.lu()
try:
    y = L.forward_substitution(Matrica([[12000000.000001],[14000000],[10000000]]))
    x = U.backwards_substitution(y)
    print("Rješenje sustava")
    print(x)
except ZeroDivisionError as e:
    print("Division by zero")

print("\nLUP dekompozicija")
L,U,P,_ = Cetvrti.lup()
try:
    y = L.forward_substitution(Matrica([[12000000.000001],[14000000],[10000000]]))
    x = U.backwards_substitution(y)
    print("Rješenje sustava")
    print(x)
except ZeroDivisionError as e:
    print("Division by zero")

print("\nPeti zadatak")
Peti = Matrica([[0,1,2],[2,0,3],[3,5,1]])

print("LU dekompozicija")
try:
    L,U = Peti.lu()
    y = L.forward_substitution(Matrica([[6],[9],[3]]))
    x = U.backwards_substitution(y)
    print("Rješenje sustava")
    print(x)
except ZeroDivisionError as e:
    print("Division by zero")

print("\nLUP dekompozicija")
try:
    L,U,P,_ = Peti.lup()
    y = L.forward_substitution(Matrica([[6],[9],[3]]))
    x = U.backwards_substitution(y)
    print("Rješenje sustava")
    print(x)
except ZeroDivisionError as e:
    print("Division by zero")

print("\nŠesti zadatak")

Sesti = Matrica([[4000000000,1000000000,3000000000],[4,2,7],[0.0000000003,0.0000000005,0.0000000002]])

print("LU dekompozicija")
try:
    L,U = Sesti.lu()
    y = L.forward_substitution(Matrica([[9000000000],[15],[0.0000000015]]))
    x = U.backwards_substitution(y)
    print("Rješenje sustava")
    print(x)
except ZeroDivisionError as e:
    print("Division by zero")

print("\nLUP dekompozicija")
try:
    L,U,P,_ = Sesti.lup()
    y = L.forward_substitution(Matrica([[6],[9],[3]]))
    x = U.backwards_substitution(y)
    print("Rješenje sustava")
    print(x)
except ZeroDivisionError as e:
    print("Division by zero")


print("\nSedmi zadatak")
Sedmi = Matrica([[1,2,3],[4,5,6],[7,8,9]])
try:
    ~Sedmi
    print(Sedmi)
except TypeError as e:
    print(e)

print("\nOsmi zadatak")
Osmi = Matrica([[4,-5,-2],[5,-6,-2],[-8,9,3]])
print("Inverz:")
print(~Osmi)

print("\nDeveti zadatak")
Deveti = Matrica([[4,-5,-2],[5,-6,-2],[-8,9,3]])
print("Determinanta:")
print(Deveti.calculate_lup_determinant())

print("\nDeseti zadatak")
Deseti = Matrica([[3,9,6],[4,12,12],[1,-1,1]])
print("Determinanta:")
print(Deseti.calculate_lup_determinant())
"""
