#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:34:56 2018

@author: levi
"""
import random


class msgr:
    """The messenger, which prints the messages."""

    def __init__(self, InptLang='eng'):
        if not(InptLang == 'eng' or InptLang == 'por'):
            print("Unknown language.")
            raise Exception
        else:
            self.lang = InptLang

    def prnt(self, textDict):
        """Print a given text."""
        if isinstance(textDict, dict):
            print(textDict.get(self.lang, 'eng'))
        else:
            print(textDict)


class domino:
    """Class domino holds the basics for the game in general.

    There are methods for the getting piece pair from integer number and vice
    versa, compatibility test, etc.
    """

    def isComp(self, handP, tablP):
        """Find out if piece is compatible with the table's current state.

        handP: the piece in the player's hand (represented by its integer
               (0 to 27) number; whose compatibility is being tested
        tablP: the piece representing the state of the table (also represen-
               ted by its integer (0 to 27).

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
        # these are the piece pairs (e.g. [6,6] instead of 27)
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

    @staticmethod
    def getPiecPair(piecNum):
        """Get piece pair.

        Gets the pair of numbers that represent the piece (e.g., [0,0], [2,3],
        [4,4], [5,6]]), given its piece number (e.g., 0, 14, 22, 26).
        """
        pair = [0, 0]
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
            pair = [6, 6]

        return pair

    @staticmethod
    def getPiecNum(piecPair):
        """Get piece number.

        Gets the piece number (e.g., 0, 14, 22, 26) given the pair of
        numbers that represent the piece (e.g., [0,0], [2,3], [4,4], [5,6]).
        """
        piecPair.sort()
        num = 0

        for ind in range(6):
            if piecPair[0] > ind:
                num += 6-ind
        num += piecPair[1]

        return num

    @staticmethod
    def pcsWith(num):
        """Get all possible pieces with a given number.

        For example:
            - pieces #0 through #6 are the ones that have a 0 in it.
            - pieces #6, #12, #17, #21, #24, #26 and #27 are the ones that
              have a 6 in it.

        returns: a list of the 7 pieces that have the given number 'num'.
        """
        ret = [0]*7

        for i in range(7):
            ret[i] = domino.getPiecNum([num, i])

        return ret


class player:
    """Represents the player."""

    def __init__(self, plNumb, isAuto, hand, sttg='rand'):
        self.plNumb = plNumb
        self.isAuto = isAuto
        self.sttg = sttg
        self.hand = hand

    def promUser(self, currPiec, psbl, msgr=None):
        """Prompt user for input, showing his/her possibilities.

        Returns the index for the possibilites list psbl.
        """
        dom = domino()
        if currPiec is not None:
            currPiecPair = dom.getPiecPair(currPiec)
        else:
            currPiecPair = [0, 0]

        keepAsk = True
        while keepAsk:
            msgr.prnt({'eng': "\nThis is your hand:",
                       'por': "\nEsta é a sua mão:"})
            hand = self.hand
            handStr = ''
            for ind in range(len(hand)):
                handStr += str(dom.getPiecPair(hand[ind]))
                handStr += ', '
            msgr.prnt(handStr)

            if len(psbl) == 0:
                dic = {'eng': "\nI'm sorry, there is nothing you can play " +
                              "now.\nPress any key to continue...",
                       'por': "\nDesculpe, não há o que jogar agora." +
                              "\nPressione qualquer tecla para continuar..."}

                msgr.prnt(dic)
                input("  >> ")
                keepAsk = False
                choice = None
            else:
                if len(psbl) == 1:
                    msgr.prnt({'eng': "\nThere is only one possibility:",
                               'por': "\nSó há uma possibilidade:"})
                else:
                    msgr.prnt({'eng': "\nChoose the piece to be played:",
                               'por': "\nEscolha a peça a ser jogada:"})

                for ind in range(len(psbl)):
                    piec, posi, ornt = psbl[ind]
                    strPrnt = ' - ' + str(ind) + ' : '
                    strPrnt += str(dom.getPiecPair(piec))
                    if currPiec is not None:

                        str1, str2, str3 = '', '', ''
                        if msgr.lang == 'eng':
                            str1 = '(' + str(piec) + ') at the '
                            str2 = 'left position (by the '
                            str3 = 'right position (by the '
                        elif msgr.lang == 'por':
                            str1 = '(' + str(piec) + ') ao lado '
                            str2 = 'esquerdo (junto ao '
                            str3 = 'direito (junto ao '

                        if posi == 0:
                            str3 = ''
                        else:
                            str2 = ''

                        strPrnt += str1 + str2 + str3

                        strPrnt += str(currPiecPair[posi])
                        strPrnt += ')'

                    msgr.prnt(strPrnt)
                #

                if len(psbl) == 1:
                    msgr.prnt({'eng': "Press any key to play it.",
                               'por': "Pressione qualquer tecla para "
                                      "jogá-la."})
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
                        msgr.prnt({'eng': "\nError while parsing input." +
                                          "\nPlease try again.",
                                   'por': "\nErro ao interpretar entrada." +
                                          "\nPor favor, tente novamente."})
            #
        #
        return choice

    def getPsbl(self, currPiec):
        """Get the possibilities for playing.

        Returns a list of possibilities.
        Each possibility is a triple containing:
           1. ind: the index (integer, 0 to 6) of the piece in the player's
                   hand;
           2. posi: 0 or 1, correponding to the side of the table
                    (0 is for the lesser side, 1 for the greater one);
           3. ornt: True or False, corresponding to the piece's orientation
                    (True is for setting the piece on its lesser side,
                     revealing the greater one; False for the opposite).
        """
        dom = domino()
        psbl = []
        if currPiec is None:
            # If there is no current piece, than all pieces are allowed.
            # Orientation and position do not apply.
            for ind in self.hand:
                psbl.append([ind, 0, True])
        else:
            for ind in self.hand:
                # all the possibilities for this particular piece are encoded
                # in psblIndx
                psblIndx = dom.isComp(ind, currPiec)
                piecPair = dom.getPiecPair(ind)
                if psblIndx > 0:
                    if psblIndx % 2 == 1:
                        psbl.append([ind, 0, True])
                        psblIndx -= 1
                    if psblIndx % 4 == 2:
                        psbl.append([ind, 1, True])
                        psblIndx -= 2
                    if psblIndx % 8 == 4:
                        if piecPair[0] != piecPair[1]:
                            psbl.append([ind, 0, False])
                        psblIndx -= 4
                    if psblIndx > 0:
                        if piecPair[0] != piecPair[1]:
                            psbl.append([ind, 1, False])
                    #
                #
            #
        #
        return psbl

    def play(self, currPiec, piecHist, strtWith=None, msgr=None):
        """Play a piece.

        This method chooses the piece to be played (if such piece exists),
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

        posi, ornt = None, None

        # strtWith is only used when starting a match with the [6,6], [5,5],
        # etc. No choice in this case.
        if strtWith is None:
            psbl = self.getPsbl(currPiec)

            if self.isAuto:
                if len(psbl) > 0:
                    # HERE IS WHERE THE PLAYER MAKES THE CHOICE
                    if self.sttg == 'rand':
                        # Random stategy: play anything
                        playPiec, posi, ornt = random.choice(psbl)
                        # print("Playing randomly here!")
                    if self.sttg == 'basic':
                        # Basic stategy: play the highest possible piece
                        playPiec, posi, ornt = psbl[-1]
                        # print("Playing basic here!")
                        # print("Not implemented yet!")

            else:
                # MANUAL MODE
                choice = self.promUser(currPiec, psbl, msgr=msgr)
                if choice is None:
                    return None, None, None
                else:
                    playPiec, posi, ornt = psbl[choice]
        #

        if playPiec is not None:
            str1, str2, str3 = '', '', ''
            if msgr.lang == 'eng':
                str1 = "\nPlayer #" + str(self.plNumb) + \
                       ": I've played piece " + \
                       str(dom.getPiecPair(playPiec)) + " (" + \
                       str(playPiec) + ") at the "
                str2 = "left side!"
                str3 = "right side!"
            elif msgr.lang == 'por':
                str1 = "\nJogador #" + str(self.plNumb) + \
                       ": Joguei a pedra " + \
                       str(dom.getPiecPair(playPiec)) + " (" + \
                       str(playPiec) + ") no lado "
                str2 = "esquerdo!"
                str3 = "direito!"
            #

            if posi == 0:
                str3 = ''
            else:
                str2 = ''

            msgr.prnt(str1+str2+str3)

            self.hand.remove(playPiec)
        else:
            pair = dom.getPiecPair(currPiec)

            msgr.prnt({'eng': "Player #" + str(self.plNumb) +
                              ": Passed!\n" +
                              "> Has no " + str(pair[0]) + " or " +
                              str(pair[1]) + ".",
                       'por': "Jogador #" + str(self.plNumb) + ": Passou!\n" +
                              "> Não tem " + str(pair[0]) + " nem " +
                              str(pair[1]) + "."})

        return playPiec, posi, ornt
