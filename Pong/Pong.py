# filename: 'Pong.py'
# author: Keith Carscadden
# date: 5/25/14
# purpose: Simple 2 player pong game

import math,sys,pygame as pg
from pygame.locals import *
from random import randint
from .Ball import Ball
from .Paddle import Paddle
from ScoreScreen import ScoreScreen
import Fade

from os import environ
environ['SDL_VIDEO_CENTERED'] = '1'

def drawBall(b):
    pg.draw.circle(screen,BG,b.getoldcoords(),b.getsize())
    pg.draw.circle(screen,b.getclr(),b.getcoords(),b.getsize())
    pg.draw.circle(screen,BG,b.getcoords(),b.getsize(),1)
    return b
def drawPaddle(p):
    pg.draw.rect(screen,BG,p.getoldrect())
    pg.draw.rect(screen,p.getclr(),p.getrect())
    return p
def randcol():
    return randint(0,255),randint(0,255),randint(0,255)
def drawlines():
    [pg.draw.line(screen,FG,[0,n*height/10.0],[width,n*height/10.0]) for n in range(10)]
    [pg.draw.line(screen,FG,[n*width/10.0,0],[n*width/10.0,width]) for n in range(10)]
def drawLine():
    pg.draw.line(screen,FG,[width/2.0,0],[width/2.0,height],2)
def displayScore(s1,s2,n=0):
    if n:
        pg.draw.rect(screen,BG,[int(width/2.0-90),20,40,100])
        pg.draw.rect(screen,BG,[int(width/2.0+ 50),20,40,100])

    scores = [str(s1),str(s2)]
    offx = [-90,50]
    for n,s in enumerate(scores):
        size = font.size(s)
        label = font.render(s,1,FG)
        screen.blit(label,(width/2.0+offx[n]+size[0]/2.0,20))


def main():

    global BG,FG,screen,width,height,font

    BG = (0,0,0)
    FG = (255,255,255)

    # init
    pg.init()
    size = width, height = 800,800
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Pong')
    clock = pg.time.Clock()
    font = pg.font.SysFont('Arial',40)

    screen.fill(BG)
    drawLine()

    ball = Ball(int(width/2.0),int(height/2.0),12,FG,[1 if randint(0,1) is 1 else -1,1 if randint(0,1) is 1 else -1],width,height)
    p1 = Paddle(0,height/2.0-3*height/40.0,width/25.0,3*height/20.0,FG,height)
    p2 = Paddle(width-width/25.0,height/2.0-3*height/40.0,width/25.0,3*height/20.0,FG,height)

    drawBall(ball)
    drawPaddle(p1)
    drawPaddle(p2)

    Fade.fadein(screen.copy(),screen)

    pg.display.flip()

    s1,s2 = 0,0
    displayScore(s1,s2)

    inc = 20
    running = 1
    started = scoreUpdated = 0
    while running:

        # event handling
        for ev in pg.event.get():

            # non-game keys pressed
            if ev.type is KEYDOWN:

                # quit
                if ev.key is K_ESCAPE or ev.key is K_q:
                    running = False

                # reset
                elif ball.gameOver():

                    screen.fill(BG)
                    displayScore(s1,s2,1)
                    drawLine()

                    ball = Ball(int(width/2.0),int(height/2.0),12,FG,[1 if randint(0,1) is 1 else -1,1 if randint(0,1) is 1 else -1],width,height)
                    p1 = Paddle(0,height/2.0-3*height/40.0,width/25.0,3*height/20.0,FG,height)
                    p2 = Paddle(width-width/25.0,height/2.0-3*height/40.0,width/25.0,3*height/20.0,FG,height)

                    drawBall(ball)
                    drawPaddle(p1)
                    drawPaddle(p2)

                    if running:
                        pg.display.flip()

                    started = scoreUpdated = 0

                # start
                elif not started:

                    started = 1
                    ball.resetDirection()


            # quit
            if ev.type is QUIT:
                Fade.fadeout(screen.copy(),screen,0.0,1.0)
                pg.quit()
                sys.exit()

        # if the games going on
        if not ball.gameOver() and started and running:

            displayScore(s1,s2,1)

            # check, update, draw ball
            drawBall(ball.checkIfHit(p1,p2).update())

            # redraw if hit, in case
            for p in p1,p2:
                if p.wasHit():
                    pg.display.update(drawPaddle(p).getwholerect())

            # check for up/down/w/s keys pressed
            keys = pg.key.get_pressed()
            if 1 in keys[:300]:
                if keys[K_w]:
                    drawPaddle(p1.moveByY(-inc))
                elif keys[K_s]:
                    drawPaddle(p1.moveByY(inc))
                if keys[K_UP]:
                   drawPaddle(p2.moveByY(-inc))
                elif keys[K_DOWN]:
                    drawPaddle(p2.moveByY(inc))

            displayScore(s1,s2)
            drawLine()
            pg.display.update()
            clock.tick(90)

        if ball.gameOver() and not scoreUpdated:
            scoreUpdated = 1

            if ball.getx() < width/2.0:
                s2 += 1
            else:
                s1 += 1

            displayScore(s1,s2,1)

            pg.display.update()

        if s1 >= 7 or s2 >= 7:
            running = 0

    score = [0,0]
    winner = 0
    if s1 >= 7:
        winner = 1
    elif s2 >= 7:
        winner = 2
    sc = ScoreScreen(screen.copy(),1,scores=(s1,s2),winner=winner)

if __name__ == "__main__":
    main()