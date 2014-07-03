# filename: 'Minesweeper.py'
# author: Keith Carscadden
# date: 5/14/14
# purpose: Minesweeper game

import pygame as pg,sys,time
from random import randint
from pygame.locals import *
from ScoreScreen import ScoreScreen
import Fade

from os import environ
environ['SDL_VIDEO_CENTERED'] = '1'

WHITE = (255,255,255)
GRAY = (200,200,200)
RED = (255,0,0)

def __init__():
    main()

def main():

    global flagged,score,size,xgrid,ygrid,maxx,maxy,numberOfMines,screen,font

    global startTime,won
    startTime = time.time()

    score = won = 0

    size = 40
    xgrid,ygrid = 25,20
    maxx,maxy = size*xgrid,size*ygrid
    numberOfMines = 75

    screen = pg.display.set_mode((size*xgrid, size*ygrid))
    pg.display.set_caption('Minesweeper!')

    # constants
    running = True
    mousex,mousey = 0,0
    mouseDown = False
    turn = (255,0,0)
    font = pg.font.SysFont("monospace",25)
    gameOver = False

    # initial surface
    screen.fill(WHITE)
    mines = []
    first = 1
    flagged = []

    # main loop
    while running or gameOver:

        # event handling
        for ev in pg.event.get():

            if (ev.type == KEYDOWN and (ev.key == K_ESCAPE or ev.key == K_q)):
                running=False

            elif ev.type == QUIT:
                Fade.fadeout(screen.copy(),screen,0.0,1.0)
                pg.quit()
                sys.exit()

            if (ev.type == MOUSEBUTTONDOWN or ev.type == KEYDOWN) and gameOver:
                running=False
                gameOver = False

            elif ev.type == MOUSEBUTTONDOWN:

                button = pg.mouse.get_pressed()

                # actual clicks (l-click)
                if button[0]:
                    if ev.pos[0] < maxx and ev.pos[1] < maxy:
                        mouseDown = True
                        mousex,mousey = ev.pos
                # for flagging (r-click)
                elif button[2]:
                    coords = [(int(ev.pos[0]/int(maxx/xgrid))*int(maxx/xgrid)), (int(ev.pos[1]/int(maxy/ygrid))*int(maxy/ygrid))]
                    x,y = int(coords[0]/size),int(coords[1]/size)

                    # unflagging
                    if tuple(coords) in flagged:
                        flagged.remove(tuple(coords))
                        pg.draw.rect(screen,(255,255,255),(coords,(maxx/xgrid,maxy/ygrid)))
                        pg.display.update()

                    # flagging
                    else:
                        flagged.append(tuple(coords))
                        pg.draw.rect(screen,(255,255,0),(coords,(maxx/xgrid,maxy/ygrid)))
                        pg.display.update()

        # mouse up/down
        if mouseDown and running:

            mouseDown = 0

            # on first to make sure you don't click a mine
            if mines == []:
                mines = generateMines(screen,[mousex,mousey])

                # don't try to fix these lines up
                pg.draw.rect(screen,GRAY,([(int(mousex/int(maxx/xgrid))*int(maxx/xgrid)), (int(mousey/int(maxy/ygrid))*int(maxy/ygrid))],(maxx/xgrid,maxy/ygrid)))
                screen.blit(font.render(clickSquare(screen,mousex,mousey,mines,font,True),1,(0,0,0)),((int(mousex/int(maxx/xgrid))*int(maxx/xgrid)) + 6*maxx/(xgrid*18),(int(mousey/int(maxy/ygrid))*int(maxy/ygrid)) + 4*maxy/(ygrid*18)))

            running = clickSquare(screen,mousex,mousey,mines,font)

            if not running:
                gameOver = True
            elif running == 2:
                won = 1
                running = 0
                gameOver = 1

        # check if game is still running
        if running:
            drawGrid(screen)
            if first: # initial fade
                Fade.fadein(screen.copy(),screen)
                first = 0
            pg.display.flip()

        # quit if the games won, or the game is over
        if gameOver or won:
            quitProgramDisplayMines(screen,mines)
            gameOver = running = False

    sc = ScoreScreen(screen.copy(),0,time=int(time.time()-startTime),win=won)

