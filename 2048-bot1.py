import pygame, sys
from pygame.locals import *
import random

windowwidth  = 640
windowheight = 480
boxwidth = 80
boxheight = 80
border = 4
cols = 4
rows = 4
fps = 3

white = (255, 255, 255)
blue = (0,204,204)
darkblue = (0,128,125)
lightBlue = (102, 255, 255)
black= (0,0,0)
darkturqoise = (3,54,73)

bgbox = darkblue
textcolor = white
boxcolor = blue
bgtext = lightBlue
bgcolor = black

xmargin = int((windowwidth - (boxwidth*cols))/2)
ymargin = int((windowheight - (boxheight*rows))/2)

prob = 0.9
totalScore = [0]
over = 0
levels = 6
mv = [0]

def main():
	global displaysurf, fpslock
	totalScore[0] = 0
	pygame.init()
	fpslock = pygame.time.Clock()
	displaysurf = pygame.display.set_mode((windowwidth,windowheight))
	mainBoard = Board()
	randomSelection(mainBoard)
	randomSelection(mainBoard)
	startAnimation(mainBoard)
	over = 0

	while True:
		if over == 1:
			showOvertext(white)
		while True:
			options(white)

			if over == 1:
				showOvertext(white)

			for event in pygame.event.get():
			
				if event.type ==  QUIT:
					pygame.quit()
					sys.exit()

				if event.type == MOUSEMOTION:
					mousex, mousey= event.pos
					if hoverOption(mousex,mousey,20):
						options(darkturqoise)
				
				if event.type == MOUSEBUTTONUP:
					mousex,mousey = event.pos
					if hoverOption(mousex, mousey,20):
						showOvertext(black)
						mainBoard = Board()
						over = 0
						randomSelection(mainBoard)
						randomSelection(mainBoard)
						startAnimation(mainBoard)
						totalScore[0] = 0
						continue
				
					
			if over==0:
				temp = [[mainBoard[i][j] for j in range(cols)] for i in range(rows)]	
				move = bestMove(temp,levels)
				print move,
				move = mv[0]
				print mv[0]
				check = [[mainBoard[i][j] for j in range(cols)] for i in range(rows)]	
				if move == 275:
					leftMove(mainBoard)
				elif move == 276:
					rightMove(mainBoard)	
				elif move == 273:
					upMove(mainBoard)
				elif move ==  274:
					downMove(mainBoard)

				if check == mainBoard:
					if isGameover(mainBoard):
						showOvertext(white)
						over = 1
						print True
					continue

				startAnimation(mainBoard)			
				showScore(totalScore[0])
				pygame.time.wait(100)	
				tempBoard = [[mainBoard[i][j] for j in range(cols)] for i in range(rows)]	
				if anySpace(mainBoard):
					randomSelection(mainBoard)
				if isGameover(mainBoard):
					showOvertext(white)
					over = 1
					print True
				cmpBoard(tempBoard, mainBoard)

		

def bestMove(board, levels):
	''' selects moves with maximum score '''

	if  isGameover(board):
		return -100

	if levels == 0:
		return totalScore[0]

	max_score = -1;
	score = totalScore[0]

	new_board = [[board[i][j] for j in range(cols)] for i in range(rows)]	
	leftMove(new_board)
	if anySpace(new_board):
		randomSelection(new_board)
	sc = bestMove(new_board,levels-1)
	if sc > max_score:
		max_score = sc
		mv[0] = 275	
	totalScore[0]-=totalScore[0]- score

	new_board = [[board[i][j] for j in range(cols)] for i in range(rows)]	
	rightMove(new_board)
	if anySpace(new_board):
		randomSelection(new_board)
	sc = bestMove(new_board,levels-1)
	if sc > max_score:
		max_score = sc
		mv[0] = 275	
	elif sc==max_score and random.random()>=0.98:
		mv[0] = 273			
	totalScore[0]-=totalScore[0]- score
	
	new_board = [[board[i][j] for j in range(cols)] for i in range(rows)]	
	upMove(new_board)
	if anySpace(new_board):
		randomSelection(new_board)
	sc = bestMove(new_board,levels-1)
	if sc > max_score:
		max_score = sc
		mv[0] = 273
	elif sc==max_score and random.random()>=0.5:
		mv[0] = 273	
	totalScore[0]-=totalScore[0]- score

	new_board = [[board[i][j] for j in range(cols)] for i in range(rows)]	
	downMove(new_board)
	if anySpace(new_board):
		randomSelection(new_board)
	sc = bestMove(new_board,levels-1)
	if sc > max_score:
		max_score = sc
		mv[0] = 274
	elif sc==max_score and random.random()>=0.5:
		mv[0] = 274	
	totalScore[0]-=totalScore[0]- score

	return max_score

def anySpace(board):
	for i in range(rows):
		for j in range(cols):
			if board[i][j] ==0:
				return True
	return False
				
def cmpBoard(board,mainBoard):
	for i in range(rows):
		flag = 0
		for j in range(cols):
			if board[i][j]!=mainBoard[i][j]:
				flag = 1
				break
		if flag == 1:
			break		

	left, top = topCoordinates(i,j)		
	displayDigit(left,top,mainBoard[i][j])

def downMove(board):
	for i in range(cols):
		curr = rows - 1
		count = 0
		for j in range(rows-1,-1,-1):
			if board[j][i] != 0:
				if count == 0:
					board[curr][i] = board[j][i]
					count+=1
				else:
					if board[j][i] ==  board[curr][i]:
						totalScore[0]+= board[j][i]*2
						board[curr][i]*=2
						curr-=1
						count = 0	
					else:
						curr-=1
						board[curr][i] = board[j][i]
		if count !=0:
			curr-=1
		for j in range(curr,-1,-1):
			board[j][i] = 0

