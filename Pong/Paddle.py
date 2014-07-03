# filename: 'Paddle.py'
# author: Keith Carscadden
# date: 5/25/14
# purpose: Paddle class, for use by Pong.py

class Paddle():

    # init
    def __init__(self,x,y,w,h,c,s):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.clr = c
        self.oldrect = self.getrect()
        self.screenHeight = s
        self.inc=0
        self.hit=0
        self.score=0

    # getters
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getw(self):
        return self.w
    def geth(self):
        return self.h
    def getclr(self):
        return self.clr
    def getrect(self):
        return [self.x,self.y,self.w,self.h]
    def getoldrect(self):
        return self.oldrect
    def getwholerect(self):
        self.hit = False
        x=self.x
        w=self.w
        h=self.h + abs(self.inc)
        y=min(self.y,self.oldrect[1])
        return [x,y,w,h]

    def addScore(self,n):
        self.score += n

    def getScore(self):
        return self.score

    def isHit(self):
        self.hit=True

    def wasHit(self):
        return self.hit

    # check roof hit
    def checky(self):
        if self.y > self.screenHeight-self.h:
            self.y = self.screenHeight-self.h
        elif self.y < 0:
            self.y = 0

    # move methods
    def moveByY(self,y):
        self.oldrect = [self.x,self.y,self.w,self.h]
        self.inc=y
        self.y+=y
        self.checky()
        return self
    def moveToY(self,y):
        self.y=y
        self.checky()
        return self

        
    def __repr__(self):
        return 'x:{} y:{} w:{} h:{} c:{}'.format(self.x,self.y,self.w,self.h,self.clr)