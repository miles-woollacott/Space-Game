import pygame

from pygame.locals import *

class textBox:
    def __init__(self, left, top, width, height, text="", color=None):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text
        self.sfont = pygame.font.Font('freesansbold.ttf', 24)
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.color = color
    
    def get_text(self):
        return self.sfont.render(self.text, False, self.color)
    
    def isClicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())