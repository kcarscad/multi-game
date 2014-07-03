# filename: 'Snake.py'
# author: Keith Carscadden
# date: 5/20/14
# purpose: Simple snake game, no other classes used

import pygame as pg
from pygame.locals import *
import math,random,sys
from random import randint
from copy import copy
from ScoreScreen import ScoreScreen
import Fade

from os import environ
environ['SDL_VIDEO_CENTERED'] = '1'

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
FUSCHIA = (255,0,255)
s = 20
w,h=800,800

def RANDOMCOLOR():
    return randint(75,180),randint(75,180),randint(75,180)

def drawGrid(screen):
    for x in range(0,w,s): pg.draw.line(screen,WHITE,(x,0),(x,h))
    for y in range(0,h,s): pg.draw.line(screen,WHITE,(0,y),(h,y))

def updateScore(screen,font,score,n):

    if not n:
        pg.draw.rect(screen,BLACK,[10,10,50,100])
    else:
        score = 'Score: '+str(score)
        label = font.render(score,1,WHITE)
        screen.blit(label,(10,10))

def drawSnake(screen,boxes,c=WHITE):

    # for gradient
    col = []
    l=len(boxes)
    for i in range(l):
        col.append((255-255.0*i/l,255-255.0*i/l,255-255.0*i/l))

    for n,box in enumerate(boxes):
        x,y = box[0],box[1]
        if c == WHITE: # regular drawing
            pg.draw.rect(screen,col[n],[x,y,s,s])
            pg.draw.rect(screen,GREEN,[x,y,s,s],1)
        elif c: # red square or random colour square
            pg.draw.rect(screen,c,[x,y,s,s])
        else: # ouline all squares in red
            pg.draw.rect(screen,RED,[x,y,s,s],1)

def main():

    # init
    pg.init()
    screen = pg.display.set_mode((w,h))
    pg.display.set_caption('Snake')
    screen.fill(BLACK)
    x,y = (int(((w-s)/2)/s))*s,(int(((h-s)/2)/s))*s
    gameOver = 0
    dropCoords = [(int((randint(0,w-s))/s))*s,(int((randint(0,h-s))/s))*s]
    clock = pg.time.Clock()
    font = pg.font.SysFont('Arial',20)

    # up,down,left,right
    leftRight = [0,0]
    upDown = [0,0]
    boxes = [[x,y]]

    drawSnake(screen,boxes)

    Fade.fadein(screen.copy(),screen)

    direction = [0,0]
    running=True
    randomColor = RANDOMCOLOR()
    justDropped = 0
    score = 0
    paused = 0

    while running:

        if paused:
            paused = 0
            a=1
            while a:
                key = pg.key.get_pressed()
                if not key[K_p]:
                    a=0
            a=1
            while 1:
                key = pg.key.get_pressed()
                print('now here')
                if key[K_p]:
                    a=0
            a=1
            while 1:
                key = pg.key.get_pressed()
                if not key[K_p]:
                    a=0

        oldUpDown = upDown
        oldLeftRight = leftRight

        # event handling
        for ev in pg.event.get():

            if ev.type==QUIT:
                Fade.fadeout(screen.copy(),screen,0.0,1.0)
                pg.quit()
                sys.exit()

            elif ev.type == KEYDOWN:
                k = ev.key

                if k == K_p:
                    paused = 1

                if k == K_q or k == K_ESCAPE:
                    running=False

                if k == K_LEFT or k == K_a:
                    if leftRight[1]:
                        break
                    else:
                        leftRight=[1,0]
                        upDown = [0,0]
                elif k == K_RIGHT or k == K_d:
                    if leftRight[0]:
                        break
                    else:
                        leftRight=[0,1]
                        upDown = [0,0]
                if k == K_DOWN or k == K_s:
                    if upDown[0]:
                        break
                    else:
                        upDown=[0,1]
                        leftRight = [0,0]
                elif k == K_UP or k == K_w:
                    if upDown[1]:
                        break
                    else:
                        upDown=[1,0]
                        leftRight = [0,0]

        # for a weird bug
        if (oldUpDown == upDown[::-1] and oldUpDown != [0,0]):
            upDown = oldUpDown
        if (oldLeftRight == leftRight[::-1] and oldLeftRight != [0,0]):
            leftRight = oldLeftRight

        # hitting itself
        if len(boxes)>3:
            for b in boxes:
                if boxes.index(b) != len(boxes)-1-boxes[::-1].index(b):
                    gameOver = 1
                    drawSnake(screen,[boxes[0]],RED) # draw red square
                    drawSnake(screen,boxes,None) # outline all squares in red
                    pg.display.update()

        # check if player ran over the drop
        if dropCoords in [x for x in boxes]:
            score+=1
            boxes.insert(1,dropCoords)
            a,b = (int((randint(0,w-s))/s))*s,(int((randint(0,h-s))/s))*s
            randomColor = RANDOMCOLOR()
            drawSnake(screen,[[a,b]],randomColor)
            dropCoords = [a,b]
            justDropped = 1

        # if the game is over
        if x>=w or x+s<=0 or y+s<=0 or y>=h:
            gameOver=1
            drawSnake(screen,boxes,None)
            pg.display.flip()

        if gameOver:
            running = 0

        # move values down
        i = len(boxes)-1 if (len(boxes) > 2 and not justDropped) else 0
        while i >= 1:
            boxes[i] = list(boxes[i-1])
            i-=1

        justDropped = 0

        if 1 in upDown+leftRight:
            if len(boxes) <= 2:
                boxes.insert(1,[x,y])
            if upDown[1]:
                y+=s
                boxes[0][1] += s
            elif upDown[0]:
                y-=s
                boxes[0][1] -= s
            if leftRight[0]:
                x-=s
                boxes[0][0] -= s
            elif leftRight[1]:
                x+=s
                boxes[0][0] += s

        if running:
            screen.fill(BLACK)
            updateScore(screen,font,score,0)
            drawSnake(screen,[dropCoords],randomColor)
            drawSnake(screen,boxes)
            updateScore(screen,font,score,1)
            if not gameOver:
                pg.display.flip()
            clock.tick(18)

    sc = ScoreScreen(screen.copy(),2,score=score)

if __name__=='__main__':
    main()
