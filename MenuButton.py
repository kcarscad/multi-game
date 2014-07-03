# filename: 'MenuButton.py'
# author: Keith Carscadden
# date: 6/8/14
# purpose: MenuButton class, for menu in Game.py

from Minesweeper import Minesweeper
from Pong import Pong
from Snake import Snake
from Sudoku import Sudoku

class MenuButton():

    ids = ['minesweeper','pong','snake','sudoku']

    def __init__(self,p,t,x,y,w,h):
        if type(p)==int:
            if p==0:
                self.program = Minesweeper
            elif p==1:
                self.program = Pong
            elif p==2:
                self.program = Snake
            elif p==3:
                self.program = Sudoku
        else:
            self.program=p
        self.text=t
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.clr=(0,0,0)
        self.bgclr=(255,255,255)
        self.mouse = 0

    def getrect(self):
        return [self.x,self.y,self.w,self.h]
    def getprogram(self):
        return self.program
    def getclr(self):
        return self.clr
    def getbgclr(self):
        return self.bgclr
    def gettext(self):
        return self.text
    def setMousedOver(self,m):
        self.mouse = m
    def mousedOver(self):
        return self.mouse

    def checkIfOnButton(self,pos):
        x,y=pos
        if self.x < x < self.x+self.w and self.y < y < self.y+self.h:
            return True
        return False

    def __repr__(self):
        return 'program:{} x:{} y:{} w:{} h:{}'.format(self.program,self.x,self.y,self.w,self.h)