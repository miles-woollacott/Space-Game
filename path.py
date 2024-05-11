import pygame
import os

from pygame.locals import *
from functions import angle, distance

class Path:
    def __init__(self, points):
        super(Path, self).__init__()
        self.points = points

        self.angles = [i for i in range(len(self.points)-1)]
        for i in range(len(points)-1):
            self.angles[i] = angle(self.points[i], self.points[i+1])
            if self.angles[i]<0:
                self.angles[i] += 360


        self.start = points[0]
        self.end = points[-1]

    def get_start(self):
        return [self.start[0], self.start[1]]
    def get_end(self):
        return [self.end[0], self.end[1]]
    def get_index(self, i):
        return [self.points[i][0], self.points[i][1]]
    def set_position(self):
        self.start = self.points[0]
        self.end = self.points[-1]