from sys import stdin
from decimal import Decimal, ROUND_HALF_UP
import numpy as np

def filter(matrix, matrix_sub, vector_length, I, J, K):
    I -= 1 
    J -= 1 
    
    weight = dict()

    for i in range(len(matrix)):
        if i == I: continue

        array_product = np.dot(matrix_sub[I],matrix_sub[i])
        weight[i] = array_product / (vector_length[I] * vector_length[i])
   
    weight_score = []

    for key, value in weight.items():
        if value > 0 and matrix[key][J] != 0:
            weight_score.append((value,matrix[key][J]))

    sorted_weights = sorted(weight_score, reverse=True, key=lambda x: x[0])[:K]
    
    numerator = 0
    denominator = 0

    for value, score in sorted_weights:
       numerator += value * score 
       denominator += value

    recommend_score = numerator / denominator

    return recommend_score

def substractMatrix(matrix, avg, N, M):
    matrix_sub = []

    for i in range(N):
        row = []
        for j in range(M):
            if matrix[i][j] == 0:
                row.append(0)
            else:
                row.append(matrix[i][j] - avg[i])

        matrix_sub.append(row)

    return matrix_sub

def average(matrix):
    avg = [] 

    for row in matrix:
        sm = 0
        count = 0

        for item in row:
            if item > 0:
                sm += item
                count += 1
            
        avg.append(sm / count)

    return avg

def vectorLength(matrix):
    vector_length = []
    for row in matrix:
        vector_length.append(np.sqrt(np.sum(np.square(row))))

    return vector_length

N, M = [int(i) for i in stdin.readline().strip().split(' ')]

matrix_item = []
matrix_user = [] 

for i in range(N):
    values = np.array(stdin.readline().strip().split(' '))
    values[values == 'X'] = 0
    values = values.astype(np.float)
    matrix_user.append(values)
    
matrix_item = np.transpose(matrix_user)

average_item = average(matrix_item)
average_user = average(matrix_user)

matrix_sub_item = substractMatrix(matrix_item, average_item, M, N)
matrix_sub_user = substractMatrix(matrix_user, average_user, N, M)

vector_length_item = vectorLength(matrix_sub_item)
vector_length_user = vectorLength(matrix_sub_user)

Q = int(stdin.readline().strip().split(' ')[0])

for i in range(Q):
    I, J, T, K = [int(x) for x in stdin.readline().strip().split(' ')] 
    
    if T == 0:
        print(Decimal(Decimal(filter(matrix_user, matrix_sub_user, vector_length_user, I, J, K)).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)))
    else:
        print(Decimal(Decimal(filter(matrix_item, matrix_sub_item, vector_length_item, J, I, K)).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)))
