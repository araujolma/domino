#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:34:56 2018

@author: levi
"""

#class domino():
#    """Class domino holds the basics for the game: piece list, compatibility
#    test, etc."""
#    # Define list of pieces    
#    piecList = []
#    for i1 in range(7):
#        for i2 in range(i1,7):
#            piecList.append([i1,i2])
#    
#    def isComp(self,p1,p2):
#        
#        if self.piecList[p1][0] == self.piecList[p2][0] or \
#            self.piecList[p1][0] == self.piecList[p2][1] or \
#            self.piecList[p1][1] == self.piecList[p2][0] or \
#            self.piecList[p1][1] == self.piecList[p2][1]:
#            return True
#        else: 
#            return False
#
#    def getPiec(self,piecPair):
#        piecPair.sort()
#        num = 0
#        
#        for ind in range(6):
#            if piecPair[0] > ind:
#                num += 6-ind
#        num += piecPair[1]
#        
#        return num

class domino():
    """Class domino holds the basics for the game: piece list, compatibility
    test, etc."""
    
    def isComp(self,p1,p2):
        
        pp1 = self.getPiecPair(p1)
        pp2 = self.getPiecPair(p2)
        if pp1[0] == pp2[0] or pp1[0] == pp2[1] or \
            pp1[1] == pp2[0] or pp1[1] == pp2[1]:
            return True
        else: 
            return False

    def getPiecPair(self,piecNum):
        pair = [0,0]
        if piecNum < 7:
            pair[1] = piecNum
        elif piecNum < 13:
            pair[0] = 1
            pair[1] = piecNum - 6
        elif piecNum < 18:
            pair[0] = 2
            pair[1] = piecNum - 11
        elif piecNum < 22:
            pair[0] = 3
            pair[1] = piecNum - 15
        elif piecNum < 25:
            pair[0] = 4
            pair[1] = piecNum - 18
        elif piecNum < 27:
            pair[0] = 5
            pair[1] = piecNum - 20
        else:
            pair = [6,6]
            
        return pair
        
    def getPiecNum(self,piecPair):
        piecPair.sort()
        num = 0
        
        for ind in range(6):
            if piecPair[0] > ind:
                num += 6-ind
        num += piecPair[1]
        
        return num

class player():

    
    def __init__(self,plNumb, isAuto, hand, strat='basic'):
        self.plNumb = plNumb
        self.isAuto = isAuto
        self.strat = strat
        self.hand = hand
        
    def play(self,currPiec,piecHist,play27=False):
        dom = domino()
        
        # 
        playPiec = None
        
        # This is to start a match with the [6,6]. No choice here.
        if play27:
            playPiec = 27
        # For any other case...
        else:
            # This is for the beginning case (any piece is ok)
            if currPiec is None:
                psbl = self.hand
            else:
                # Get the possible pieces to play
                psbl = []
                
                for ind in self.hand:
                    if dom.isComp(ind,currPiec):
                        psbl.append(ind)
                    
            # HERE IS WHERE THE PLAYER MAKES THE CHOICE
            if len(psbl) > 0:                
                if self.isAuto:
                    
                    if self.strat == 'basic':
                        # Basic stategy: play the highest possible piece
                        playPiec = psbl[-1]
                    
                else:
                    # MANUAL MODE
                    keepAsk = True
                    while keepAsk:
                        print("\nChoose the piece to be played:")
                        for ind in range(len(psbl)):
                            strPrint = ' - ' + str(ind) + ' : '
                            strPrint += str(dom.getPiecPair(psbl[ind]))
                            strPrint += '(' + str(psbl[ind]) + ')'
        
                            print(strPrint)
                                                    
                        strChoice = input("  >> ")
                        try:
                            choice = int(strChoice)
                            isInt = True
                        except ValueError:
                            isInt = False
                        
                        if isInt and choice > -1 and choice <= len(psbl):
                            keepAsk = False
                        else:
                            print("Error while parsing input.")
                            print("Please try again.")
                    #
                    playPiec = psbl[choice]
                
        if playPiec is not None:
            print("\nPlayer #" + str(self.plNumb) + ": I've played piece " + \
                  str(dom.getPiecPair(playPiec)) + " (" + str(playPiec) + ")!")
            self.hand.remove(playPiec)
        else:
            print("Player #" + str(self.plNumb) + ": passon!")
            
        if self.isAuto:
            input("Press any key to continue...")
        
        return playPiec