# when a square is clicked
def clickSquare(display,x,y,mines,font,first=False):

    coords = [(int(x/int(maxx/xgrid))*int(maxx/xgrid)), (int(y/int(maxy/ygrid))*int(maxy/ygrid))]
    x,y = int(coords[0]/size),int(coords[1]/size)
    mineTouchingCount = 0
    draw = 0

    if tuple(coords) in flagged:
        return True

    # runs all time but first
    if not first:

        # not a mines
        if nums[y][x] != 'm':
            drawSingleSquare(display,x,y,0)

        # mine
        else:
            return False

    # returns number for first square
    else:
        return str(int(nums[y][x]))

    # flood fill
    floodfill(display,int(coords[0]/size),int(coords[1]/size))
    drawGrid(display)

    if checkForWin():
        return 2

    return True

def checkForWin():
    for rows in nums:
        for n in rows:
            if type(n) == int:
                return 0
    return 1

# recursive floodfill
# changed to check corners as well!
def floodfill(display,x,y):

    # using float num values as an indicator, if it's already been drawn
    # end case also includes mines, or going off the grid
    if (x<0 or x>=xgrid or y<0 or y>=ygrid) or type(nums[y][x]) == float or nums[y][x] == 'm':
        return
    if nums[y][x] != 0:
        drawSingleSquare(display,x,y)
        return

    drawSingleSquare(display,x,y)

    floodfill(display,x+1,y)
    floodfill(display,x-1,y)
    floodfill(display,x,y+1)
    floodfill(display,x,y-1)
    floodfill(display,x+1,y+1)
    floodfill(display,x-1,y-1)
    floodfill(display,x-1,y+1)
    floodfill(display,x+1,y-1)

def drawSingleSquare(display,x,y,n=1):
    label = font.render(str(int(nums[y][x])),1,(0,0,0))
    pg.draw.rect(display,GRAY,((x*size,y*size),(size,size)))
    display.blit(label,(x*size + maxx/(xgrid*3),y*size + 2*maxy/(ygrid*9)))
    if n: 
        nums[y][x] = float(nums[y][x])

# draw initial grid
def drawGrid(display):
    for x in range(0,maxx,int(maxx/xgrid)): pg.draw.line(display,(0,0,0),(x,0),(x,maxy),1)
    for y in range(0,maxy,int(maxy/ygrid)): pg.draw.line(display,(0,0,0),(0,y),(maxx,y),1)

# generate, return mine values **called once**
# called after first click
def generateMines(display,pos):

    # init
    isDisplayed,chosenMines = False,[(None,None)]*numberOfMines
    pos[0] = int(pos[0]/int(maxx/xgrid))*int(maxx/xgrid)
    pos[1] = int(pos[1]/int(maxy/ygrid))*int(maxy/ygrid)
    pos=pos[0],pos[1]

    # make sure there are no duplicates
    while 1:

        # random picks
        for x in range(numberOfMines):
            chosenMines[x-1] = (int(randint(0,xgrid-1)*(maxx/xgrid)),int(randint(0,ygrid-1)*(maxy/ygrid)))

        # check initial pick
        if pos in chosenMines:
            continue

        # check duplicates
        if len(chosenMines) == len(set(chosenMines)):
            if isDisplayed:
                for mine in chosenMines:
                    pg.draw.rect(display,(0,0,0),(mine,(maxx/xgrid,maxy/ygrid)))
            break

    global nums
    nums = []
    for i in range(ygrid):
        a = []
        for j in range(xgrid):
            try:
                b = chosenMines.index((j*size,i*size))
                a.append('m')
            except:
                a.append(0)

        nums.append(a)

    check = ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))
    for m in chosenMines:
        for c in check:
            x = int(m[0]/size) + c[0]
            y = int(m[1]/size) + c[1]
            if x >= xgrid or y >= ygrid or x < 0 or y < 0 or nums[y][x] == 'm':
                continue
            nums[y][x] += 1

    return chosenMines

def printl(a):
    for i in a:
        for j in i:
            print(j,'',end='')
        print()
    print()

# display all mines at the end
def quitProgramDisplayMines(display,mines):

    for mine in mines:
        pg.draw.rect(display,RED,(mine,(maxx/xgrid,maxy/ygrid)))

    drawGrid(display)
    pg.display.flip()

if __name__ == "__main__":
    main()
