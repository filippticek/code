#!/usr/bin/python
import sys
import re
import urllib.request

stranica = urllib.request.urlopen("https://www.fer.unizg.hr")
mybytes = stranica.read()
mystr = mybytes.decode("utf8")

hosts = {}
href = re.findall(r'href="http.*?"', mystr)
for h in href:
    m = re.search(r'https?://(www\.)?((.*?)(/.*)?)"', h)
    url = m.group(2)
    host = m.group(3)
    print(url)
    if host in hosts:
        hosts[host] += 1
    else:
        hosts[host] = 1

for host in hosts.keys():
    print("%3d %s" % (hosts[host], host))

mailovi = re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', mystr)
for mail in mailovi:
    print(mail)

print(len(re.findall(r'<img src=".*?>', mystr)))
