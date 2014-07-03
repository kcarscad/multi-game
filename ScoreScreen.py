# filename: 'ScoreScreen.py'
# author: Keith Carscadden
# date: 6/16/14
# purpose: ScoreScreen class, for use in all games, when the game is over (displays button, scores)

import sys,pygame as pg
from pygame.locals import *
import Minesweeper,Pong,Snake,Sudoku
import MenuButton
import Fade

class ScoreScreen():

    def __init__(self,i,p,**kwargs):

        self.img = i
        self.p = p
        self.w,self.h = self.img.get_size()
        self.font = pg.font.SysFont('Arial',45)
        self.screen = pg.display.set_mode(self.img.get_size())
        self.setscreen(kwargs)

    # set initial screen, vars
    def setscreen(self,args):

        Fade.fadeout(self.img,self.screen,0,0.7)

        self.buttons = [
            MenuButton.MenuButton(self.p,'Retry',int(self.w/2.0 - 300),500,200,100),
            MenuButton.MenuButton(None,'Quit',int(self.w/2.0 + 100),500,200,100)]

        # draw buttons, message, then main loop
        self.drawButton(self.buttons,0)
        self.displayMessage(args)
        self.main()

    def displayMessage(self,args):

        def drawText(t1,t2=''):

            f = pg.font.SysFont('Arial',83)

            s = f.size(t1)
            label = f.render(t1,1,(255,255,255))
            self.screen.blit(label,(self.w/2.0-s[0]/2.0,100))

            s = f.size(t2)
            label = f.render(t2,1,(255,255,255))
            self.screen.blit(label,(self.w/2.0-s[0]/2.0,220))
            pg.display.update()

        # minesweeper
        if self.p == 0:

            s,win = args['time'],args['win']

            t1 = ''
            if win:
                t1 = 'Congrats, you won!'
            else:
                t1 = 'You lost!'

            m,s = int(s/60),int(s%60)
            if m != 0:
                t2 = 'Time taken: {}m {}s'.format(m,s)
            else:
                t2 = 'Time taken: {}s'.format(s)

            drawText(t1,t2)

        # pong
        elif self.p == 1:

            s1,s2 = args['scores']
            winner = args['winner']

            t1 = ''
            if winner == 0 and s1 == s2:
                t1 = 'It was a draw!'
            elif winner == 1 or s1 > s2:
                t1 = 'Player 1 won!'
            elif winner == 2 or s2 > s1:
                t1 = 'Player 2 won!'

            t2 = '{} : {}'.format(s1,s2)

            drawText(t1,t2)
            
        # snake
        elif self.p == 2:
            
            score = args['score']

            t = 'Your score was {}'.format(score)

            drawText(t)
            
        # sudoku
        elif self.p == 3:
            
            s,win = args['time'],args['win']

            t1 = ''
            if win:
                t1 = 'Congrats, you won!'
            else:
                t1 = 'You lost!'

            m,s = int(s/60),int(s%60)
            if m != 0:
                t2 = 'Time taken: {}m {}s'.format(m,s)
            else:
                t2 = 'Time taken: {}s'.format(s)

            drawText(t1,t2)

    # draw the button, same as method in Game.py
    def drawButton(self,b,mouseOver):

        if type(b) != list:
            b = [b]

        for button in b:
            c = button.getbgclr(),button.getclr()
            c1,c2 = c if mouseOver else c[::-1]
            r = button.getrect()
            pg.draw.rect(self.screen,c2,r)
            pg.draw.rect(self.screen,c1,r,1)
            x,y,w,h = r
            s = self.font.size(button.gettext())
            label = self.font.render(button.gettext(),1,c1)
            self.screen.blit(label,[x+w/2.0-s[0]/2.0, y+h/2.0-s[1]/2.0])

        pg.display.update()


    def main(self):
        quit = 0
        clicked = False
        p = 1
        while not clicked:
            for ev in pg.event.get():

                # mousing over
                if ev.type == MOUSEMOTION:

                    # draw negative of button
                    for b in self.buttons:
                        if not b.mousedOver() and b.checkIfOnButton(ev.pos):
                            b.setMousedOver(1)
                            self.drawButton(b,1)
                            break
                        elif b.mousedOver() and not b.checkIfOnButton(ev.pos):
                            b.setMousedOver(0)
                            self.drawButton(b,0)
                            break

                if ev.type == QUIT:
                    quit = 1
                    break

                # clicking
                if ev.type == MOUSEBUTTONDOWN:
                    for b in self.buttons:
                        if b.checkIfOnButton(ev.pos):
                            p = b.getprogram()
                            break

                elif ev.type == KEYDOWN:
                    if ev.key == K_r:
                        p = self.buttons[0].getprogram()
                        break
                    elif ev.key == K_q or ev.key == K_ESCAPE:
                        p = self.buttons[1].getprogram()
                        break

            # go wherever they clicked
            if p == None:
                clicked = True
                Fade.fadeout(self.img,self.screen,0.7,1.0)

            elif type(p) != int:
                clicked = True
                Fade.fadeout(self.img,self.screen,0.7,1.0)
                p.main()

            if quit:
                Fade.fadeout(self.img,self.screen,0.7,1.0)
                pg.quit()
                sys.exit()