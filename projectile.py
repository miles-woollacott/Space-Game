import pygame
import os

from pygame.locals import *
from hitBox import HitBox

class Projectile:
    def __init__(self, xy, angle):
        super(Projectile, self).__init__()
        self.angle = angle
        self.lifespan = 0
        self.center = xy
        self.position = [xy[0]-self.width/2, xy[1]-self.height/2]
        self.hitBox = HitBox(self.center, self.width, self.height)
        self.damage = 1

    def update(self):
        self.position = [self.center[0]-self.width/2, self.center[1]-self.height/2]
        self.hitBox.update(self.center)

class Bullet(Projectile):
    def __init__(self, xy, angle):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Bullet_basic.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Bullet_basic.png")).convert_alpha()
        self.width = 10
        self.height = 17
        self.pierce = 1
        self.speed = 18
        self.lifespan_reset = 300
        self.id = "Bullet"
        super().__init__(xy, angle)

class Blast(Projectile):
    def __init__(self, xy, angle):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Blast.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Blast.png")).convert_alpha()
        self.width = 10
        self.height = 18
        self.pierce = 18
        self.speed = 4
        self.lifespan_reset = 600
        self.id = "Blast"
        super().__init__(xy, angle)

class Missile(Projectile):
    def __init__(self, xy, angle):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Missile.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Missile.png")).convert_alpha()
        self.width = 16
        self.height = 32
        self.pierce = 1
        self.speed = 10
        self.lifespan_reset = 100000
        self.id = "Missile"
        self.target = "First"
        self.accelerate = False
        super().__init__(xy, angle)

class Meteor(Projectile):
    def __init__(self, xy, angle):
            self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Meteor.png")).convert_alpha()
            self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Meteor.png")).convert_alpha()
            self.width = 23
            self.height = 27
            self.pierce = 0
            self.speed = 3
            self.lifespan_reset = 0
            self.id = "Meteor"
            super().__init__(xy, angle)

class Shrapnel(Projectile):
    def __init__(self, xy, angle):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Shrapnel.png")).convert_alpha()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Bullet", "Shrapnel.png")).convert_alpha()
        self.width = 8
        self.height = 12
        self.pierce = 1
        self.speed = 20
        self.lifespan_reset = 300
        self.id = "Shrapnel"
        self.damage = 0.5
        super().__init__(xy, angle)