#implement a chess game in python.
import sys
import pygame
import random
import time
from pygame.locals import *
import copy
from multiprocessing import Pool


SCREENSIZE=(600,600)
FONT="Times New Roman"
BACKGRUNDCOLOR=(0,0,0)
FIELDCOLORS=((125,125,125),(66,66,66))


class Player:
    def __init__(self,Player):
        self.Moves=0
        self.Playernr=Player #1 is white, two is black
        self.AlivePieces=['']*16
        for i in range(16):
            self.AlivePieces[i]=[i,1,0] #list to hold which pieces are still alive. Third argument is moves. If second argument is two, piece is transformed to queen
        if self.Playernr==2:
            self.Pieceplacement=['']*16
            for i in range(6,8,1):
                for j in range(8):
                    self.Pieceplacement[j+(i-6)*8]=[j,i]

        else:
            self.Pieceplacement=['']*16
            for i in range(2):
                for j in range(8):
                    self.Pieceplacement[j+i*8]=[j,i]
            self.Pieceplacement=self.Pieceplacement[8:]+self.Pieceplacement[:8]

def CheckIfChess(Player,Opponent,FieldPair=0): #Checks if the Player is chess. If Fieldpair is provided, it will return the result for these shifted
    #Check if any moves Opponent can make will be able to kill the king
    PieceNum_Player = []
    OldPlacement_Player = []
    PieceNum_Opponent = []
    OldPlacement_Opponent = []
    OldAlive_Opponent =[]

    if not FieldPair==0:
        if len(FieldPair)==2:
            PieceNum_Player.append(Player.Pieceplacement.index(FieldPair[0]))
            OldPlacement_Player.append(copy.copy(Player.Pieceplacement[PieceNum_Player[0]]))
            Player.Pieceplacement[copy.copy(PieceNum_Player[0])]=FieldPair[1]
        elif len(FieldPair)==4:
            PieceNum_Player.append(Player.Pieceplacement.index(FieldPair[0]))
            PieceNum_Player.append(Player.Pieceplacement.index(FieldPair[2]))
            OldPlacement_Player.append(copy.copy(Player.Pieceplacement[PieceNum_Player[0]]))
            OldPlacement_Player.append(copy.copy(Player.Pieceplacement[PieceNum_Player[1]]))
            Player.Pieceplacement[PieceNum_Player[0]]=FieldPair[1]
            Player.Pieceplacement[PieceNum_Player[0]]=FieldPair[3]

        if FieldPair[1] in Opponent.Pieceplacement:

            Piece=Opponent.Pieceplacement.index(FieldPair[1])
            PieceNum_Opponent.append(Piece)
            OldPlacement_Opponent.append(copy.copy(Opponent.Pieceplacement[Piece]))
            OldAlive_Opponent.append(Opponent.AlivePieces[Piece][1])
            Opponent.Pieceplacement[Piece]=[-1,-1]
            Opponent.AlivePieces[Piece][1]=0
    KingAlive=1
    if FieldPair==0:
        for i in range(16):
            if Player.Pieceplacement[12] in FindPossibleMoves(Opponent.Pieceplacement[i],Opponent,Player,0):
                KingAlive=0
    else:
        for i in range(16):
            if Player.Pieceplacement[12] in FindPossibleMoves(Opponent.Pieceplacement[i],Opponent,Player,0):
                KingAlive=0

        for i in range(len(PieceNum_Player)):
            Player.Pieceplacement[PieceNum_Player[i]] = OldPlacement_Player[i]
        for i in range(len(PieceNum_Opponent)):
            Opponent.Pieceplacement[PieceNum_Opponent[i]] = OldPlacement_Opponent[i]
            Opponent.AlivePieces[PieceNum_Opponent[i]][1] = OldAlive_Opponent[i]
    return not KingAlive

def CheckIfChessMate(Player,Opponent): #Check if Player is Chessmate. Return 1 if chessmate, 2 if stalemate. else return 0
    #Check if player can move any piece
    canmove=0
    for i in Player.Pieceplacement:
        if len(FindPossibleMoves(i,Player,Opponent))>0:
            canmove=1
    if canmove:
        return 0 #it is possible to make a move, thus the player is not checkmate
    else:
        #Check if we are stalemate
        if CheckIfChess(Player,Opponent)==1:
            #Checkmate
            return 1
        else:
            return 2