def isGameover(board):
	flag = 0
	for i in range(rows):
		for j in range(cols):
			if board[i][j] == 0:
				flag = 1
				break 	

	if flag == 1:
		return False

	for i in range(0,rows):
		for j in range(1,cols):
			if board[i][j] == board[i][j-1]:
				return False

	for i in range(0,cols):
		for j in range(0,rows-1):
			if board[j][i] == board[j+1][i]:
				return False			
	return True

def upMove(board):
	for i in range(cols):
		curr = 0
		count = 0
		for j in range(rows):
			if board[j][i] != 0:
				if count == 0:
					board[curr][i] = board[j][i]
					count+=1
				else:
					if board[j][i] ==  board[curr][i]:
						totalScore[0]+= board[j][i]*2
						board[curr][i]*=2
						curr+=1	
						count = 0
					else:
						curr+=1
						board[curr][i] = board[j][i]
		if count !=0:
			curr+=1
		for j in range(curr,rows):
			board[j][i] = 0

def leftMove(board):
	for i in range(rows):
		curr = cols - 1
		count = 0

		for j in range(cols-1,-1,-1):
			if board[i][j] != 0:

				if count == 0:
					board[i][curr] = board[i][j]
					count = 1
				else:
					if board[i][j] == board[i][curr]:
						totalScore[0]+= board[i][j]*2
						board[i][curr]*=2
						curr-=1	
						count = 0
					else:
						curr-=1
						board[i][curr] = board[i][j]

						
		if count!=0:
			curr-=1

		for j in range(curr,-1,-1):
			board[i][j] = 0
							
def rightMove(board):
	for i in range(rows):
		curr = 0
		count = 0
		for j in range(cols):
			if board[i][j]!=0:
				if count == 0:
					board[i][curr] = board[i][j]
					count = 1
				else:
					if board[i][j] == board[i][curr]:
						totalScore[0]+= board[i][j]*2
						board[i][curr]*=2
						curr+=1	
						count = 0
					else:
						curr+=1
						board[i][curr] = board[i][j]		
		if count!=0:
			curr+=1

		for j in range(curr,cols):
			board[i][j] = 0	
						
def randomSelection(board):
	empty = emptyArray(board)
	digit = selectDigit()
	box = randomBox(empty)
	board[box[0]][box[1]] = digit

def randomBox(empty):
	return empty[random.randint(0,len(empty)-1)]

def emptyArray(board):
	empty = []

	for i in range(rows):
		for j in range(cols):
			if board[i][j] == 0:
				empty.append((i,j))

	return empty			

def Board():
	return [[0 for j in range(cols)] for i in range(rows)]

def selectDigit():
	if random.random()<=prob:
		return 2
	else:
		return 4	

def topCoordinates(x,y):
	left, top = xmargin + y*boxheight, ymargin + x*boxwidth
	return left, top

def displayDigit(left,top,digit):
	pygame.draw.rect(displaysurf,bgtext,(left,top,boxwidth-2,boxheight-2))
	fontObj = pygame.font.Font('freesansbold.ttf', 40)
	textSurfaceObj = fontObj.render(str(digit), True, textcolor,bgtext)
	textRecteObj = textSurfaceObj.get_rect()
	textRecteObj.center = (left+boxwidth/2,top+boxheight/2)
	displaysurf.blit(textSurfaceObj, textRecteObj)
	pygame.display.update()

def startAnimation(board):
	pygame.draw.rect(displaysurf,bgbox,(xmargin-border,ymargin-border,(boxwidth)*cols+border*2,(boxheight)*rows+border*2))

	for i in range(cols):
		for j in range(rows):
			left, top = topCoordinates(i,j)
			pygame.draw.rect(displaysurf,boxcolor,(left,top,boxwidth-2,boxheight-2))
			if board[i][j] != 0:
				displayDigit(left,top,board[i][j])
	showScore(0)			
	options(white)
	pygame.display.update()		

def showScore(score):
	pygame.draw.rect(displaysurf,black,(90,0,200,40))
	fontObj = pygame.font.Font('freesansbold.ttf', 20)
	textSurfaceObj = fontObj.render('Total Score : %d'%(score), True, white,bgcolor)
	textRecteObj = textSurfaceObj.get_rect()
	textRecteObj.center = (180,20)
	displaysurf.blit(textSurfaceObj,textRecteObj)
	pygame.display.update()

def hoverOption(x,y,size):
	boxRect= pygame.Rect(510,430,size*6,size+2)
	if boxRect.collidepoint(x,y):
		return True
	return False

def options(color):
	fontObj = pygame.font.Font('freesansbold.ttf', 20)
	textSurfaceObj = fontObj.render('New Game', True, color,black)
	textRecteObj = textSurfaceObj.get_rect()
	textRecteObj.center = (560, 440)
	displaysurf.blit(textSurfaceObj,textRecteObj)
	pygame.display.update()	

def showOvertext(color):
	fontObj = pygame.font.Font('freesansbold.ttf', 40)
	textSurfaceObj = fontObj.render('Game Over', True, color,black)
	textRecteObj = textSurfaceObj.get_rect()
	textRecteObj.center = (150, 430)
	displaysurf.blit(textSurfaceObj,textRecteObj)
	pygame.display.update()	

if __name__ == '__main__':
	main()