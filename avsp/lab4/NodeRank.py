from sys import stdin
import numpy as np

def nodeRank(N, node_matrix, node_degree, beta, iteration_cap):
    rank_matrix = np.zeros((iteration_cap + 1, N))    
    
    for i in range(N):
        rank_matrix[0][i] = 1. / N

    for i in range(iteration_cap):
        
        for j in range(N):
            
            value = beta * rank_matrix[i][j] / node_degree[j]

            for k in range(node_degree[j]):
                rank_matrix[i + 1][node_matrix[j][k]] += value

        for j in range(N):
            rank_matrix[i + 1][j] += (1 - beta) / N

    return rank_matrix

node_matrix = []
node_degree = []

line = stdin.readline().strip().split(' ')
N = int(line[0])
beta = float(line[1])

for _ in range(N):

    line = stdin.readline().strip().split(' ')
    nodes = []

    for i in line:
        nodes.append(int(i))

    node_matrix.append(nodes) 
    node_degree.append(len(nodes))


line = stdin.readline().strip().split(' ')
Q = int(line[0])

query = []
iteration_cap = 0

for i in range(Q):

    line = stdin.readline().strip().split(' ')
    query.append((int(line[1]), int(line[0])))
    
    if int(line[1]) > iteration_cap:
        iteration_cap = int(line[1])

rank_matrix = nodeRank(N, node_matrix, node_degree, beta, iteration_cap)

for q in query:
    print("%.10f" % rank_matrix[q[0]][q[1]])