def FindPossibleMoves(Field,thePlayer,theOpponent,checkchess=1, Piece = -1): #Contains most of gamelogic and rules. Most bugs will probably be here.
    Piece=thePlayer.Pieceplacement.index(Field)
    if thePlayer.AlivePieces[Piece][1]==0:
        return []
    #print Piece
    Moves=[]
    if Piece<8: #This is a pessant
        if thePlayer.AlivePieces[Piece][2]==0: #First move for this piece
            if thePlayer.Playernr==2: #White
                if not [Field[0],Field[1]-1] in theOpponent.Pieceplacement+thePlayer.Pieceplacement:
                    Moves.append([Field[0],Field[1]-1])
                    if not [Field[0],Field[1]-2] in theOpponent.Pieceplacement+thePlayer.Pieceplacement:
                        Moves.append([Field[0],Field[1]-2])
                if [Field[0]+1,Field[1]-1] in theOpponent.Pieceplacement:
                    Moves.append([Field[0]+1,Field[1]-1])
                if [Field[0]-1,Field[1]-1] in theOpponent.Pieceplacement:
                    Moves.append([Field[0]-1,Field[1]-1])
            else:
                if not [Field[0],Field[1]+1] in theOpponent.Pieceplacement+thePlayer.Pieceplacement:
                    Moves.append([Field[0],Field[1]+1])
                    if not [Field[0],Field[1]+2] in theOpponent.Pieceplacement+thePlayer.Pieceplacement:
                        Moves.append([Field[0],Field[1]+2])
                if [Field[0]+1,Field[1]+1] in theOpponent.Pieceplacement:
                    Moves.append([Field[0]+1,Field[1]+1])
                if [Field[0]-1,Field[1]+1] in theOpponent.Pieceplacement:
                    Moves.append([Field[0]-1,Field[1]+1])
        else:
            if thePlayer.AlivePieces[Piece][1]==2: #check if transformed to queen
                #Queenmoves
                #Combine Runner and Tower
                for i in zip(list(range(Field[0]+1,8)),list(range(Field[1]+1,8))):
                    i=[i[0],i[1]]
                    if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                        Moves.append(i)
                    else:
                        if i in theOpponent.Pieceplacement:
                            Moves.append(i)
                            break
                        else:
                            break
                for i in zip(list(range(Field[0]-1,-1,-1)),list(range(Field[1]+1,8))):
                    i=[i[0],i[1]]
                    if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                        Moves.append(i)
                    else:
                        if i in theOpponent.Pieceplacement:
                            Moves.append(i)
                            break
                        else:
                            break
                for i in zip(list(range(Field[0]+1,8)),list(range(Field[1]-1,-1,-1))):
                    i=[i[0],i[1]]
                    if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                        Moves.append(i)
                    else:
                        if i in theOpponent.Pieceplacement:
                            Moves.append(i)
                            break
                        else:
                            break
                for i in zip(list(range(Field[0]-1,-1,-1)),list(range(Field[1]-1,-1,-1))):
                    i=[i[0],i[1]]
                    if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                        Moves.append(i)
                    else:
                        if i in theOpponent.Pieceplacement:
                            Moves.append(i)
                            break
                        else:
                            break
                #Check horisontal
                i=0
                while (Field[0]+i<=6):
                    i+=1
                    if not ([Field[0]+i,Field[1]] in thePlayer.Pieceplacement or [Field[0]+i,Field[1]] in theOpponent.Pieceplacement):
                        Moves.append([Field[0]+i,Field[1]])
                    else:
                        if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
                            Moves.append([Field[0]+i,Field[1]])
                            break
                        else:
                            break

                i=0
                while (Field[0]+i>=1):
                    i-=1
                    if not ([Field[0]+i,Field[1]] in thePlayer.Pieceplacement or [Field[0]+i,Field[1]] in theOpponent.Pieceplacement):
                        Moves.append([Field[0]+i,Field[1]])
                    else:
                        if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
                            Moves.append([Field[0]+i,Field[1]])
                            break
                        else:
                            break
                #Check Vertical
                i=0
                while (Field[1]+i<=6):
                    i+=1
                    if not ([Field[0],Field[1]+i] in thePlayer.Pieceplacement or [Field[0],Field[1]+i] in theOpponent.Pieceplacement):
                        Moves.append([Field[0],Field[1]+i])
                    else:
                        if [Field[0],Field[1]+i] in theOpponent.Pieceplacement:
                            Moves.append([Field[0],Field[1]+i])
                            break
                        else:
                            break

                i=0
                while (Field[1]+i>=1):
                    i-=1
                    if not ([Field[0],Field[1]+i] in thePlayer.Pieceplacement or [Field[0],Field[1]+i] in theOpponent.Pieceplacement):
                        Moves.append([Field[0],Field[1]+i])
                    else:
                        if [Field[0],Field[1]+i] in theOpponent.Pieceplacement:
                            Moves.append([Field[0],Field[1]+i])
                            break
                        else:
                            break



            if thePlayer.Playernr==2: #White
                #Check if anything in front of piece
                if not ([Field[0],Field[1]-1] in thePlayer.Pieceplacement  or [Field[0],Field[1]-1] in theOpponent.Pieceplacement):
                    Moves.append([Field[0],Field[1]-1])
                if [Field[0]-1,Field[1]-1] in theOpponent.Pieceplacement and  not Field[0]-1 <0:
                    Moves.append([Field[0]-1,Field[1]-1])
                if [Field[0]+1,Field[1]-1] in theOpponent.Pieceplacement and  not Field[0]+1 >7:
                    Moves.append([Field[0]+1,Field[1]-1])
            else: #Black
                if not ([Field[0],Field[1]+1] in thePlayer.Pieceplacement  or [Field[0],Field[1]+1] in theOpponent.Pieceplacement):
                    Moves.append([Field[0],Field[1]+1])
                if [Field[0]-1,Field[1]+1] in theOpponent.Pieceplacement and  not Field[0]-1 <0:
                    Moves.append([Field[0]-1,Field[1]+1])
                if [Field[0]+1,Field[1]+1] in theOpponent.Pieceplacement and  not Field[0]+1 >7:
                    Moves.append([Field[0]+1,Field[1]+1])
    elif Piece==15 or Piece==8: #Tower
        #Check horisontal
        i=0
        while (Field[0]+i<=6):
            i+=1
            if not ([Field[0]+i,Field[1]] in thePlayer.Pieceplacement or [Field[0]+i,Field[1]] in theOpponent.Pieceplacement):
                Moves.append([Field[0]+i,Field[1]])
            else:
                if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
                    Moves.append([Field[0]+i,Field[1]])
                    break
                else:
                    break

        i=0
        while (Field[0]+i>=1):
            i-=1
            if not ([Field[0]+i,Field[1]] in thePlayer.Pieceplacement or [Field[0]+i,Field[1]] in theOpponent.Pieceplacement):
                Moves.append([Field[0]+i,Field[1]])
            else:
                if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
                    Moves.append([Field[0]+i,Field[1]])
                    break
                else:
                    break
        #Check Vertical
        i=0
        while (Field[1]+i<=6):
            i+=1
            if not ([Field[0],Field[1]+i] in thePlayer.Pieceplacement or [Field[0],Field[1]+i] in theOpponent.Pieceplacement):
                Moves.append([Field[0],Field[1]+i])
            else:
                if [Field[0],Field[1]+i] in theOpponent.Pieceplacement:
                    Moves.append([Field[0],Field[1]+i])
                    break
                else:
                    break

        i=0
        while (Field[1]+i>=1):
            i-=1
            if not ([Field[0],Field[1]+i] in thePlayer.Pieceplacement or [Field[0],Field[1]+i] in theOpponent.Pieceplacement):
                Moves.append([Field[0],Field[1]+i])
            else:
                if [Field[0],Field[1]+i] in theOpponent.Pieceplacement:
                    Moves.append([Field[0],Field[1]+i])
                    break
                else:
                    break


    elif Piece==9 or Piece==14: #Horse
        for i in range(-2,3):
            if i==0:
                continue
            for j in range(-2,3):
                if j==0:
                    continue
                if abs(i)==abs(j):
                    continue
                if not (Field[0]+i<0 or Field[0]+i>7 or Field[1]+j<0 or Field[1]+j>7 or [Field[0]+i,Field[1]+j] in thePlayer.Pieceplacement) :
                    Moves.append([Field[0]+i,Field[1]+j])

    elif Piece==10 or Piece==13: #Runner
        for i in zip(list(range(Field[0]+1,8)),list(range(Field[1]+1,8))):
            i=[i[0],i[1]]
            if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                Moves.append(i)
            else:
                if i in theOpponent.Pieceplacement:
                    Moves.append(i)
                    break
                else:
                    break
        for i in zip(list(range(Field[0]-1,-1,-1)),list(range(Field[1]+1,8))):
            i=[i[0],i[1]]
            if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                Moves.append(i)
            else:
                if i in theOpponent.Pieceplacement:
                    Moves.append(i)
                    break
                else:
                    break
        for i in zip(list(range(Field[0]+1,8)),list(range(Field[1]-1,-1,-1))):
            i=[i[0],i[1]]
            if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                Moves.append(i)
            else:
                if i in theOpponent.Pieceplacement:
                    Moves.append(i)
                    break
                else:
                    break
        for i in zip(list(range(Field[0]-1,-1,-1)),list(range(Field[1]-1,-1,-1))):
            i=[i[0],i[1]]
            if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                Moves.append(i)
            else:
                if i in theOpponent.Pieceplacement:
                    Moves.append(i)
                    break
                else:
                    break

    elif Piece==11: #Queen
        #Combine Runner and Tower
        for i in zip(list(range(Field[0]+1,8)),list(range(Field[1]+1,8))):
            i=[i[0],i[1]]
            if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                Moves.append(i)
            else:
                if i in theOpponent.Pieceplacement:
                    Moves.append(i)
                    break
                else:
                    break
        for i in zip(list(range(Field[0]-1,-1,-1)),list(range(Field[1]+1,8))):
            i=[i[0],i[1]]
            if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                Moves.append(i)
            else:
                if i in theOpponent.Pieceplacement:
                    Moves.append(i)
                    break
                else:
                    break
        for i in zip(list(range(Field[0]+1,8)),list(range(Field[1]-1,-1,-1))):
            i=[i[0],i[1]]
            if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                Moves.append(i)
            else:
                if i in theOpponent.Pieceplacement:
                    Moves.append(i)
                    break
                else:
                    break
        for i in zip(list(range(Field[0]-1,-1,-1)),list(range(Field[1]-1,-1,-1))):
            i=[i[0],i[1]]
            if not (i in thePlayer.Pieceplacement or i in theOpponent.Pieceplacement):
                Moves.append(i)
            else:
                if i in theOpponent.Pieceplacement:
                    Moves.append(i)
                    break
                else:
                    break
        #Check horisontal
        i=0
        while (Field[0]+i<=6):
            i+=1
            if not ([Field[0]+i,Field[1]] in thePlayer.Pieceplacement or [Field[0]+i,Field[1]] in theOpponent.Pieceplacement):
                Moves.append([Field[0]+i,Field[1]])
            else:
                if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
                    Moves.append([Field[0]+i,Field[1]])
                    break
                else:
                    break

        i=0
        while (Field[0]+i>=1):
            i-=1
            if not ([Field[0]+i,Field[1]] in thePlayer.Pieceplacement or [Field[0]+i,Field[1]] in theOpponent.Pieceplacement):
                Moves.append([Field[0]+i,Field[1]])
            else:
                if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
                    Moves.append([Field[0]+i,Field[1]])
                    break
                else:
                    break
        #Check Vertical
        i=0
        while (Field[1]+i<=6):
            i+=1
            if not ([Field[0],Field[1]+i] in thePlayer.Pieceplacement or [Field[0],Field[1]+i] in theOpponent.Pieceplacement):
                Moves.append([Field[0],Field[1]+i])
            else:
                if [Field[0],Field[1]+i] in theOpponent.Pieceplacement:
                    Moves.append([Field[0],Field[1]+i])
                    break
                else:
                    break

        i=0
        while (Field[1]+i>=1):
            i-=1
            if not ([Field[0],Field[1]+i] in thePlayer.Pieceplacement or [Field[0],Field[1]+i] in theOpponent.Pieceplacement):
                Moves.append([Field[0],Field[1]+i])
            else:
                if [Field[0],Field[1]+i] in theOpponent.Pieceplacement:
                    Moves.append([Field[0],Field[1]+i])
                    break
                else:
                    break



    elif Piece==12: #King
        for i in range(-1,2):
            for j in range(-1,2):
                if i==0 and j==0:
                    continue
                else:
                    if not ([Field[0]+i,Field[1]+j] in thePlayer.Pieceplacement) and not (Field[0]+i>7 or Field[0]+i<0 or Field[1]+j>7 or Field[1]+j<0):
                        Moves.append([Field[0]+i,Field[1]+j])

        #Castling!!
        if checkchess:
            if thePlayer.AlivePieces[12][2]==0 and (thePlayer.AlivePieces[8][2]==0 or thePlayer.AlivePieces[8][2]==0) and not CheckIfChess(thePlayer,theOpponent):
                #Check if right Castling is possible
                if thePlayer.AlivePieces[15][2]==0: #Right Tower has not moved
                    if not ([thePlayer.Pieceplacement[12][0]+1,thePlayer.Pieceplacement[12][1]] in thePlayer.Pieceplacement+theOpponent.Pieceplacement or [thePlayer.Pieceplacement[12][0]+2,thePlayer.Pieceplacement[12][1]] in thePlayer.Pieceplacement+theOpponent.Pieceplacement): #Fields between king and tower is empty
                        if not (CheckIfChess(thePlayer,theOpponent) or CheckIfChess(thePlayer,theOpponent,[[thePlayer.Pieceplacement[12][0],thePlayer.Pieceplacement[12][1]],[thePlayer.Pieceplacement[12][0]+1,thePlayer.Pieceplacement[12][1]]]) or CheckIfChess(thePlayer,theOpponent,[[thePlayer.Pieceplacement[12][0],thePlayer.Pieceplacement[12][1]],[thePlayer.Pieceplacement[12][0]+2,thePlayer.Pieceplacement[12][1]]])): #the king does not pass through attacked fields
                            if not CheckIfChess(thePlayer,theOpponent,[[thePlayer.Pieceplacement[12][0],thePlayer.Pieceplacement[12][1]],[thePlayer.Pieceplacement[12][0]+2,thePlayer.Pieceplacement[12][1]],[thePlayer.Pieceplacement[15][0],thePlayer.Pieceplacement[15][1]],[thePlayer.Pieceplacement[15][0]-2,thePlayer.Pieceplacement[15][1]]]):
                                Moves.append([thePlayer.Pieceplacement[15][0],thePlayer.Pieceplacement[15][1]])
                #Check if left Castling is possible
                if thePlayer.AlivePieces[8][2]==0: #Right Tower has not moved
                    if not ([thePlayer.Pieceplacement[12][0]-1,thePlayer.Pieceplacement[12][1]] in thePlayer.Pieceplacement+theOpponent.Pieceplacement or [thePlayer.Pieceplacement[12][0]-2,thePlayer.Pieceplacement[12][1]] in thePlayer.Pieceplacement+theOpponent.Pieceplacement or [thePlayer.Pieceplacement[12][0]-3,thePlayer.Pieceplacement[12][1]] in thePlayer.Pieceplacement+theOpponent.Pieceplacement): #Fields between king and tower is empty
                        if not (CheckIfChess(thePlayer,theOpponent) or CheckIfChess(thePlayer,theOpponent,[[thePlayer.Pieceplacement[12][0],thePlayer.Pieceplacement[12][1]],[thePlayer.Pieceplacement[12][0]-1,thePlayer.Pieceplacement[12][1]]]) or CheckIfChess(thePlayer,theOpponent,[[thePlayer.Pieceplacement[12][0],thePlayer.Pieceplacement[12][1]],[thePlayer.Pieceplacement[12][0]-2,thePlayer.Pieceplacement[12][1]]])): #the king does not pass through attacked fields
                            if not CheckIfChess(thePlayer,theOpponent,[[thePlayer.Pieceplacement[12][0],thePlayer.Pieceplacement[12][1]],[thePlayer.Pieceplacement[12][0]-2,thePlayer.Pieceplacement[12][1]],[thePlayer.Pieceplacement[8][0],thePlayer.Pieceplacement[8][1]],[thePlayer.Pieceplacement[8][0]+3,thePlayer.Pieceplacement[8][1]]]):
                                Moves.append([thePlayer.Pieceplacement[8][0],thePlayer.Pieceplacement[8][1]])

            #Check if left castling is possible
    if checkchess:
        #print "CheckChess"
        Moves2=[]
        for i in Moves:
            if not CheckIfChess(thePlayer,theOpponent,(Field,i)):
                Moves2.append(i)
        #print Moves
        #print Moves2
        return Moves2
    return Moves

