# filename: 'Fade.py'
# author: Keith Carscadden
# date: 6/16/14
# purpose: provides fadein, fadeout functions for any screen (Game.py, intro, and all games)

import pygame as pg
from pygame.locals import *

def fadein(img,screen):
	screen.blit(img,(0,0))
	s = pg.Surface(img.get_size())
	s.fill((0,0,0))

	for i in range(0,256,4):
		pg.time.wait(2)
		s.set_alpha(255-i)
		screen.blit(img,(0,0))
		screen.blit(s,(0,0))
		pg.display.update()

def fadeout(img,screen,startPercent,endPercent):

	# blit original screen, pause, create black rect
    screen.blit(img,(0,0))
    pg.time.wait(250)
    s = pg.Surface(img.get_size())
    s.fill((0,0,0))

    t = int(550/((endPercent-startPercent)*255))

    # fade out slightly
    for i in range(int(startPercent*255),int(endPercent*255),4):
        pg.time.wait(t)
        s.set_alpha(i)
        screen.blit(img,(0,0))
        screen.blit(s,(0,0))
        pg.display.update()
