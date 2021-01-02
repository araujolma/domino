#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:58:05 2018

@author: levi
"""
from play import player, domino
import random
import numpy


class table:
    """Represents the table.

    Class table acts as both the table itself, holding the history of
    played pieces, as well as the dealer, asking the players to play.
    """

    def __init__(self, compSttg, starts=-1, msgr=None):

        self.starts = starts
        self.strtWith = None
        self.nPtsAdd = 1
        self.piecHist = []
        self.currPiec = None
        self.msgr = msgr
        self.hasNot = numpy.zeros((4, 7), dtype=bool)

        # Declare players, set their hands
        self.players = []

        newHands = []
        for ind in range(28):
            newHands.append(ind)
        random.shuffle(newHands)

        ind = 0
        isAutoList = [False, True, True, True]
        for plyrInd in range(4):
            pHand = newHands[ind:ind + 6]
            pHand.sort()
            if isAutoList[plyrInd]:
                p = player(plNumb=plyrInd, hand=pHand,
                           isAuto=isAutoList[plyrInd],
                           sttg=compSttg[plyrInd - 1])
            else:
                p = player(plNumb=0, hand=pHand, isAuto=False)
            self.players.append(p)
            ind += 6
        self.msgr.prnt(newHands)

        self.msgr.prnt({'eng': "\nPieces dealt.",
                        'por': "\nPeças distribuídas."})

        # If there is no one to start, find who has the [6,6] (piece #27)
        # If no one has this piece, then look for the [5,5], and so on, up to
        # the last possible double piece, [2,2]

        if starts == -1:
            startList = [27, 25, 22, 18, 13]
            thisDblIndx = 0
            keepLook = True
            while keepLook:

                plyrInd = 0
                while keepLook and plyrInd < 4:

                    pHand = self.players[plyrInd].hand

                    if startList[thisDblIndx] in pHand:
                        keepLook = False

                    else:
                        plyrInd += 1
                    #
                #
                if keepLook:
                    msg = {'eng': "\nPiece " + str(startList[thisDblIndx]) +
                                  " is not in the players' hands." +
                                  "\nPress any key to continue...",
                           'por': "\nPedra " + str(startList[thisDblIndx]) +
                                  " não está nas mãos dos jogadores." +
                                  "\nPressione qualquer tecla " +
                                  "para continuar..."}
                    self.msgr.prnt(msg)

                    input("  >> ")
                    thisDblIndx += 1
                #
            #
            self.starts = plyrInd
            self.strtWith = startList[thisDblIndx]
        #
        self.msgr.prnt({'eng': "\nPlayer #" + str(self.starts) +
                               " will begin.\n",
                        'por': "\nJogador #" + str(self.starts) +
                               " vai começar.\n"})
        self.plays = self.starts

    def play(self, isFirst=False):
        """Put the players to play."""
        dom = domino()
        win = None
        pl = self.players[self.plays]
        if not pl.isAuto:
            self.showTabl()
        if isFirst:
            move = pl.play(self.currPiec, self.piecHist,
                           strtWith=self.strtWith, msgr=self.msgr)
        else:
            move = pl.play(self.currPiec, self.piecHist, msgr=self.msgr)
        piec, posi, ornt = move
        self.piecHist.append(piec)

        if piec is None:
            # no piece was played. Update the 'hasNot' arrays:
            thisPiecPair = dom.getPiecPair(self.currPiec)
            self.hasNot[self.plays, thisPiecPair[0]] = True
            self.hasNot[self.plays, thisPiecPair[1]] = True
        else:
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
                        ptEvn += (pair[0] + pair[1])
                    else:
                        ptOdd += (pair[0] + pair[1])

            # TODO: solve the tie condition in a less biased way
            self.msgr.prnt({'eng': "\nDeadlock!",
                            'por': "\nTravou!"})
            self.showAll()
            self.msgr.prnt({'eng': "\nEven team: " + str(ptEvn) +
                                   " points, Odd team: " + str(ptOdd) +
                                   " points...",
                            'por': "\nTime par: " + str(ptEvn) +
                                   " pontos, Time ímpar: " + str(ptOdd) +
                                   " pontos..."})
            if ptEvn <= ptOdd:
                win = 0
            elif ptOdd < ptEvn:
                win = 1
            #
        #

        # Next player to play
        self.plays = (self.plays + 1) % 4

        return win

    def updtCurrPiec(self, move):
        """Update current piece.

        Updates the table's .currPiec attribute and returns None.
        """
        dom = domino()
        piec, posi, ornt = move

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

    def specFnshTest(self, move):
        """Check for special finishings.

        Special finishings are:
            - "carroça": for finishing with a double piece such as [3,3];
                         (this yields 2 points)
            - "lailot": for finishing at both ends simultaneously;
                         (this yields 3 points)
            - "cruzado": for finishing with a double piece at both ends;
                         (this yields 4 points)

        """
        self.msgr.prnt({'eng': "\nDONE!", 'por': "\nBATI!"})
        dom = domino()

        piec, _, _ = move
        piecPair = dom.getPiecPair(piec)

        # Test for final double piece
        if piecPair[0] == piecPair[1]:
            isCarr = True
        else:
            isCarr = False

        # Test for finish at both ends
        compScor = dom.isComp(piec, self.currPiec)
        # print(compScor)

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

        if (isTwo and isFour) or (isEig and isOne):
            bothSide = True
        else:
            bothSide = False

        # Final count for points

        if isCarr:
            if bothSide:
                nPtsAdd = 4
                self.msgr.prnt("\n----- CRUZADO!! 4 pts! -----")
            else:
                nPtsAdd = 2
                self.msgr.prnt("\n----- CARROÇA!! 2 pts! -----")
        else:
            if bothSide:
                nPtsAdd = 3
                self.msgr.prnt("\n----- LAILOT!!  3 pts! -----")
            else:
                nPtsAdd = 1
                self.msgr.prnt("\n-----     OK!  1 pt. -----")

        self.nPtsAdd = nPtsAdd

    def showHist(self):
        """Show history of the played pieces."""
        dom = domino()

        # Show history
        self.msgr.prnt({'eng': "\n-> This is the played history:",
                        'por': "\n-> Este é o histórico de jogadas:"})
        indPl = self.starts
        # print(indPl)
        for ind in self.piecHist:
            # print(ind)
            strPrnt = "Pl." + str(indPl) + ": "
            # print("strPrnt = '"+strPrnt+"'")

            if ind is None:
                if self.msgr.lang == 'eng':
                    strPrnt += "Passed."
                elif self.msgr.lang == 'por':
                    strPrnt += "Passei."
                else:
                    strPrnt += "None"
            else:
                strPrnt += str(dom.getPiecPair(ind)) + " (" + str(ind) + ")"
            #
            self.msgr.prnt(strPrnt)
            indPl = (indPl + 1) % 4
        #

    def showStat(self):
        """Show current state of the table."""
        dom = domino()
        cp = self.currPiec
        if cp is not None:
            self.msgr.prnt({'eng': "\n-> This is the current piece " +
                                   "(state) in the table:",
                            'por': "\n-> Esta é a peça atual (estado) " +
                                   "do jogo:"})
            self.msgr.prnt(str(cp) + " (" + str(dom.getPiecPair(cp)) + ")")

    def showHand(self):
        """Show the player's hands."""
        dom = domino()
        self.msgr.prnt({'eng': "\nThese are the players' hands:",
                        'por': "\nAqui estão as mãos dos jogadores:"})
        for pl in range(4):
            p = self.players[pl]
            self.msgr.prnt({'eng': "  Player #" + str(pl) + ":",
                            'por': "  Jogador #" + str(pl) + ":"})
            handStr = '    '
            for ind in range(len(p.hand)):
                handStr += str(dom.getPiecPair(p.hand[ind]))+', '
            self.msgr.prnt(handStr)

    def showHandNumb(self):
        """Show the number of pieces on each player's hands."""
        self.msgr.prnt({'eng': "\n-> Number of pieces in players' hands:",
                        'por': "\n-> Número de peças nas mãos dos jogadores:"})
        for pl in range(4):
            p = self.players[pl]
            self.msgr.prnt({'eng': " Pl. " + str(pl) + ": " +
                                   str(len(p.hand)) + " pieces.",
                            'por': " Jog. " + str(pl) + ": " +
                                   str(len(p.hand)) + " peças."})

    def showHasNot(self):
        """Show what each player has declared not to have."""
        # language-specific texts:
        if self.msgr.lang == 'eng':
            hasNot_txt = 'has declared not having'
            pl_txt = 'Pl'
            titl_txt = "\n-> Player's declarations:\n"
        elif self.msgr.lang == 'por':
            hasNot_txt = 'declarou não ter'
            pl_txt = 'Jog'
            titl_txt = "\n-> Declarações dos jogadores:\n"

        # this is the body of the message
        msg = ''
        for i in range(4):
            thisPlyrStr = ' {}. {} {}: '.format(pl_txt, i, hasNot_txt)
            # check which pieces this player has not.
            lacks = False  # In principle, he/she has everything
            for j in range(7):
                if self.hasNot[i, j]:
                    lacks = True
                    thisPlyrStr += '{}, '.format(j)
            # only print something if this player lacks something
            if lacks:
                # this [:-2] gets rid of the trailing ", "
                msg += thisPlyrStr[:-2] + ';\n'

        # only print if someone has declared something
        if len(msg) > 0:
            # this [:-1] gets rid of the extra '\n' in the end
            self.msgr.prnt(titl_txt + msg[:-1])

    def showTabl(self):
        """Show the table: history, status and hand numbers."""
        self.msgr.prnt('-' * 80)
        self.showHist()
        self.showStat()
        self.showHasNot()
        self.showHandNumb()

    def showAll(self):
        """Show everything: history, status and the players' hands."""
        self.msgr.prnt('-' * 80)
        self.showHist()
        self.showStat()
        self.showHand()


