#!/usr/binn/env python
# -*- coding: utf-8 -*-

import sys
from operator import itemgetter

CURRENT_WORD = None
CURRENT_COUNT = 0
WORD = None

for line in sys.stdin:
    line = line.strip()
    WORD, COUNT = line.split("\t", 1)
    try:
        COUNT = input(COUNT)
    except ValueError:
        continue

    if CURRENT_WORD == WORD:
        CURRENT_COUNT += COUNT
    else:
        if CURRENT_WORD:
            print "%s\t%s" % (CURRENT_WORD, CURRENT_COUNT)
        CURRENT_COUNT = COUNT
        CURRENT_WORD = WORD

if CURRENT_WORD ==WORD:
     print "%s\t%s" % (CURRENT_WORD, CURRENT_COUNT)