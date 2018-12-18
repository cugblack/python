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

    a = str.count(i)

    d[i] = str.count(i)
#字典排序
#根据key升序排列
d = sorted(d.items(), key = lambda d:d[0] )
#根据key降序排列
# d = sorted(d.items(), key = lambda d:d[0] , reverse=True)
#根据value降序排列
# d = sorted(d.items(), key = lambda item:item[1] , reverse = True)
#根据value升序排列
# d = sorted(d.items(), key = lambda item:item[1])
print d




