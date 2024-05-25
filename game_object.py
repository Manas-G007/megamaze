import pygame as pyg

class GameObject:
    def __init__(self,imgPath,x,y,speed,speedConst):
        self.image=pyg.image.load(imgPath)
        self.x=x
        self.y=y
        self.speedX=speed
        self.speedY=speed
        self.speed=speedConst

    def changeX(self,x):
        self.x=x
    
    def changeY(self,y):
        self.y=y

    def changeSpeedX(self,speed):
        self.speedX=speed
    
    def changeSpeedY(self,speed):
        self.speedY=speed