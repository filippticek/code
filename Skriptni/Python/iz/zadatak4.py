#!/usr/bin/python
import sys
import re

if len(sys.argv) != 2:
    sys.exit(1)

with open(sys.argv[1], 'r') as dat:
    da = dat.read()
    d = da.decode("utf8")

books = re.findall(r'<li>.*?</li>', d)
for book in books:
    m = re.match(r'<li>(.*?), <i>(.*?)</i>, (.*?)</li>', book)
    author = m.group(1)
    title = m.group(2)
    tmp = m.group(3).split(',')
    publisher = tmp[0]
    tp = tmp[1].split()
    year = tp[0]
    asd = tp[1]
    asd = asd[1:-1]
    print("@book{%s," % asd)
    print('    author = "{0}",'.format(author))
    print('    title = "{0}",'.format(title))
    print('    year = "{0}",'.format(year))
    print('    publisher = "{0}"'.format(publisher))
    print('}')
    print("")
