import sys
from scapy.all import *

print("Tracing route to: " + sys.argv[1])

for i in range(1, 32):
    start_time = time.time()
    packet = IP(dst=sys.argv[1], ttl=i)/ICMP()/"Filip Pticek" 
    answer = sr1(packet, verbose=0, timeout=4)
    rtt = time.time() - start_time 

    if answer is None:
        print("%2d" % i + " *********** Timeout") 
    elif answer.type == 3:
        print("Trace complete")
    else:
        print("%2d" % i + " " + answer.src + " RTT: %.3fms" % rtt) 