def doubledPawns(Player):
  Doubled = 0
  for i in range(8):
    isDoubled = 0
    if Player.AlivePieces[i][1] == 0:
      continue
    for j in range(i + 1, 8):
      if(Player.AlivePieces[j][1]):
        if Player.Pieceplacement[j][0] == Player.Pieceplacement[i][0]:
          isDoubled = 1
          break
    if(isDoubled):
      Doubled += 1
  return Doubled

def blockedPawns(Players, SelectedPlayer):
  Blocked = 0
  for i in range(8):
    isBlocked = 0
    if Players[0].AlivePieces[i][1] == 0:
      continue

    for j in range(16):
      if(Players[0].AlivePieces[j][1] and j != i):
        if SelectedPlayer == 1: #White
          if(Players[0].Pieceplacement[i][0] == Players[0].Pieceplacement[j][0] and Players[0].Pieceplacement[i][1] == Players[0].Pieceplacement[j][1] + 1):
            isBlocked = 1
            break
        else: #Black
          if(Players[0].Pieceplacement[i][0] == Players[0].Pieceplacement[j][0] and Players[0].Pieceplacement[i][1] == Players[0].Pieceplacement[j][1] - 1):
            isBlocked = 1
            break
      if(Players[1].AlivePieces[j][1]):
        if SelectedPlayer == 1: #White
          if(Players[0].Pieceplacement[i][0] == Players[1].Pieceplacement[j][0] and Players[0].Pieceplacement[i][1] == Players[1].Pieceplacement[j][1] + 1):
            isBlocked = 1
            break
        else: #Black
          if(Players[0].Pieceplacement[i][0] == Players[1].Pieceplacement[j][0] and Players[0].Pieceplacement[i][1] == Players[1].Pieceplacement[j][1] - 1):
            isBlocked = 1
            break
    if(isBlocked):
      Blocked += 1
  return Blocked

