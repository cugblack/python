#!/usr/bin/env python
# -*- coding: UTF-8 -*-

f = open("data.txt", "r")
str = f.read()

new = []
d = {}
# for n in sorted(str, key=lambda x: -x count):
#     print(n.ch, "=", n.count)
for n in str:
    if n not in new:
        new.append(n)

for i in new:
    a =str.count(i)
    d[i] = str.count(i)

print d




