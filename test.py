#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:06:07 2018

@author: levi
"""

#import game
#
#domino = game.domino()
#table = game.table()
#
#print("This is the piece list:")
#print(domino.piecList)
#
#print("\nThis is the compatibility map:")
#for i1 in range(28):
#    for i2 in range(i1+1,28):
#        print(str(domino.piecList[i1]) + " and " + \
#              str(domino.piecList[i2]) + ": " + \
#              str(domino.isComp(i1,i2)))

import random
r = range(28)
x = r.copy()
print("x =",x)
random.shuffle(x)
print("Shuffled x =",x)