from pygame.locals import *

class User:
    def __init__(self, money=1000, lives=100, round=0, difficulty="Medium"):
        self.money = money
        self.lives = lives
        self.round = round
        self.max_ticks = 1000
        self.leveltick = 0
        self.difficulty = difficulty