class match:
    """Class match plays a simple match."""

    @staticmethod
    def play(compSttg, starts=-1, msgr=None):
        """Play a match."""
        msgr.prnt('-' * 80)
        msgr.prnt({'eng': "\nNew match!",
                   'por': "\nNova partida!"})
        # create a new table
        tab = table(starts=starts, compSttg=compSttg, msgr=msgr)

        # First piece!
        if starts == -1:
            tab.play(isFirst=True)
        else:
            tab.play()
        # DEBUG:
        # tab.showAll()

        win = None
        while win is None:
            win = tab.play()
            # DEBUG:
            # tab.showAll()
        msgr.prnt('-' * 80)

        msgr.prnt({'eng': "\n\n\nGAME FINISHED!",
                   'por': "\n\n\nJOGO CONCLUÍDO!"})
        if win % 2 == 0:
            msgr.prnt({'eng': "\n    EVEN team won this match!" +
                              "\n\nCONGRATULATIONS!!",
                       'por': "\n    Time PAR ganhou esta partida!" +
                              "\n\nPARABÉNS!!"})
        else:
            msgr.prnt({'eng': "\n    ODD team won this match!" +
                              "\n\nSorry, you lost!",
                       'por': "\n    Time ÍMPAR ganhou esta partida!" +
                              "\n\nSinto muito, você perdeu!"})
        return win, tab.nPtsAdd, tab.starts


