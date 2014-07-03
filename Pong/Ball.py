# filename: 'Ball.py'
# author: Keith Carscadden
# date: 5/25/14
# purpose: Ball class, for use by Pong.py

from sys import exit
from random import randint
import math
from math import pi

# input degrees
def sin(a):
    return math.sin(a*pi/180.0)
def cos(a):
    return math.cos(a*pi/180.0)
def tan(a):
    return math.tan(a*pi/180.0)

class Ball():

    # init
    def __init__(self,x,y,s,c,direction,w,h):
        self.x=x
        self.y=y
        self.size=s
        self.clr=c
        self.speed = 6.0
        self.direction = [self.speed*direction[0],self.speed*direction[1]]
        self.oldx=x
        self.oldy=y
        self.maxw = w
        self.maxh = h
        self.point = 0

    # getters
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getcoords(self):
        return [self.x,self.y]
    def getsize(self):
        return int(self.size)
    def getclr(self):
        return self.clr
    def getoldcoords(self):
        return [self.oldx,self.oldy]
    def getwholerect(self):
        w,h =   abs(self.x-self.oldx)+2*self.size, \
                abs(self.y-self.oldy)+2*self.size
        x,y =   (self.x if self.x < self.oldx else self.oldx)-self.size, \
                (self.y if self.y < self.oldy else self.oldy)-self.size
        return [x,y,w,h]
    def resetDirection(self):
        d = [1 if randint(0,1) is 1 else -1,1 if randint(0,1) is 1 else -1]
        self.direction=[d[0]*self.speed,d[1]*self.speed]

    def setGameOver(self):
        self.point = 1

    # update with speed,direction
    def update(self):
        if not self.point:
            self.oldx=self.x
            self.oldy=self.y
            self.x += int(self.direction[0])
            self.y += int(self.direction[1])
        return self

    def gameOver(self):
        return self.point

    def checkIfHit(self,p1,p2):

        if p1.getx()+p1.getw() >= self.x-self.size:
            if p1.gety()-self.size/2.0 <= self.y <= p1.gety()+p1.geth()+self.size/2.0:

                percent = (self.y-p1.gety())/p1.geth()
                angle = 180-(120*percent + 30)

                self.direction = [-self.direction[0],self.speed/tan(angle)]

                p1.isHit()

            else:
                self.point = 1
                p1.addScore(1)
        elif p2.getx() <= self.x+self.size:
            if p2.gety()-self.size/2.0 <= self.y <= p2.gety()+p2.geth()+self.size/2.0:

                percent = ((self.y-p2.gety())/p2.geth())
                angle = 120*percent + 30

                self.direction = [-self.direction[0],-self.speed/tan(angle)]

                p2.isHit()

            else:
                self.point = 1
                p2.addScore(1)

        # for top,bottom hits
        if self.y-self.size <= 0:
            self.direction[1] *= -1
        elif self.y+self.size >= self.maxh:
            self.direction[1] *= -1

        return self

    # string
    def __repr__(self):
        return 'dir:{} x:{} y:{} size:{} c:{}'.format(self.direction,self.x,self.y,self.size,self.clr)