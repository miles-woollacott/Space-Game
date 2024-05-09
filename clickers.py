import pygame
import os

from pygame.locals import *
from hitBox import HitBox
from heroes import *

class Clicker:
    def __init__(self, xy):
        super(Clicker, self).__init__()
        self.center = xy
        self.hitBox = HitBox(self.center, self.width, self.height)
        self.position = [self.center[0]-self.width/2, self.center[1]-self.height/2]
        

class GunnerClicker(Clicker):
    def __init__(self, xy):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Gunner.png")).convert()
        self.width = 30
        self.height = 26
        self.cost = Gunner([0, 0]).cost
        self.id = "Gunner"
        self.text = "A basic attack tower. Cheap, and can fire fast."
        super().__init__(xy)

class HowitzerClicker(Clicker):
    def __init__(self, xy):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Howitzer.png")).convert()
        self.width = 30
        self.height = 61
        self.cost = Howitzer([0, 0]).cost
        self.id = "Howitzer"
        self.text = "Slow, but projectiles have massive pierce."
        super().__init__(xy)
        

class TrashClicker(Clicker):
    def __init__(self, xy):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Clickers", "trash-can.png")).convert()
        self.width = 20
        self.height = 27
        self.clicked = False
        self.id = "Trash"
        self.text = "Click, then click on tower to sell for partial value."
        super().__init__(xy)

class SaboteurClicker(Clicker):
    def __init__(self, xy):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Saboteur.png")).convert()
        self.width = 28
        self.height = 61
        self.cost = Saboteur([0, 0]).cost
        self.id = "Saboteur"
        self.text = "Sabotages enemies in various ways."
        super().__init__(xy)
        
