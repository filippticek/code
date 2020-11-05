from sys import stdin

def bfs(visited, queue, dist):
    
    if dist > 10 or not queue:
        return (-1, -1)

    visit_next = []

    for node in queue:
        
        
        if nodes[node] == 1:
            return node, dist

        for next_node in matrix[node]:
            
            if next_node in visited:
                continue
            elif next_node in queue:
                continue
            elif next_node in dead_nodes:
                continue
            else:
                visit_next.append(next_node)

        visited.append(node)

    visited.sort()
    visit_next.sort()
    
    return bfs(visited, visit_next, dist + 1)



line = stdin.readline().strip().split(' ')
N = int(line[0])
e = int(line[1])

nodes = []
matrix = {}

for i in range(N):
    line = stdin.readline().strip().split(' ')
    node = int(line[0])
    nodes.append(node)

for i in range(e):
    line = stdin.readline().strip().split(' ')
    s = int(line[0])
    d = int(line[1])

    if s in matrix:
        matrix[s] += [d]
    else:
        matrix[s] = [d]

    if d in matrix:
        matrix[d] += [s]
    else:
        matrix[d] = [s]

dead_nodes = [] 

for i in range(N):

    b, dist = bfs([], [i], 0)
    
    if b  == -1:
        dead_nodes.append(b)

    print(b, dist)


