from pygame.locals import *

class User:
    def __init__(self, money=1000, lives=100, round=0, difficulty="Medium"):
        self.money = money
        self.lives = lives
        self.round = round
        self.difficulty = difficulty
        if self.difficulty == "Easy":
            self.max_ticks = 1000
        elif self.difficulty == "Medium":
            self.max_ticks = 800
        else:
            self.max_ticks = 550
        self.leveltick = 0