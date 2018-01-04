#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:34:56 2018

@author: levi
"""
import random

class domino():
    """Class domino holds the basics for the game: piece list, compatibility
    test, etc."""
    
    def isComp(self,handP,tablP):
        """Finds out if piece is compatible with the table's current state.
        
        It returns an integer with the sum of the possibilities for the given 
        piece:
        
        0 means no possibility,
        1 means the piece is appliable on the left (lesser) side, 
            with True orientation
        2 means the piece is appliable on the right (greater) side, 
            with True orientation
        4 means the piece is appliable on the left (lesser) side, 
            with False orientation
        8 means the piece is appliable on the right (greater) side, 
            with False orientation
    
        """
        
        handPP = self.getPiecPair(handP)
        tablPP = self.getPiecPair(tablP)
        
        NPsbl = 0
        
        if handPP[0] == tablPP[0]:
            NPsbl += 1

        if handPP[0] == tablPP[1]:
            NPsbl += 2

        if handPP[1] == tablPP[0]: 
            NPsbl += 4
    
        if handPP[1] == tablPP[1]:
            NPsbl += 8

        return NPsbl


    def getPiecPair(self,piecNum):
        """Get the pair of numbers that represent the piece (e.g., [0,0], 
        [2,3], [4,4], [5,6]]), given its piece number (e.g., 0, 14, 22, 26)."""

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
        """Gets the piece number (e.g., 0, 14, 22, 26) given the pair of 
        numbers that represent the piece (e.g., [0,0], [2,3], [4,4], [5,6])."""

        piecPair.sort()
        num = 0

        for ind in range(6):
            if piecPair[0] > ind:
                num += 6-ind
        num += piecPair[1]
        
        return num

class player():

    
    def __init__(self,plNumb, isAuto, hand, strat='rand'):
        self.plNumb = plNumb
        self.isAuto = isAuto
        self.strat = strat
        self.hand = hand
        
    def promUser(self,currPiec,psbl):
        """Prompt user for input, showing his/her possibilities.
        Returns the index for the possibilites list psbl."""
        
        dom = domino()
        currPiecPair = dom.getPiecPair(currPiec)

        keepAsk = True
        while keepAsk:
            print("\nThis is your hand:")
            hand = self.hand
            handStr = ''
            for ind in range(len(hand)):
                handStr += str(dom.getPiecPair(hand[ind]))
                handStr += ', '
            print(handStr)
            if len(psbl) == 1:
                print("\nThere is only one possibility:")
            else:
                print("\nChoose the piece to be played:")

            for ind in range(len(psbl)):
                piec,posi,ornt = psbl[ind]
                strPrnt = ' - ' + str(ind) + ' : '
                strPrnt += str(dom.getPiecPair(piec))
                strPrnt += '(' + str(piec) + ') in the '
                if posi == 0:
                    strPrnt += 'left position (by the '
                else:
                    strPrnt += 'right position (by the '

                strPrnt += str(currPiecPair[posi])
                strPrnt += ')'
                
                print(strPrnt)

            if len(psbl) == 1:
                print("Press any key to play it.")            
                input("  >> ")
                choice = 0
                keepAsk = False
            else:
                strChoice = input("  >> ")
                try:
                    choice = int(strChoice)
                    isInt = True
                except ValueError:
                    isInt = False
                
                if isInt and choice > -1 and choice < len(psbl):
                    keepAsk = False
                else:
                    print("Error while parsing input.")
                    print("Please try again.")
            #
        #
        return choice
        
    def getPsbl(self,currPiec):
        """Get the possibilities for playing."""
        dom = domino()
        psbl = []
                
        for ind in self.hand:
            # all the possibilities for this particular piece are encoded in 
            # psblIndx
            psblIndx = dom.isComp(ind,currPiec)
            piecPair = dom.getPiecPair(ind)
            if psblIndx > 0:
                if psblIndx % 2 == 1:
                    psbl.append([ind,0,True])
                    psblIndx -= 1
                if psblIndx % 4 == 2:
                    psbl.append([ind,1,True])
                    psblIndx -= 2
                if psblIndx % 8 == 4:
                    if piecPair[0] != piecPair[1]:
                        psbl.append([ind,0,False])
                    psblIndx -= 4
                if psblIndx > 0:
                    if piecPair[0] != piecPair[1]:
                        psbl.append([ind,1,False])
                #
            #
        #
        return psbl
        
        
    def play(self,currPiec,piecHist,strtWith=None):
        """This method chooses the piece to be played (if such piece exists), 
        its orientation and placement, and then removes the piece from the 
        player's hand (again, if it is the case). 
        
        Orientation is True for a lesser side fitting the table and exposing
        a greater side (e.g., placing a [2,3] at an end with an exposed 2)
        and False for the opposite. Of course, this makes no difference for 
        double pieces. 
        
        Position is either 0 or 1: 0 for the left (lesser) side, and 1 for the
        right (greater) side. Again, this makes no difference if the current 
        state is equivalent to a double piece, e.g., [4,4].
        """
        
        dom = domino()
        
        # This first part is concerned with choosing a piece to be played
        playPiec = strtWith
        
        posi = None
        ornt = None
        
        # This is to start a match with the [6,6]. No choice here.
        if strtWith is None:

            # This is for the beginning case, without a specific piece to begin
            # with. (That is, any piece is ok)
            if currPiec is None:
                psbl = self.hand
                # Orientation and position do not apply
            else:
                # Get the possible pieces to play
                psbl = self.getPsbl(currPiec)
                
                #print("Debug: calculated possibilities for player #",self.plNumb)
                #print(psbl)
                
            # HERE IS WHERE THE PLAYER MAKES THE CHOICE
            if len(psbl) > 0:                
                if self.isAuto:
                    
                    if self.strat == 'rand':
                        # Random stategy: play anything
                        playPiec,posi,ornt = random.choice(psbl)
                    if self.strat == 'basic':
                        # Basic stategy: play the highest possible piece
                        print("Not implemented yet!")
                    
                else:
                    # MANUAL MODE
                    choice = self.promUser(currPiec,psbl)
                    playPiec,posi,ornt = psbl[choice]
                
        if playPiec is not None:
            strPrnt = "\nPlayer #" + str(self.plNumb) + \
            ": I've played piece " + str(dom.getPiecPair(playPiec)) + " (" + \
            str(playPiec) + ") at the "
            if posi == 0:
                strPrnt += "left side!"
            else:
                strPrnt += "right side!"
            print(strPrnt)

            self.hand.remove(playPiec)
        else:
            print("Player #" + str(self.plNumb) + ": passon!")
            
#        if self.isAuto:
#            input("Press any key to continue...")
        
        return playPiec, posi, ornt
