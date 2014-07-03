# filename: 'Sudoku.py'
# author: Keith Carscadden
# date: 6/1/14
# purpose: Sudoku game, uses 3rd party file 'generator.py'

import math,sys,os,time,pygame as pg
from pygame.locals import *
from random import randint
from ScoreScreen import ScoreScreen
import Fade

from os import environ
environ['SDL_VIDEO_CENTERED'] = '1'

BG = (255,255,255)
C1 = (0,0,0)
C2 = (120,120,120)
HL = (255,255,0)
N = 9
T = 3

# random number, 1-N (9)
def rnd():
    return randint(1,N)

# draw the number at the clicked position
def drawNum(n,pos,option=0):

    x,y = pos
    c = C2

    if not locked[x][y] or option==2:

        if option==1:
            locked[x][y] = 1
            c = C1
        elif option==2:
            c = (0,255,0)

        i,j = coords[pos]
        k,l = fontSize
        pg.draw.rect(screen,BG,[i,j,k,l])

        # draw num
        if n:
            label = font.render(str(n),1,c)
            screen.blit(label,coords[pos])

        board[x][y] = n

# draw grid
def drawLines(w,h):
    [pg.draw.line(screen,C1,[i*w/N,0],[i*w/N,h],T if i%3==0 else 1) for i in range(N+1)]
    [pg.draw.line(screen,C1,[0,i*h/N],[w,i*h/N],T if i%3==0 else 1) for i in range(N+1)]

# blink waiting for input
def blink(board,pos,oldPos,dark):

    # make sure it changed, neither are blank, and the old number wasn't taken
    # will also be called if a locked tile == currently clicked (fills in old one)
    if pos != oldPos and pos and oldPos:
        a,b = coords[oldPos]
        c,d = fontSize
        pg.draw.rect(screen,BG,[a,b,c,d])
        if board[oldPos[0]][oldPos[1]]:
            c=C2 if not locked[oldPos[0]][oldPos[1]] else C1
            label = font.render(str(board[oldPos[0]][oldPos[1]]),1,c)
            screen.blit(label,coords[oldPos])


    if not locked[pos[0]][pos[1]]:

        # draw blinking line
        c = C1 if dark else BG
        x1 = x2 = coords[pos][0] + fontSize[0]/2.0
        y1 = coords[pos][1]+3
        y2 = coords[pos][1] + fontSize[1]-3

        pg.draw.line(screen,c,[x1,y1],[x2,y2])

        # redraw if the number was already picked
        num = board[pos[0]][pos[1]]
        if num :
            label = font.render(str(num),1,C2)
            screen.blit(label,coords[pos])

def checkWin():

    # check if the board == full
    for row in board:
        if 0 in row:
            return 0

    # columns
    cols=[]
    for i in range(9):
        c = []
        for j in range(9):
            c.append(board[j][i])
        cols.append(c)

    # boxes
    boxes = []
    for i in range(3):
        for j in range(3):
            b = []
            for k in range(3):
                for l in range(3):
                    b.append(board[3*i+k][3*j+l])
            boxes.append(b)

    # check for any common numbers in rows,cols,boxes
    for i in cols+board+boxes:
        if len(i) != len(set(i)):
            return 0

    return 1

def win():
    for i in range(9):
        for j in range(9):
            drawNum(board[i][j],(i,j),2)

############ MAIN ############

