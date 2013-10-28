#implement a chess game in python.
import sys
import pygame
from pygame.locals import *

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
		if self.Playernr==1:
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
		
					
def FindPossibleMoves(Field,thePlayer,theOpponent): #Contains most of gamelogic and rules. Most bugs will probably be here.
	Piece=thePlayer.Pieceplacement.index(Field)
	print Piece
	Moves=[]
	if Piece<8: #This is a pessant
		if thePlayer.AlivePieces[Piece][2]==0: #First move for this piece
			if thePlayer.Playernr==1: #White
				return([Field[0],Field[1]-1],[Field[0],Field[1]-2])
			else:
				return([Field[0],Field[1]+1],[Field[0],Field[1]+2])
		else:
			if thePlayer.AlivePieces[Piece][1]==2: #check if transformed to queen
				#Queenmoves
				pass
			if the.Player.Playernr==1: #White
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
		pass #
		#Check horisontal
		i=0
		while (Field[0]+i<=7):
			i+=1
			if not ([Field[0]+i,Field[1]] in thePlayer.Pieceplacement or [Field[0]+i,Field[1]] in theOpponent.Pieceplacement):
				Moves.append([[Field[0]+i,Field[1]])
			else:
				if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
					Moves.append([Field[0]+i,Field[1]])
					break
				else:
					break
				
		i=0
		while (Field[0]+i>=0):
			i-=1
			if not ([Field[0]+i,Field[1]] in thePlayer.Pieceplacement or [Field[0]+i,Field[1]] in theOpponent.Pieceplacement):
				Moves.append([[Field[0]+i,Field[1]])
			else:
				if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
					Moves.append([Field[0]+i,Field[1]])
					break
				else:
					break
		#Check Vertical
		i=0
		while (Field[1]+i<=7):
			i+=1
			if not ([Field[0],Field[1]+i] in thePlayer.Pieceplacement or [Field[0],Field[1]+i] in theOpponent.Pieceplacement):
				Moves.append([[Field[0],Field[1]+i])
			else:
				if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
					Moves.append([Field[0],Field[1]+i])
					break
				else:
					break
				
		i=0
		while (Field[0]+i>=0):
			i-=1
			if not ([Field[0],Field[1]+i] in thePlayer.Pieceplacement or [Field[0],Field[1]+i] in theOpponent.Pieceplacement):
				Moves.append([[Field[0],Field[1]+i])
			else:
				if [Field[0]+i,Field[1]] in theOpponent.Pieceplacement:
					Moves.append([Field[0],Field[1]+i])
					break
				else:
					break

		
	elif Piece==9 or Piece==14: #Horse
		pass>>> 

	elif Piece==10 or Piece==13 #Runner
		pass
	elif Piece==11: #Queen
		pass
	elif Piece==12: #King
		pass
	return Moves

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
										
	pygame.display.flip()	
pygame.init()
screen=pygame.display.set_mode(SCREENSIZE,0,32)
pygame.display.set_caption("PyChess", "PyCs") #Set title
White=Player(1)
Black=Player(2)
clock=pygame.time.Clock()
DrawBoard([White,Black])
Turn=2
while 1: #Gameloop
	for event in pygame.event.get(): #Event	quoue
		if event.type==QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button==1:
				#check if clicked field contains a piece
				SelectedField=[int(float(event.pos[0])/SCREENSIZE[0]*8),int(float(event.pos[1])/SCREENSIZE[1]*8)]
				if Turn==1 and SelectedField in White.Pieceplacement:
					FindPossibleMoves(SelectedField,White,Black)
				elif Turn==2 and SelectedField in Black.Pieceplacement:
					FindPossibleMoves(SelectedField,Black,White)
					
					
	clock.tick(60)
