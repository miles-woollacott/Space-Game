import pygame
import os

from pygame.locals import *
from hitBox import HitBox

class Hero:
    def __init__(self, xy, move):
        super(Hero, self).__init__()
        self.position = xy
        self.center = [xy[0]+self.width/2, xy[1]+self.height/2]
        self.hitBox = HitBox(self.center, self.width, self.height)
        self.cooldown = 0
        self.move = move
        self.target = "First" # First and strong
        self.hover = False
        self.placed = False
        self.upgraded = [False for i in self.upgrades]
        self.super_upgrade = False
        self.sell_value = 0
    
    def update(self):
        self.position = [self.center[0]-self.width/2, self.center[1]-self.height/2]
        self.hitBox.update(self.center)

class Gunner(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Gunner.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Gunner.png")).convert()
        self.width = 30
        self.height = 26
        self.range = 140
        self.angle = 0
        self.cooldown_reset = 30
        self.id = "Gunner"
        self.cost = 85
        self.upgrades = [50, 100, 150, 250] # Cost of upgrades
        self.upgrade_text = ["Range Up", "Attack Speed Up", "Projectile Speed Up", "Pierce Up"]
        self.super_upgrade_text = "Shoots incredibly fast"
        self.super_upgrade_cost = 5000
        super().__init__(xy, move)

class Howitzer(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Howitzer.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Howitzer.png")).convert()
        self.width = 30
        self.height = 61
        self.range = 320
        self.angle = 0
        self.cooldown_reset = 80
        self.id = "Howitzer"
        self.cost = 200
        self.upgrades = [100, 100, 200] # Cost of upgrades
        self.upgrade_text = ["Projectile Speed Up", "Attack Speed Up", "Projectile Size Up"]
        self.super_upgrade_text = "Nothing can stop it."
        self.super_upgrade_cost = 2000
        super().__init__(xy, move)

class Saboteur(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Saboteur.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Saboteur.png")).convert()
        self.width = 28
        self.height = 61
        self.range = 80
        self.angle = 0
        self.cooldown_reset = 1
        self.id = "Saboteur"
        self.cost = 500
        self.upgrades = [500, 2000, 1000, 2000, 2000] # Cost of upgrades
        self.upgrade_text = ["Increase Range", "Increase Speed Reduction", "Cripple Accelerator", "Cripple Regenerator", "Cripple Spawners"]
        self.super_upgrade_text = "What is targeting mode?"
        self.super_upgrade_cost = 12000
        super().__init__(xy, move)