def issolatedPawns(Player):
  issolated = 0
  for i in range(8):
    isIssolated = 1
    if Player.AlivePieces[i][1] == 0:
      continue
    for j in range(8):
      if(Player.AlivePieces[j][1] and i != j):
        if Player.Pieceplacement[i][0] == Player.Pieceplacement[j][0] + 1 or Player.Pieceplacement[i][0] == Player.Pieceplacement[j][0] - 1:
          isIssolated = 0
          break
    if( isIssolated):
      issolated += 1
  return issolated

def PawnScore(Players, SelectedPlayer):
  Score = issolatedPawns(Players[0])
  Score += blockedPawns(Players, SelectedPlayer)
  Score += doubledPawns(Players[0])
  return Score

def isAlive(AlivePieces, List):
  count = 0
  for i in List:
    if AlivePieces[i][1]:
      count += 1
  return count

def evaluate(Players, SelectedPlayer): #first player in list should be white, next should be black
  #Calculate score from alive pieces
  Score = 0
  for i in range(8):
    if Players[0].AlivePieces[i][1] == 1:
      Score += 100
    elif Players[0].AlivePieces[i][1] == 2:
      Score += 900
    if Players[1].AlivePieces[i][1] == 1:
      Score -= 100
    elif Players[1].AlivePieces[i][1] == 2:
      Score -= 100

  Score += 500 * isAlive(Players[0].AlivePieces, [8, 15])
  Score -= 500 * isAlive(Players[1].AlivePieces, [8, 15])

  Score += 300 * isAlive(Players[0].AlivePieces, [9, 10, 13, 14])
  Score -= 300 * isAlive(Players[1].AlivePieces, [9, 10, 13, 14])

  Score += 20000 * isAlive(Players[0].AlivePieces, [12])
  Score -= 20000 * isAlive(Players[1].AlivePieces, [12])

  Score += 900 * isAlive(Players[0].AlivePieces, [11])
  Score -= 900 * isAlive(Players[1].AlivePieces, [11])

  Score += 5 * PawnScore(Players, 1)
  Score -= 5 * PawnScore(Players[::-1], 2)

  for i in range(16):
    if(Players[0].AlivePieces[i][1]):
      Score += 1 * len(FindPossibleMoves(Players[0].Pieceplacement[i], Players[0], Players[1]))
    if(Players[1].AlivePieces[i][1]):
      Score -= 1 * len(FindPossibleMoves(Players[1].Pieceplacement[i], Players[1], Players[0]))
  if SelectedPlayer == 2:
    Score *= -1
  return Score

