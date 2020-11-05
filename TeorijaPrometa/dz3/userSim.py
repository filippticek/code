import random
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from discreteMarkovChain import markovChain

SOCIAL_MEDIA = 1./134
VIDEO = 1./58
GAMES = 1./51

data = [[],[],[]] 


def sample_from_rate(rate):
    if rate == 0:
        return 10000
    return random.expovariate(rate)

def simulate_cmc(Q, time):
    Q = list(Q)  # In case a matrix is input
    state_space = range(len(Q))  # Index the state space
    time_spent = {s:0 for s in state_space}  # Set up a dictionary to keep track of time
    current_state = random.randrange(3)  # First state
    
    for _ in range(time):
        # Sample the transitions
        sojourn_times = [sample_from_rate(rate) for rate in Q[current_state][:current_state]]
        sojourn_times += [100000]  # An infinite sojourn to the same state
        sojourn_times += [sample_from_rate(rate) for rate in Q[current_state][current_state + 1:]]

        # Identify the next state
        next_state = min(state_space, key=lambda x: sojourn_times[x])
        sojourn = sample_from_rate(- Q[current_state][current_state])
        time_spent[current_state] += sojourn
        data[current_state].append(sojourn)
        current_state = next_state  # Transition

    pi = [time_spent[state] / sum(time_spent.values()) for state in state_space]  # Calculate probabilities
    print("##PROBABILITY")
    print(pi)
    print("##TIME SPENT")
    print(time_spent)
    return pi

Q= [[0,0,0],[0,0,0],[0,0,0]]
state = [SOCIAL_MEDIA,VIDEO, GAMES]

for i in range(3):
    probability = random.random()
    for j in range(3):
        if i == j:
            Q[i][j] = - state[i]
        else:
            Q[i][j] = state[i] * probability
            probability = 1 - probability

print("##MATRIX##")
print(Q[0])
print(Q[1])
print(Q[2])

mc = markovChain(np.array(Q))
mc.computePi('linear')
print("##STATIONARY")
print(mc.pi)

simulate_cmc(Q, 10000)


#with open("state_time.csv","w+") as my_csv:
#    csvWriter = csv.writer(my_csv,delimiter=',')
#    csvWriter.writerows(data)

x = np.sort(data[0])
y = np.arange(len(x))/float(len(x))
plt.plot(x, y, 'b')

x = np.sort(data[1])
y = np.arange(len(x))/float(len(x))
plt.plot(x, y, 'r')

x = np.sort(data[2])
y = np.arange(len(x))/float(len(x))
plt.plot(x, y, 'g')

#n, bins, patches = plt.hist(U1,bins=50, density=1,facecolor='red', alpha=0.5, label='User distribution')
#plt.hist(data[0],bins=50,density=True, facecolor='red',histtype='step', cumulative=True)
#plt.hist(data[1],bins=50,density=True, facecolor='green',histtype='step', cumulative=True)
#plt.hist(data[2],bins=50,density=True, facecolor='blue',histtype='step', cumulative=True)
#

plt.show()






