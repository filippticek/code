import random
import numpy as np
import scipy.stats as stat
from discreteMarkovChain import markovChain
import time as t
from scapy.all import *
import matplotlib
import matplotlib.pyplot as plt

#Average time for a state 
RADIO = 1./51
VIDEO = 1./58
SOCIAL_MEDIA = 1./134

#Destionation IP and port
DESTINATION_IP = "localhost"
DESTINATION_PORT = 8000

data = { 0 : [[],[]],
         1 : [[],[]],
         2 : [[],[]]
    }

#Get interarrival time
def sample_radio_time():
    return stat.alpha.rvs(a=0.1, loc=-1.61, scale=2.45)

def sample_video_time():
    return stat.genhalflogistic.rvs(c=0.1, loc=-0.29, scale=17.68)

def sample_social_time():
    return stat.exponnorm.rvs(K=3457.7, loc=0.01, scale=0.5)

#Get packet size
def sample_radio_length():
    return stat.chi2.rvs(df=0.95, loc=110.0, scale=12.18)

def sample_video_length():
    return stat.genextreme.rvs(c=1.45, loc=1489.32, scale=24.12)

def sample_social_length():
    return stat.pearson3.rvs(skew=-3.2, loc=1324.81, scale=174.59)

#Generate packet data
def generate_network_data(traffic_size):
    #Substract header size
    return Raw(RandString(size=traffic_size - 50))

#Send packet
def generate_radio_traffic(traffic_size):
    network_data = generate_network_data(traffic_size)
    packet = IP(dst=DESTINATION_IP)/UDP(dport=DESTINATION_PORT, sport=5000)/network_data
    send(packet, verbose=0) 

def generate_video_traffic(traffic_size):
    network_data = generate_network_data(traffic_size)
    packet = IP(dst=DESTINATION_IP)/UDP(dport=DESTINATION_PORT, sport=6000)/network_data
    send(packet, verbose=0) 

def generate_social_traffic(traffic_size):
    network_data = generate_network_data(traffic_size)
    packet = IP(dst=DESTINATION_IP)/UDP(dport=DESTINATION_PORT, sport=7000)/network_data
    send(packet, verbose=0) 

#Sojourn time
def sample_from_rate(rate):
    if rate == 0:
        return 10000
    return random.expovariate(rate)

#Simulation
def simulate_cmc(Q, transition_count):
    Q = list(Q)  # In case a matrix is input
    state_space = range(len(Q))  # Index the state space
    time_spent = {s:0 for s in state_space}  # Set up a dictionary to keep track of time
    current_state = random.randrange(3)  # First state
    
    for _ in range(transition_count):

        sojourn = sample_from_rate(- Q[current_state][current_state]) / 10
        time = 0
        print("#######################") 
        print("CURRENT STATE TIME: %f" % sojourn)
        print("CURRENT STATE: %s" % state[current_state])
        #t.sleep(5)
        while time < sojourn:
            sampled_time = 0.
            
            if current_state == 0:
                sampled_time = sample_radio_time()
                sampled_length = int(sample_radio_length())
                generate_radio_traffic(sampled_length)

            elif current_state == 1:
                sampled_time = sample_video_time()
                sampled_length = int(sample_video_length())
                generate_video_traffic(sampled_length)

            else:
                sampled_time = sample_social_time()
                sampled_length = int(sample_social_length())
                generate_social_traffic(sampled_length)
            
            # ms -> s
            sampled_time = abs(sampled_time) / 1000
            
            #Correct sampled time if it crosses the time threshold
            if sampled_time + time >= sojourn:
                sampled_time = sojourn - time
            
            data[current_state][0].append(sampled_time * 1000)
            data[current_state][1].append(sampled_length)
            
            print("Sampled time: %f" % sampled_time)
            print("Traffic size: %d" % sampled_length)
            
            t.sleep(sampled_time)
            time += sampled_time 

        sojourn = time
        time_spent[current_state] += sojourn

        # Sample the transitions
        sojourn_times = [sample_from_rate(rate) for rate in Q[current_state][:current_state]]
        sojourn_times += [100000]  # An infinite sojourn to the same state
        sojourn_times += [sample_from_rate(rate) for rate in Q[current_state][current_state + 1:]]

        # Identify the next state
        next_state = min(state_space, key=lambda x: sojourn_times[x])
        current_state = next_state  # Transition

    pi = [time_spent[state] / sum(time_spent.values()) for state in state_space]  # Calculate probabilities
    print("##PROBABILITY")
    print(pi)
    print("##TIME SPENT")
    print(time_spent)

    return pi 

state = ["RADIO", "VIDEO", "SOCIAL_MEDIA"]
'''
#Define state machine
Q= [[0,0,0],[0,0,0],[0,0,0]]

#Generate transition rates
for i in range(3):
    probability = random.random()
    for j in range(3):
        if i == j:
            Q[i][j] = - state[i]
        else:
            Q[i][j] = state[i] * probability
            probability = 1 - probability
'''

Q = [[], [], []]
Q[0] = [-0.0196078431372549, 0.0026227642309271603, 0.016985078906327743]
Q[1] = [0.014030240457579134, -0.017241379310344827, 0.0032111388527656937]
Q[2] = [0.0012304579488692923, 0.006232228618294887, -0.007462686567164179]

print("##MATRIX##")
print(Q[0])
print(Q[1])
print(Q[2])

#Calculate stationary values
mc = markovChain(np.array(Q))
mc.computePi('linear')
print("##STATIONARY")
print(mc.pi)

#Begin simulation
simulate_cmc(Q, 10)

#Histogram for interarrival time 
plt.figure(figsize=(12,8))
radio_time  = plt.hist(data[0][0], bins=100)
video_time  = plt.hist(data[1][0], bins=100)
social_time = plt.hist(data[2][0], bins=100)

#Histogram for packet length
plt.figure(figsize=(12,8))
radio_length  = plt.hist(data[0][1], bins=100)
video_length  = plt.hist(data[1][1], bins=100)
social_length = plt.hist(data[2][1], bins=100)


plt.show()
