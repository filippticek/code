#!/usr/bin/python3
import sys
from scapy.all import *
import time

min_time = 1000
max_time = 0
total_time = 0
packets_transmitted = 10
packets_received = 0

for _ in range(packets_transmitted):
    start_time = time.time()
    packet = IP(dst=sys.argv[1])/ICMP()
    answer = sr1(packet, verbose=0, timeout=4)
    rtt = time.time() - start_time 
    
    if answer is None:
        print("Timeout")
    else:
        print(answer.src + ": time=%.3fms" % rtt )
        if rtt > max_time: max_time = rtt
        if rtt < min_time: min_time = rtt 
        packets_received += 1
        total_time += rtt

print("%d packets transmitted, " % packets_transmitted + "%d packets received" % packets_received)
print("rtt min/max/avg = %.3f/%.3f/%.3f" % (min_time, max_time, total_time / packets_received))