def GetBestMovePiece(List):
    Piece, Players, SelectedPlayer = List
    BestMove = []
    max = -999999
    if SelectedPlayer == 1: # White
        for Move in FindPossibleMoves(Players[0].Pieceplacement[Piece], Players[0], Players[1]):
            OldPlacement = [copy.deepcopy(Players[0].AlivePieces), copy.deepcopy(Players[0].Pieceplacement), copy.deepcopy(Players[1].AlivePieces), copy.deepcopy(Players[1].Pieceplacement)]
            MakeMove(Players, Move, Players[0].Pieceplacement[Piece])
            score = -NegaMax(Players, 2, 1)
            Players[0].AlivePieces    = OldPlacement[0]
            Players[0].Pieceplacement = OldPlacement[1]
            Players[1].AlivePieces    = OldPlacement[2]
            Players[1].Pieceplacement = OldPlacement[3]
            if score > max:
                max = score
                BestMove = Move
    else:
        for Move in FindPossibleMoves(Players[1].Pieceplacement[Piece], Players[1], Players[0]):
            OldPlacement = [copy.deepcopy(Players[0].AlivePieces), copy.deepcopy(Players[0].Pieceplacement), copy.deepcopy(Players[1].AlivePieces), copy.deepcopy(Players[1].Pieceplacement)]
            MakeMove(Players[::-1], Move, Players[1].Pieceplacement[Piece])
            score = -NegaMax(Players, 1, 1)
            Players[0].AlivePieces    = OldPlacement[0]
            Players[0].Pieceplacement = OldPlacement[1]
            Players[1].AlivePieces    = OldPlacement[2]
            Players[1].Pieceplacement = OldPlacement[3]
            if score > max:
                max = score
                BestMove = Move
    return [Piece, max, BestMove]

def GetBestMove(Players, SelectedPlayer):
    BestMove = []
    max = -999999
    pool = Pool(processes = 4)
    result = ""
    poollist = []
    for i in random.sample(range(16), 16):
        poollist.append([i, copy.deepcopy(Players), SelectedPlayer])
    result = pool.imap_unordered(GetBestMovePiece, poollist)
    while result._index < 16:
        print(result._index)
        time.sleep(0.1)
    for i in result:
        if(i[1] > max):
            max = i[1]
            BestMove = [i[0], i[2]]
    pool.close()
    return BestMove


def NegaMax(Players, SelectedPlayer, depth = 3):
    if(depth == 0):
        return evaluate(Players, SelectedPlayer)
    max = -999999
    if SelectedPlayer == 1: # White
        for i in range(16):
            for Move in FindPossibleMoves(Players[0].Pieceplacement[i], Players[0], Players[1]):
                OldPlacement = [copy.deepcopy(Players[0].AlivePieces), copy.deepcopy(Players[0].Pieceplacement), copy.deepcopy(Players[1].AlivePieces), copy.deepcopy(Players[1].Pieceplacement)]
                MakeMove(Players, Move, Players[0].Pieceplacement[i])
                score = - NegaMax(Players, 2, depth - 1)
                Players[0].AlivePieces    = OldPlacement[0]
                Players[0].Pieceplacement = OldPlacement[1]
                Players[1].AlivePieces    = OldPlacement[2]
                Players[1].Pieceplacement = OldPlacement[3]
                if score > max:
                    max = score
    else:
        for i in range(16):
            for Move in FindPossibleMoves(Players[1].Pieceplacement[i], Players[1], Players[0]):
                OldPlacement = [copy.deepcopy(Players[0].AlivePieces), copy.deepcopy(Players[0].Pieceplacement), copy.deepcopy(Players[1].AlivePieces), copy.deepcopy(Players[1].Pieceplacement)]
                MakeMove(Players[::-1], Move, Players[1].Pieceplacement[i])
                score = - NegaMax(Players, 1, depth - 1)
                Players[0].AlivePieces    = OldPlacement[0]
                Players[0].Pieceplacement = OldPlacement[1]
                Players[1].AlivePieces    = OldPlacement[2]
                Players[1].Pieceplacement = OldPlacement[3]
                if score > max:
                    max = score
    return max

