#########################################
# Programmer: Omri
# Date: June 5th 2018
# File Name: mr_gun_classes.py
# Description: These classes are for a mr.gun game.
#########################################
import pygame
from math import sin,cos,pi

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                  
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255) 
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  MAGENTA,  YELLOW, CYAN, WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']

class Block(object):
    """ A square - basic building block
        data:               behaviour:
            x                 draw
            y                  move left/right
            clr - colour
            h-height
            w-width
    """

    def __init__(self, x, y, clr,w,h):
        self.x = x                  
        self.y = y                  
        self.clr = clr
        self.h=h
        self.w=w
        
    def __str__(self):                  
        return '('+str(self.x)+','+str(self.y)+') '+CLR_names[self.clr]

    def draw(self, surface):                     
        CLR = COLOURS[self.clr]            
        pygame.draw.rect(surface,CLR,(self.x,self.y,self.w-20,self.h+40), 0)#w+10, h+5
        CLR = COLOURS[8]            
        pygame.draw.rect(surface,CLR,(self.x-10,self.y-70,self.w,self.h), 0)#h+25

    def moveR1(self):
        if self.x<=400:
            self.x += 10
        else:
            return True

    def moveR2(self):
        if 300<=self.x<=690:
            self.x += 10
            
    def moveL1(self):
        if self.x>=300:
            self.x -= 10
        else:
            return True

    def moveL2(self):
        if 50<=self.x<=720:
            self.x -= 10
            
    
class Bullet(object):
    """ A bullet 
        data:               behaviour:
            x                 draw
            y                  move 
            clr - colour   collision with block
            h-height
            w-width
    """
    def __init__(self,x,y,clr,w,h,angle=0):
        self.angle=angle
        self.x = x
        self.y = y
        self.clr=clr
        self.w=w
        self.h=h

    def move_bul(self,side,VELOCITY,objectAngle):
        if side==-1:
            self.x += int(round(VELOCITY*cos(objectAngle*pi/180)))
        elif side==1:
            self.x -= int(round(VELOCITY*cos(objectAngle*pi/180)))
        self.y += int(round(VELOCITY*sin(objectAngle*pi/180)))

    def draw(self,surface):
        CLR=COLOURS[self.clr]
        pygame.draw.rect(surface,CLR,(self.x,self.y,self.w,self.h),0)

    def collidesBod(self, other):
        for i in ((0, 40),(-20, -70)):
            if (other.x+i[0]+other.w>=self.x>=other.x+i[0] and other.y+i[1]+other.h>=self.y>=other.y+i[1]):
                return i
 
            elif (other.x+i[0]+other.w>=self.x+self.w>=other.x+i[0] and other.y+i[1]+other.h>=self.y>=other.y+i[1]):
                return i
        
            elif (other.x+i[0]+other.w>=self.x>=other.x+i[0] and other.y+i[1]+other.h>=self.y+self.h>=other.y+i[1]):
                return i
 
            elif (other.x+i[0]+other.w>=self.x+self.w>=other.x+i[0] and other.y+i[1]+other.h>=self.y+self.h>=other.y+i[1]):
                return i
        return False