class champ:
    """Class champ plays a championship."""

    def __init__(self, compSttg=None, msgr=None):
        msgr.prnt('-' * 80 + '\n' + '-' * 80)
        msgr.prnt({'eng': "\nNew championship!\n",
                   'por': "\nNovo campeonato!\n"})
        msgr.prnt('-' * 80 + '\n' + '-' * 80)

        msg = {'eng': "\nThere will be four players:\n" +
                      " - 0 (You), \n - 1 (Computer opponent),\n" +
                      " - 2 (Computer ally),\n - 3 (Computer opponent).",
               'por': "\nSão quatro os jogadores:\n" +
                      " - 0 (Você), \n - 1 (Computador oponente),\n" +
                      " - 2 (Computer aliado),\n - 3 (Computador oponente)."}
        msgr.prnt(msg)

        if compSttg is None:
            compSttg = ['rand', 'rand', 'rand']

        msgr.prnt({'eng': "\n Strategy for the computers:",
                   'por': "\n Estratégia para os computadores:"})
        msgr.prnt(compSttg)

        msgr.prnt({'eng': "\nPress any key to continue...",
                   'por': "\nPressione qualquer tecla para continuar..."})
        input("  >> ")

        EvnPts = 0
        OddPts = 0
        starts = -1
        while EvnPts < 6 and OddPts < 6:
            win, ptsAdd, started = match.play(starts=starts, compSttg=compSttg,
                                              msgr=msgr)

            if win % 2 == 0:
                EvnPts += ptsAdd
            else:
                OddPts += ptsAdd

            starts = (started + 1) % 4
            msgr.prnt({'eng': "\nEven team: " + str(EvnPts),
                       'por': "\nTime par: " + str(EvnPts)})

            msgr.prnt({'eng': "\nOdd team: " + str(OddPts),
                       'por': "\nTime ímpar: " + str(OddPts)})

            msgr.prnt({'eng': "\nPress any key to continue...",
                       'por': "\nPressione qualquer tecla para continuar..."})
            input("  >> ")
        #

        msgr.prnt('\n\n\n' + '*' * 80)
        if EvnPts >= 6:
            msgr.prnt({'eng': "\n YOU HAVE WON THIS GAME!\n" +
                              "YOU ARE TOTALLY EXCELLENT!!\n",
                       'por': "\n VOCÊ GANHOU ESSE JOGO!\n" +
                              "VOCÊ É TOTALMENTE EXCELENTE!!\n"})
        else:
            msgr.prnt({'eng': "\nSorry, it seems you lost this game...\n" +
                              "Good luck on the next one!\n",
                       'por': "\nDesculpe, mas parece que você perdeu" +
                              " esse jogo...\nBoa sorte no próximo!\n"})
