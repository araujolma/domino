#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:31:29 2018

@author: levi

Main file for domino project.
"""


# from game import match

# match()
# pts = match.play()

from game import champ
from play import msgr

thisMsgr = msgr(InptLang='por')
champ(compSttg=['basic', 'rand', 'basic'], msgr=thisMsgr)
