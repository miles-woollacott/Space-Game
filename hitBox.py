import pygame
import os

from pygame.locals import *
from functions import distance

class HitBox:
    def __init__(self, xy, width, height):
        super(HitBox, self).__init__()
        self.center = xy
        self.radius = max(width, height)/2

    def isClicked(self, mouseloc):
        return distance(self.center, mouseloc) < self.radius
    
    def intersects(self, circ):
        return distance(self.center, circ.center) < self.radius + circ.radius
    
    def update(self, xy):
        self.center = xy
