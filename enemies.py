import pygame
import os

from pygame.locals import *
from hitBox import HitBox

class Enemy:
    def __init__(self, xy, distance=0, shielded=False):
        super(Enemy, self).__init__()
        self.center = xy
        self.position = [xy[0]-self.width/2, xy[1]-self.height/2]
        self.hitBox = HitBox(self.center, self.width, self.height)
        self.distance = distance
        self.shielded = shielded
        self.sabotaged = False
        self.repaired = False

    def update(self):
        self.position = [self.center[0]-self.width/2, self.center[1]-self.height/2]
        self.hitBox.update(self.center)

class Speeder(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Speeder.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Speeder.png")).convert()
        self.width = 24
        self.height = 22
        self.index = index
        self.angle = 0
        self.speed = 8
        self.lives = 3
        self.id = "Speeder"
        self.priority = 1
        self.reward = 10
        super().__init__(xy, distance=distance, shielded=shielded)

class Spawner(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Spawner.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Spawner.png")).convert()
        self.width = 72
        self.height = 88
        self.index = index
        self.angle = 0
        self.speed = 2
        self.lives = 20
        self.countdown = 0
        self.countdown_reset = 60
        self.id = "Spawner"
        self.priority = 3
        self.reward = 20
        super().__init__(xy, distance=distance, shielded=shielded)

class Accelerator(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Accelerator.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Accelerator.png")).convert()
        self.width = 22
        self.height = 22
        self.index = index
        self.angle = 0
        self.speed = 4
        self.lives = 2
        self.id = "Accelerator"
        self.priority = 1
        self.reward = 15
        super().__init__(xy, distance=distance, shielded=shielded)

class Tanker(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Tanker.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Tanker.png")).convert()
        self.width = 30
        self.height = 27
        self.index = index
        self.angle = 0
        self.speed = 6
        self.lives = 10
        self.id = "Tanker"
        self.priority = 2
        self.reward = 20
        super().__init__(xy, distance=distance, shielded=shielded)

class Dreadnought(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Dreadnought.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Dreadnought.png")).convert()
        self.width = 72
        self.height = 88
        self.index = index
        self.angle = 0
        self.speed = 1
        self.lives = 100
        self.countdown = 0
        self.countdown_reset = 100
        self.id = "Dreadnought"
        self.priority = 4
        self.reward = 100
        super().__init__(xy, distance=distance, shielded=shielded)

class Regenerator(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Regenerator.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Regenerator.png")).convert()
        self.width = 22
        self.height = 24
        self.index = index
        self.angle = 0
        self.speed = 6
        self.lives = 15
        self.countdown = 0
        self.countdown_reset = 30
        self.id = "Regenerator"
        self.priority = 1
        self.reward = 150
        super().__init__(xy, distance=distance, shielded=shielded)

class Destroyer(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Destroyer.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Destroyer.png")).convert()
        self.width = 56
        self.height = 22
        self.index = index
        self.angle = 0
        self.speed = 16
        self.lives = 5
        self.id = "Destroyer"
        self.priority = 2
        self.reward = 30
        super().__init__(xy, distance=distance, shielded=shielded)

class Repairer(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Repairer.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Repairer.png")).convert()
        self.width = 28
        self.height = 28
        self.index = index
        self.angle = 0
        self.speed = 8
        self.lives = 20
        self.id = "Repairer"
        self.priority = 2
        self.reward = 100
        super().__init__(xy, distance=distance, shielded=shielded)

class Warper(Enemy):
    def __init__(self, xy, index=0, distance=0, shielded=False):
        self.imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Warper.png")).convert()
        self.a_imp = pygame.image.load(os.path.join(os.getcwd(), "Sprites", "Enemies", "Warper.png")).convert()
        self.width = 36
        self.height = 39
        self.index = index
        self.angle = 0
        self.speed = 8
        self.lives = 20
        self.id = "Warper"
        self.priority = 2
        self.reward = 100
        super().__init__(xy, distance=distance, shielded=shielded)

    