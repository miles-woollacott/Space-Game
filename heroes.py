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
        self.target = "First" # First, strong, and unsabotaged
        self.hover = False
        self.placed = False
        self.upgraded = [False for i in self.upgrades]
        self.super_upgrade = False
        self.sell_value = 0
        self.kills = 0
        self.can_see_infiltrators = False
    
    def update(self):
        self.position = [self.center[0]-self.width/2, self.center[1]-self.height/2]
        self.hitBox.update(self.center)

class Gunner(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Gunner.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Gunner.png")).convert_alpha()
        self.width = 30
        self.height = 26
        self.range = 140
        self.angle = 0
        self.cooldown_reset = 30
        self.id = "Gunner"
        self.cost = 85
        self.upgrades = [50, 100, 150, 250, 100] # Cost of upgrades
        self.upgrade_text = ["Range Up", "Attack Speed Up", "Projectile Speed Up", "Pierce Up", "Can Detect Infiltrators"]
        self.super_upgrade_text = "Shoots incredibly fast"
        self.super_upgrade_cost = 5000
        super().__init__(xy, move)

class Howitzer(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Howitzer.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Howitzer.png")).convert_alpha()
        self.width = 30
        self.height = 61
        self.range = 320
        self.angle = 0
        self.cooldown_reset = 80
        self.id = "Howitzer"
        self.cost = 200
        self.upgrades = [100, 100, 200, 150] # Cost of upgrades
        self.upgrade_text = ["Projectile Speed Up", "Attack Speed Up", "Projectile Size Up", "Damage Up"]
        self.super_upgrade_text = "Nothing can stop it."
        self.super_upgrade_cost = 2000
        super().__init__(xy, move)

class Saboteur(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Saboteur.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Saboteur.png")).convert_alpha()
        self.width = 28
        self.height = 61
        self.range = 80
        self.angle = 0
        self.cooldown_reset = 1
        self.id = "Saboteur"
        self.cost = 500
        self.upgrades = [500, 2000, 1000, 2000, 2000, 3000] # Cost of upgrades
        self.upgrade_text = ["Range Up", "Speed Reduction Up", "Cripple Accelerator", "Cripple Regenerator", "Cripple Spawners", "Reveal Infiltrators"]
        self.super_upgrade_text = "What is targeting mode?"
        self.super_upgrade_cost = 12000
        super().__init__(xy, move)

class Seeker(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Seeker.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Seeker.png")).convert_alpha()
        self.width = 28
        self.height = 61
        self.range = 100000
        self.angle = 0
        self.cooldown_reset = 100
        self.id = "Seeker"
        self.cost = 400
        self.upgrades = [600, 600, 700, 600] # Cost of upgrades
        self.upgrade_text = ["Projectile Speed Up", "Increase Pierce", "Attack Speed Up", "Damage Up"]
        self.super_upgrade_text = "It's not missing"
        self.super_upgrade_cost = 3000
        super().__init__(xy, move)

class Leech(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Leech.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Leech.png")).convert_alpha()
        self.width = 36
        self.height = 44
        self.range = 100
        self.angle = 0
        self.cooldown_reset = 50
        self.id = "Leech"
        self.cost = 150
        self.upgrades = [200, 200, 300, 200, 1000, 200] # Cost of upgrades
        self.upgrade_text = ["Chance to grant cash for hits", "Chance to grant lives for hits", "Chance to poison target", "Chance to crit for hits", "Increased chance success", "Awards cash for kills"]
        self.super_upgrade_text = "The root of all life"
        self.super_upgrade_cost = 5000
        super().__init__(xy, move)

class Shredder(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Shredder.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Shredder.png")).convert_alpha()
        self.width = 36
        self.height = 36
        self.range = 300
        self.angle = 0
        self.cooldown_reset = 100
        self.id = "Shredder"
        self.cost = 150
        self.upgrades = [100, 500, 300, 300, 500] # Cost of upgrades
        self.upgrade_text = ["Range Up", "Adds Two Frags", "Projectile Speed Up", "Homing Frags", "Attack Speed Up on Kills"]
        self.super_upgrade_text = "Frags on frags"
        self.super_upgrade_cost = 3000
        super().__init__(xy, move)

class Orbiter(Hero):
    def __init__(self, xy, move=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Orbiter.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Heroes", "Orbiter.png")).convert_alpha()
        self.width = 36
        self.height = 54
        self.range = 200
        self.angle = 0
        self.cooldown_reset = None
        self.id = "Orbiter"
        self.cost = 500
        self.upgrades = [1000, 800, 1000, 2000] # Cost of upgrades
        self.upgrade_text = ["Adds Another Orb", "Orb Speed Increase", "Orb Size Increase", "Slows Enemies on Contact"]
        self.super_upgrade_text = "The Wheel"
        self.super_upgrade_cost = 6000
        super().__init__(xy, move)

