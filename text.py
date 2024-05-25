import pygame as pyg

class Text:
    def __init__(self,content,color):
        self.content=content
        self.text=pyg.font.Font("freesansbold.ttf",38).render(self.content,True,color)