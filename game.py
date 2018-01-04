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
        for plyrInd in range(4):
            pHand = newHands[ind:ind+6]
            pHand.sort()
            p = player(plNumb=plyrInd, isAuto=isAutoList[plyrInd],hand=pHand)
            self.players.append(p)
            ind += 6
        print(newHands)
        print("\nPieces dealt.")
        
        # If there is no one to start, find who has the [6,6] (piece #27)
        # If no one has this piece, then look for the [5,5], and so on, up to
        # the last possible double piece, [2,2]

        if starts == -1:
            startList = [27,25,22,18,13]
            thisDblIndx = 0
            keepLook = True
            while keepLook:# and thisDblIndx < 5:
#                print("\nSearching for",thisDblIndx,": piece",startList[thisDblIndx])
                plyrInd = 0
                while keepLook and plyrInd < 4:
#                    print("Searching in player "+str(plyrInd)+"'s hands.")
                    pHand = self.players[plyrInd].hand
#                    print(pHand)
                    if startList[thisDblIndx] in pHand:
                        keepLook = False
#                        print("Found it!")
                    else:
                        plyrInd += 1
                    #
                #
                if keepLook:
                    thisDblIndx += 1
                #
            #
            self.starts = plyrInd
            self.strtWith = startList[thisDblIndx]
            print("\nPlayer #" + str(self.starts) + " will begin.\n")
        #
        
        self.plays = self.starts
            
    def play(self,isFirst=False):
        """ Put the players to play! """

        dom = domino()
        win = None
        pl = self.players[self.plays]
        if not pl.isAuto:
            self.showTabl()
        if isFirst:
            move = pl.play(self.currPiec, self.piecHist, \
                           strtWith=self.strtWith)
        else:
            move = pl.play(self.currPiec, self.piecHist)
        piec, posi, ornt = move
        self.piecHist.append(piec)

        if piec is not None:
            # Player has played a proper piece
            
            if len(pl.hand) == 0:
                # this player has just finished the game!
                win = self.plays % 2
                
                self.specFnshTest(move)
            else:
                self.updtCurrPiec(move)
            #
        #
        
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
            print("\nDeadlock!")
            print("Even team:",ptEvn,"points, Odd team:",ptOdd,"points...")
            if ptEvn <= ptOdd:
                win = 0
            elif ptOdd < ptEvn:
                win = 1
            #
        #
            
        # Next player to play
        self.plays = (self.plays+1) % 4
        
        return win

    def updtCurrPiec(self,move):
        """Update current piece. """
        dom = domino()
        piec,posi,ornt = move
        
        if self.currPiec is None:
            self.currPiec = piec
        else:
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
        #
        
    def specFnshTest(self,move):
        print('\n' + '-'*80)
        print('Game finished!\n')
        dom = domino()

        piec, _, _ = move
        piecPair = dom.getPiecPair(piec)

        print("Final piece:",piecPair)
        # Test for final double piece
        if piecPair[0] == piecPair[1]:
            isCarr = True
        else: 
            isCarr = False
            
        print("Table state before last piece:",dom.getPiecPair(self.currPiec))
        # Test for finish at both ends
        compScor = dom.isComp(piec,self.currPiec)
        print(compScor)
        # 1 & 2, or 4 & 8
        isOne, isTwo, isFour, isEig = False, False, False, False
        if compScor % 2 == 1:
            isOne = True
            compScor -= 1
        if compScor % 4 == 2:
            isTwo = True
            compScor -= 2
        if compScor % 8 == 4:
            isFour = True
            compScor -= 4
        if compScor > 0:
            isEig = True
            
        print("isOne:",isOne)
        print("isTwo:",isTwo)        
        print("isFour:",isFour)
        print("isEig:",isEig)
        
        if (isTwo and isFour) or (isEig and isOne):
            bothSide = True
        else:
            bothSide = False

        # Final count for points        
        if isCarr:
            if bothSide:
                nPtsAdd = 4
                print("\n----- CRUZADO!! -----")
            else:
                nPtsAdd = 2
                print("\n----- CARROÇA!! -----")
        else:
            if bothSide:
                nPtsAdd = 3
                print("\n----- LAILOT!!  -----")
            else:
                nPtsAdd = 1
                print("\n----- SIMPLES!  -----")
        return nPtsAdd

    def showTabl(self):

        dom = domino()
        
        print('-'*80)
        print("\n-> This is the played history:")
        indPl = self.starts
        #print(indPl)
        for ind in self.piecHist:
            #print(ind)
            strPrnt = "Pl." + str(indPl) + ": "
            #print("strPrnt = '"+strPrnt+"'")
            
            if ind is None:
                strPrnt += "None"
            else:
                strPrnt += str(dom.getPiecPair(ind))
                strPrnt += " (" + str(ind) + ")"
            print(strPrnt)
            indPl = (indPl+1) % 4
        #
        cp = self.currPiec
        if cp is not None:
            print("\n-> This is the current piece (state) in the table:")
            print(str(cp)+ " (" + str(dom.getPiecPair(cp)) + ")")
        #
        print("\n-> These are the players' hands:")
        for pl in range(4):
            p = self.players[pl]
            print(" Pl." + str(pl) + ": " + str(len(p.hand)) + " pieces.")
        
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
        #tab.showAll()
        
        # First piece!
        tab.play(isFirst=True)
        #tab.showAll()
        
        win = None
        while win is None:
            win = tab.play()
            #tab.showAll()
        print("\n\n\nGAME FINISHED!")
        if win % 2 == 0:
            print("\n    EVEN team wins!")
            print("\nCONGRATULATIONS!!")
        else:
            print("\n    ODD team wins!")
            print("\nSorry, you lost!")
    
    


        
class champ():
    """Class champ plays a championship."""
    
        


