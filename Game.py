# filename: 'Game.py'
# author: Keith Carscadden
# date: 6/8/14
# purpose: Main menu screen, to access other games

import pygame as pg
from pygame.locals import *
import random,math,sys
from MenuButton import MenuButton
import Fade

from os import environ
environ['SDL_VIEO_CENTERED'] = '1'

BG = (255,255,255)
FG = (0,0,0)

w,h = 300,100
buttons =  [MenuButton(0,'Minesweeper',50,200,w,h),
            MenuButton(1,'Pong',450,200,w,h),
            MenuButton(2,'Snake',50,400,w,h),
            MenuButton(3,'Sudoku',450,400,w,h)]

pg.init()

# for drawing a list of buttons, or single button
def drawButton(b,mouseOver):

    if type(b) == MenuButton:
        b = [b]

    for button in b:
        c = button.getbgclr(),button.getclr()
        c1,c2 = c if mouseOver else c[::-1]
        r = button.getrect()
        pg.draw.rect(screen,c2,r)
        pg.draw.rect(screen,c1,r,1)
        x,y,w,h = r
        font = pg.font.SysFont('Arial',45)
        s = font.size(button.gettext())
        label = font.render(button.gettext(),1,c1)
        screen.blit(label,[x+w/2.0-s[0]/2.0, y+h/2.0-s[1]/2.0])

# initialize screen
def setScreen(n=0):

    if n: 
        global screen

    screen = pg.display.set_mode(size)
    pg.display.set_caption('Quad Game')
    screen.fill(BG)
    drawButton(buttons,0)

    titleFont = pg.font.SysFont('Arial',75)
    t = 'Quad Game'
    s = titleFont.size(t)
    label = titleFont.render(t,1,FG)
    screen.blit(label,(width/2.0-s[0]/2.0,50))

    Fade.fadein(screen.copy(),screen)

    pg.display.update()

size = width, height = 800,600
setScreen(1)
clock = pg.time.Clock()

program = None
running = 1
while running:

    # event handling
    for ev in pg.event.get():

        # quit
        if (ev.type == KEYDOWN and (ev.key == K_ESCAPE or ev.key == K_q)) or ev.type == QUIT:
            running = False

        # mousing over
        if ev.type == MOUSEMOTION:

            # draw negative of button
            for b in buttons:
                if not b.mousedOver() and b.checkIfOnButton(ev.pos):
                    b.setMousedOver(1)
                    drawButton(b,1)
                    break
                elif b.mousedOver() and not b.checkIfOnButton(ev.pos):
                    b.setMousedOver(0)
                    drawButton(b,0)
                    break

        # clicking on button, launching game
        if ev.type == MOUSEBUTTONDOWN:
            for b in buttons:
                if b.checkIfOnButton(ev.pos):
                    program = b.getprogram()
                    break

    if program:
        p = program
        Fade.fadeout(screen.copy(),screen,0.0,1.0)
        program.main()
        setScreen()
        program = None

    pg.display.update()
    clock.tick(60)

Fade.fadeout(screen.copy(),screen,0.0,1.0)
pg.quit()
sys.exit()
