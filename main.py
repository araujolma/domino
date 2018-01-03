#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:31:29 2018

@author: levi

Main file for domino project.
"""

#import game
#
#domino = game.domino()
#table = game.table()
#
#print(domino.piecList)

from game import match


print("\nAtenção: jogo ainda não está ok!")
print("Caso se possa jogar de duas formas distintas, o jogo ignora isso!!")
input("\nPressione alguma coisa para continuar!")
match()