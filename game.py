#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:58:05 2018

@author: levi
"""
from play import player, domino
import random



class table():
    """Class table acts as both the table itself, holding the history of 
    played pieces, as well as the dealer, asking the players to play."""

    
    def __init__(self,starts=-1):
        
        
        self.starts = starts
        self.piecHist = []
        self.currPiec = None      
        
        # Declare players, set their hands
        self.players = []
        newHands = []
        for ind in range(28):
            newHands.append(ind)
        random.shuffle(newHands)
        
        ind = 0
        isAutoList = [False,True,True,True]
        for playInd in range(4):
            pHand = newHands[ind:ind+7]
            pHand.sort()
            p = player(plNumb=playInd, isAuto=isAutoList[playInd],hand=pHand)
            self.players.append(p)
            ind += 7
        print(newHands)
        print("\nPieces dealt.")
        
        # If there is no one to start, find who has the [6,6] (piece #27)
        if starts == -1:
            keepLook = True
            playInd = -1
            while keepLook and playInd < 4:
                playInd += 1 
                pHand = self.players[playInd].hand
                if 27 in pHand:
                    keepLook = False
            self.starts = playInd
            print("\nPlayer #" + str(self.starts) + " will begin.\n")
        #
        
        self.plays = self.starts
            
    def play(self,isFirst=False):
        """ Put the players to play! """
        
        print("\nIn table.play.")

        dom = domino()
                
        pl = self.players[self.plays]
        piec,posi,ornt = pl.play(self.currPiec,self.piecHist,play27=isFirst)
        
        self.piecHist.append(piec)

        if piec is not None:
            if self.currPiec is None:
                self.currPiec = piec
            else:
                # update current piece
                
                piecPair = dom.getPiecPair(piec)
                currPiecPair = dom.getPiecPair(self.currPiec)
                
                if ornt:
                    # True orientation: 
                    # greater side exposed, lesser side replaced
                    ppIndx = 1
                else:
                    # False orientation: 
                    # lesser side exposed, greater side replaced
                    ppIndx = 0
                    
                if posi == 0:
                    # left position. Replace lesser side
                    currPiecPair[0] = piecPair[ppIndx]
                else:
                    # right position. Replace greater side
                    currPiecPair[1] = piecPair[ppIndx]

                self.currPiec = dom.getPiecNum(currPiecPair)
        
        # Find out if player has won
        if len(pl.hand) == 0:
            win = self.plays % 2
        else:
            # Deadlock test
            if len(self.piecHist) > 4 and \
                (self.piecHist[-1] is None) and \
                (self.piecHist[-2] is None) and \
                (self.piecHist[-3] is None) and \
                (self.piecHist[-4] is None):
                ptOdd, ptEvn = 0, 0
                for indPl in range(4):
                    for ind in self.players[indPl].hand:
                        pair = dom.getPiecPair(ind)
                        if indPl % 2 == 0:
                            ptEvn += (pair[0]+pair[1])
                        else: 
                            ptOdd += (pair[0]+pair[1])

                # TODO: solve the tie condition in a less biased way
                if ptEvn <= ptOdd:
                    win = 0
                elif ptOdd < ptEvn:
                    win = 1
                    
            else:
                 win = None   
            #
            
        # Next player to play
        self.plays = (self.plays+1) % 4
        
        return win

    def showAll(self):
        dom = domino()
        
        print('-'*80)
        print("\nThis is the current table:")
        for ind in self.piecHist:
            if ind is None:
                print(str(ind))
            else:
                print(str(ind) + ": " + str(dom.getPiecPair(ind)))

        cp = self.currPiec
        if cp is not None:
            print("\nThis is the current piece (state) in the table:")
            print(str(cp)+ " (" + str(dom.getPiecPair(cp)) + ")")

        print("\nThese are the players' hands:")
        for pl in range(4):
            p = self.players[pl]
            print("\n  Player #" + str(pl) + ":")
            handStr = ''
            for ind in range(len(p.hand)):
                handStr += str(dom.getPiecPair(p.hand[ind]))
                handStr += ', '
            print(handStr)
        

class match():
    """Class match plays a simple match."""

    def __init__(self,starts=-1):
        print('-'*80)
        print("\nNew match!")
        tab = table(starts=starts)
        tab.showAll()
        
        # First piece!
        tab.play(isFirst=True)
        tab.showAll()
        
        keepPlay = True
        while keepPlay:
            win = tab.play()
            tab.showAll()
            if win is not None:
                keepPlay = False
        print("\n\n\nGAME FINISHED!")
        if win % 2 == 0:
            print("\n    EVEN team wins!")
            print("\nCONGRATULATIONS!!")
        else:
            print("\n    ODD team wins!")
            print("\nSorry, you lost!")
    
    


        
class champ():
    """Class champ plays a championship."""
    
        


