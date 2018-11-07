#!/usr/binn/env python
# -*- coding: utf-8 -*-
import sys

lines = ['test cug bgi cug' ]

# for line in sys.stdin:
for line in lines:
    line = line.strip()
    words = line.split(" ")
    for word in words:
        print "%s \t %s" % (word, 1)