def alphaBetaMax(Players, SelectedPlayer, alpha, beta, depth = 3):
    if depth == 0:
        return evaluate(Players, SelectedPlayer)
    if SelectedPlayer == 1: # White
        for i in range(16):
            for Move in FindPossibleMoves(Players[0].Pieceplacement[i], Players[0], Players[1]):
                OldPlacement = [copy.deepcopy(Players[0].AlivePieces), copy.deepcopy(Players[0].Pieceplacement), copy.deepcopy(Players[1].AlivePieces), copy.deepcopy(Players[1].Pieceplacement)]
                MakeMove(Players, Move, Players[0].Pieceplacement[i])
                score = alphaBetaMin(Players, 2, alpha, beta, depth - 1)
                Players[0].AlivePieces    = OldPlacement[0]
                Players[0].Pieceplacement = OldPlacement[1]
                Players[1].AlivePieces    = OldPlacement[2]
                Players[1].Pieceplacement = OldPlacement[3]
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
    else:
        for i in range(16):
            for Move in FindPossibleMoves(Players[1].Pieceplacement[i], Players[1], Players[0]):
                OldPlacement = [copy.deepcopy(Players[0].AlivePieces), copy.deepcopy(Players[0].Pieceplacement), copy.deepcopy(Players[1].AlivePieces), copy.deepcopy(Players[1].Pieceplacement)]
                MakeMove(Players[::-1], Move, Players[1].Pieceplacement[i])
                score = alphaBetaMin(Players, 1, alpha, beta, depth - 1)
                Players[0].AlivePieces    = OldPlacement[0]
                Players[0].Pieceplacement = OldPlacement[1]
                Players[1].AlivePieces    = OldPlacement[2]
                Players[1].Pieceplacement = OldPlacement[3]
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
    return alpha

def alphaBetaMin(Players, SelectedPlayer, alpha, beta, depth = 3):
    if depth == 0:
        return -evaluate(Players, SelectedPlayer)
    if SelectedPlayer == 1: # White
        for i in range(16):
            for Move in FindPossibleMoves(Players[0].Pieceplacement[i], Players[0], Players[1]):
                OldPlacement = [copy.deepcopy(Players[0].AlivePieces), copy.deepcopy(Players[0].Pieceplacement), copy.deepcopy(Players[1].AlivePieces), copy.deepcopy(Players[1].Pieceplacement)]
                MakeMove(Players, Move, Players[0].Pieceplacement[i])
                score = alphaBetaMax(Players, 2, alpha, beta, depth - 1)
                Players[0].AlivePieces    = OldPlacement[0]
                Players[0].Pieceplacement = OldPlacement[1]
                Players[1].AlivePieces    = OldPlacement[2]
                Players[1].Pieceplacement = OldPlacement[3]
                if score <= alpha:
                    return alpha
                if score < beta:
                    beta = score
    else:
        for i in range(16):
            for Move in FindPossibleMoves(Players[1].Pieceplacement[i], Players[1], Players[0]):
                OldPlacement = [copy.deepcopy(Players[0].AlivePieces), copy.deepcopy(Players[0].Pieceplacement), copy.deepcopy(Players[1].AlivePieces), copy.deepcopy(Players[1].Pieceplacement)]
                MakeMove(Players[::-1], Move, Players[1].Pieceplacement[i])
                score = alphaBetaMax(Players, 1, alpha, beta, depth - 1)
                Players[0].AlivePieces    = OldPlacement[0]
                Players[0].Pieceplacement = OldPlacement[1]
                Players[1].AlivePieces    = OldPlacement[2]
                Players[1].Pieceplacement = OldPlacement[3]
                if score <= alpha:
                    return alpha
                if score < beta:
                    beta = score
    return beta

def DrawPossibilities(Players,SelectedField,Possibilities):
    #print (Players,SelectedField,Possibilities)
    screen.fill(BACKGRUNDCOLOR)
    #Color all the fields.
    for i in range(8):
        if i%2==0:
            for j in range(8):
                if j%2==0:
                    pygame.draw.rect(screen,FIELDCOLORS[0],pygame.Rect((i*SCREENSIZE[0]/8,j*SCREENSIZE[1]/8),(SCREENSIZE[0],SCREENSIZE[1])))
                else:
                    pygame.draw.rect(screen,FIELDCOLORS[1],pygame.Rect((i*SCREENSIZE[0]/8,j*SCREENSIZE[1]/8),(SCREENSIZE[0],SCREENSIZE[1])))
        else:
            for j in range(8):
                if j%2==0:
                    pygame.draw.rect(screen,FIELDCOLORS[1],pygame.Rect((i*SCREENSIZE[0]/8,j*SCREENSIZE[1]/8),(SCREENSIZE[0],SCREENSIZE[1])))
                else:
                    pygame.draw.rect(screen,FIELDCOLORS[0],pygame.Rect((i*SCREENSIZE[0]/8,j*SCREENSIZE[1]/8),(SCREENSIZE[0],SCREENSIZE[1])))
    #Color Selected field blue
    pygame.draw.rect(screen,(0,0,125),pygame.Rect((SelectedField[0]*SCREENSIZE[0]/8,SelectedField[1]*SCREENSIZE[1]/8),(SCREENSIZE[0]/8,SCREENSIZE[1]/8)))
    if SelectedField in Players[0].Pieceplacement: #Selected piece os in Players[0]
        for Possibility in Possibilities:
            if Possibility in Players[1].Pieceplacement: #Draw red if we can kill another players piece
                pygame.draw.rect(screen,(125,0,0),pygame.Rect((Possibility[0]*SCREENSIZE[0]/8,Possibility[1]*SCREENSIZE[1]/8),(SCREENSIZE[0]/8,SCREENSIZE[1]/8)))
            else: #Else green
                pygame.draw.rect(screen,(0,125,0),pygame.Rect((Possibility[0]*SCREENSIZE[0]/8,Possibility[1]*SCREENSIZE[1]/8),(SCREENSIZE[0]/8,SCREENSIZE[1]/8)))
    else:
        for Possibility in Possibilities:
            if Possibility in Players[0].Pieceplacement: #Draw red if we can kill another players piece
                pygame.draw.rect(screen,(125,0,0),pygame.Rect((Possibility[0]*SCREENSIZE[0]/8,Possibility[1]*SCREENSIZE[1]/8),(SCREENSIZE[0]/8,SCREENSIZE[1]/8)))
            else: #Else green
                pygame.draw.rect(screen,(0,125,0),pygame.Rect((Possibility[0]*SCREENSIZE[0]/8,Possibility[1]*SCREENSIZE[1]/8),(SCREENSIZE[0]/8,SCREENSIZE[1]/8)))
    DrawPieces(Players)