def main():

    global screen,board,locked,coords,puzzle,font,fontSize

    from . import generator

    puzzle = generator.main()

    global startTime,won
    startTime = time.time()
    won = 0

    pg.init()
    size = width,height = int(200/2*N),int(200/2*N)
    xunit,yunit = int(width/N),int(height/N)
    screen = pg.display.set_mode((width+int(T/2),height+int(T/2))) # +T to account for thick lines
    pg.display.set_caption('Sudoku')
    screen.fill(BG)
    drawLines(width,height)

    # clock for ticking, font
    clock = pg.time.Clock()
    font = pg.font.SysFont('Arial',63)
    fontSize = font.size('1')

    # create coordinates dictionary
    # takes a tuple of coords (1-9,1-9)
    # ready to use with drawing fonts/rects
    coords = {}
    for i,y in enumerate(range(0,height,yunit)):
        for j,x in enumerate(range(0,width,xunit)):
            a = x + xunit/2.0 - fontSize[0]/2.0 + int(j/3) # x + halfunitx - halfselfx + accountForThickLines
            b = y + yunit/2.0 - fontSize[1]/2.0 + int(i/3) # CHANGE LAST COMPONENT FOR MINOR CHANGES IF NEEDED, WITH SIZING
            coords[(j,i)] = a,b

    # board:
    # locked: which numbers are correct (there from start, maybe other use later)
    # 2d lists.... board[2][0] == 3rd from the left, top row
    board = [[0]*N for i in range(N)]
    locked = [[0]*N for i in range(N)]

    # initial board
    for i in range(9):
        for j in range(9):
            if puzzle[i][j]:
                drawNum(puzzle[i][j],(i,j),1)

    Fade.fadein(screen.copy(),screen)

    pg.display.flip()


    running = darkBlinkingLine = True # main loop :
    blinking = picked = False # blinking line : already picked a number at pos
    pos=oldPos=c=0

    while running:

        # event handling
        for ev in pg.event.get():

            # keep track of clicks, blinking
            if ev.type == MOUSEBUTTONDOWN:
                oldPos,pos = pos,(int(ev.pos[0]/xunit),int(ev.pos[1]/yunit))
                blinking = True
                c,darkBlinkingLine=79,1
                picked = False

                # for clicking a little bit too far
                if pos[0] > 8:
                    pos = (8,pos[1])
                if pos[1] > 8:
                    pos = (pos[0],8)

            # quit
            elif ev.type == KEYDOWN and (ev.key == K_ESCAPE or ev.key == K_q):
                running = False

            elif ev.type == QUIT:
                Fade.fadeout(screen.copy(),screen,0.0,1.0)
                pg.quit()
                sys.exit()

            # draw number if number pressed, mouse clicked
            if ev.type == KEYDOWN:

                # for numbers
                if 49 <= ev.key <= 57 and not picked:
                    picked = True
                    blinking = False
                    drawNum(ev.key-48,pos) # -48 to index it from 0-8
                    if checkWin():
                        win()
                        won = 1

                elif ev.key == K_BACKSPACE:
                    drawNum(0,pos)

                # arrow keys to navigate around
                if (blinking or picked) and ev.key in [K_UP,K_DOWN,K_LEFT,K_RIGHT]:
                    drawNum(board[pos[0]][pos[1]],pos)
                    oldPos=pos
                    c,darkBlinkingLine=79,1
                    blinking,picked=True,False

                    # position changing
                    if ev.key == K_UP:
                        pos = (pos[0],pos[1]-1)
                    elif ev.key == K_DOWN:
                        pos = (pos[0],pos[1]+1)
                    elif ev.key == K_RIGHT:
                        pos = (pos[0]+1,pos[1])
                    elif ev.key == K_LEFT:
                        pos = (pos[0]-1,pos[1])

                    # correct going past allowed values
                    if pos[0] > 8:
                        pos = (8,pos[1])
                    elif pos[0] < 0:
                        pos = (0,pos[1])
                    if pos[1] > 8:
                        pos = (pos[0],8)
                    elif pos[1] < 0:
                        pos = (pos[0],0)

        # for blinking
        if blinking:
            c+=1
            if c%80==0:
                blink(board,pos,oldPos,darkBlinkingLine)
                darkBlinkingLine = 0 if darkBlinkingLine else 1
                c=0


        # update, regulate fps for blinking
        pg.display.flip()
        clock.tick(100)

    score = None
    sc = ScoreScreen(screen.copy(),3,time=time.time()-startTime,win=won)

if __name__ == "__main__":
    main()