def DrawBoard(Players): #Draw the chessboard
    screen.fill(BACKGRUNDCOLOR)
    #Color all the fields.
    for i in range(8):
        if i%2==0:
            for j in range(8):
                if j%2==0:
                    pygame.draw.rect(screen,FIELDCOLORS[0],pygame.Rect((i*SCREENSIZE[0]/8,j*SCREENSIZE[1]/8),(SCREENSIZE[0],SCREENSIZE[1])))
                else:
                    pygame.draw.rect(screen,FIELDCOLORS[1],pygame.Rect((i*SCREENSIZE[0]/8,j*SCREENSIZE[1]/8),(SCREENSIZE[0],SCREENSIZE[1])))
        else:
            for j in range(8):
                if j%2==0:
                    pygame.draw.rect(screen,FIELDCOLORS[1],pygame.Rect((i*SCREENSIZE[0]/8,j*SCREENSIZE[1]/8),(SCREENSIZE[0],SCREENSIZE[1])))
                else:
                    pygame.draw.rect(screen,FIELDCOLORS[0],pygame.Rect((i*SCREENSIZE[0]/8,j*SCREENSIZE[1]/8),(SCREENSIZE[0],SCREENSIZE[1])))
    DrawPieces(Players)
    pygame.display.flip()

def DrawPieces(Players):
    for player in Players:
        for i in range(16):
            if not player.Pieceplacement[i]==[-1,-1]: #Don't draw if piece is dead
                if i<8: #Pessant
                    if player.AlivePieces[i][1]==2: #Check if queen
                        Name="Q"
                    else:
                        Name="P"
                elif i==8 or i==15: #Tower
                    Name="T"
                elif i==9 or i ==14: #Horse
                    Name="H"
                elif i==10 or i==13: #Runner
                    Name="R"
                elif i==11: #Queen
                    Name="Q"
                elif i==12: #King
                    Name="K"
                if player.Playernr==1:
                    text=font.render(Name,True,(0,0,0)) #White
                else:
                    text=font.render(Name,True,(255,255,255))
                screen.blit(text,(int(float(SCREENSIZE[0])/8*((player.Pieceplacement[i][0])+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/8*((player.Pieceplacement[i][1])+0.5)-text.get_height() / 2)))
    pygame.display.flip()
def MakeMove(Players, ToField, FromField):
    if FromField in Players[0].Pieceplacement:
        Piece=Players[0].Pieceplacement.index(FromField)
        if Piece==12 and (ToField in Players[0].Pieceplacement): #Castling is chosen
            if Players[0].Pieceplacement.index(ToField)==8: #left castling
                Players[0].Pieceplacement[12]=[Players[0].Pieceplacement[12][0]-2,Players[0].Pieceplacement[12][1]]
                Players[0].Pieceplacement[8]=[Players[0].Pieceplacement[8][0]+3,Players[0].Pieceplacement[8][1]]
                Players[0].AlivePieces[12][2]+=1
                Players[0].AlivePieces[8][2]+=1
                return 1
            if Players[0].Pieceplacement.index(ToField)==15: #right castling
                Players[0].Pieceplacement[12]=[Players[0].Pieceplacement[12][0]+2,Players[0].Pieceplacement[12][1]]
                Players[0].Pieceplacement[15]=[Players[0].Pieceplacement[15][0]-2,Players[0].Pieceplacement[15][1]]
                Players[0].AlivePieces[12][2]+=1
                Players[0].AlivePieces[15][2]+=1
                return 1

        Players[0].Pieceplacement[Piece]=ToField
        Players[0].AlivePieces[Piece][2]+=1 #Add 1 to number of moves
        if Piece<8: #turn pessent into Queen if it reaces end
            if ToField[1]==7 or ToField[1]==0:
                if Players[0].AlivePieces[Piece][1]==1:
                    Players[0].AlivePieces[Piece][1]=2
        if ToField in Players[1].Pieceplacement: #Remove opponents player from alivelist and placement
            Piece=Players[1].Pieceplacement.index(ToField)
            Players[1].Pieceplacement[Piece]=[-1,-1]
            Players[1].AlivePieces[Piece][1]=0
        return 1
    else:
        Piece=Players[1].Pieceplacement.index(FromField)
        Players[1].Pieceplacement[Piece]=ToField
        Players[1].AlivePieces[Piece][2]+=1 #Add 1 to number of moves
        if Piece<8: #turn pessent into Queen if it reaces end
            if ToField[1]==7:
                if Players[1].AlivePieces[Piece][1]==1:
                    Players[1].AlivePieces[Piece][1]=2
        if ToField in Players[0].Pieceplacement: #Remove opponents player from alivelist and placement
            Piece=Players[0].Pieceplacement.index(ToField)
            Players[0].Pieceplacement[Piece]=[-1,-1]
            Players[0].AlivePieces[Piece][1]=0
        return 1
def EnterChossingLoop(Players,SelectedField,Possibilities):
    while 1: #Loop till player have choosen.
        for event in pygame.event.get(): #Event    quoue
            if event.type==QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    PressedField=[int(float(event.pos[0])/SCREENSIZE[0]*8),int(float(event.pos[1])/SCREENSIZE[1]*8)]
                    if PressedField==SelectedField:
                        return 0
                    if not PressedField in Possibilities:
                        continue
                    return MakeMove(Players, PressedField, SelectedField)


def fullauto(White, Black, clk):
    Turn=1
    while True:
        for event in pygame.event.get(): #Event    quoue
            if event.type==QUIT:
                sys.exit()
        if Turn == 1:
            Move = GetBestMove([White,Black], 1)
            if(MakeMove([White, Black], Move[1] ,White.Pieceplacement[Move[0]]) == 1):
                CheckMateState=CheckIfChessMate(Black,White)
                if CheckMateState==1: #Check if black is Chessmate
                    print("Black Is CheckMate")
                    return
                elif CheckMateState==2:
                    print("StaleMate")
                    return
                if Turn==1:
                    Turn=2
                else:
                    Turn=1

        else:
            Move = GetBestMove([White,Black], 2)
            if(MakeMove([Black, White], Move[1] ,Black.Pieceplacement[Move[0]]) == 1):
                CheckMateState=CheckIfChessMate(White,Black)
                if CheckMateState==1: #Check if White is Chessmate
                    print("White Is CheckMate")
                    return
                elif CheckMateState==2:
                    print("StaleMate")
                    return

                if Turn==1:
                    Turn=2
                else:
                    Turn=1

        DrawBoard([White,Black])
        clk.tick(60)

def semiauto(White, Black, clk):
    Turn=1
    while True:
        if Turn == 1:
            for event in pygame.event.get(): #Event    quoue
                if event.type==QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        #check if clicked field contains a piece
                        SelectedField=[int(float(event.pos[0])/SCREENSIZE[0]*8),int(float(event.pos[1])/SCREENSIZE[1]*8)]
                        if SelectedField in White.Pieceplacement:
                            PossibleMoves=FindPossibleMoves(SelectedField,White,Black)
                            DrawPossibilities([White,Black],SelectedField,PossibleMoves)
                            if(EnterChossingLoop([White,Black],SelectedField,PossibleMoves)==1):
                                CheckMateState=CheckIfChessMate(Black,White)
                                if CheckMateState==1: #Check if black is Chessmate
                                    print("Black Is CheckMate")
                                    return
                                elif CheckMateState==2:
                                    print("StaleMate")
                                    return
                                if Turn==1:
                                    Turn=2
                                else:
                                    Turn=1

        else:
            Move = GetBestMove([White,Black], 2)
            if(MakeMove([Black, White], Move[1] ,Black.Pieceplacement[Move[0]]) == 1):
                CheckMateState=CheckIfChessMate(White,Black)
                if CheckMateState==1: #Check if White is Chessmate
                    print("White Is CheckMate")
                    return
                elif CheckMateState==2:
                    print("StaleMate")
                    return

                if Turn==1:
                    Turn=2
                else:
                    Turn=1

        DrawBoard([White,Black])
        clk.tick(60)

def normal(White, Black, clk):
    Turn=1
    while True:
        for event in pygame.event.get(): #Event    quoue
            if event.type==QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    #check if clicked field contains a piece
                    SelectedField=[int(float(event.pos[0])/SCREENSIZE[0]*8),int(float(event.pos[1])/SCREENSIZE[1]*8)]
                    if Turn==1 and SelectedField in White.Pieceplacement:
                        PossibleMoves=FindPossibleMoves(SelectedField,White,Black)
                        DrawPossibilities([White,Black],SelectedField,PossibleMoves)
                        if(EnterChossingLoop([White,Black],SelectedField,PossibleMoves)==1):
                            CheckMateState=CheckIfChessMate(Black,White)
                            if CheckMateState==1: #Check if black is Chessmate
                                print("Black Is CheckMate")
                                return
                            elif CheckMateState==2:
                                print("StaleMate")
                                return
                            if Turn==1:
                                Turn=2
                            else:
                                Turn=1

                    elif Turn==2 and SelectedField in Black.Pieceplacement:
                        PossibleMoves=FindPossibleMoves(SelectedField,Black,White)
                        DrawPossibilities([White,Black],SelectedField,PossibleMoves)
                        if(EnterChossingLoop([Black,White],SelectedField,PossibleMoves)==1):
                            CheckMateState=CheckIfChessMate(White,Black)
                            if CheckMateState==1: #Check if White is Chessmate
                                print("White Is CheckMate")
                                return
                            elif CheckMateState==2:
                                print("StaleMate")
                                return

                            if Turn==1:
                                Turn=2
                            else:
                                Turn=1
        DrawBoard([White,Black])
        clk.tick(60)


pygame.init()
screen=pygame.display.set_mode(SCREENSIZE,0,32)
pygame.display.set_caption("PyChess", "PyCs") #Set title
if SCREENSIZE[0] > SCREENSIZE[1]:
    FONTBASIS = SCREENSIZE[1]
else:
    FONTBASIS = SCREENSIZE[0]
font = pygame.font.SysFont(FONT, int(float(FONTBASIS)/12))
White=Player(2)
Black=Player(1)
clock=pygame.time.Clock()
DrawBoard([White,Black])
if "-fullauto" in sys.argv:
    fullauto(White, Black, clock)
elif "-semiauto" in sys.argv:
    semiauto(White, Black, clock)
else:
    normal(White, Black, clock)
for event in pygame.event.get(): #Event    quoue
    if event.type==QUIT:
        sys.exit()
