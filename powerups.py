import pygame
from random import randint
from globals import *

PWIDTH = 10
PHEIGHT = 10

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super(Powerup, self).__init__()
        self.alive = True
        self.generate()

    def generate(self):
        rand = randint(0, 2)
        if rand == 0:
            self.ability = "SPEED+"
            self.color = GREEN
        elif rand == 1:
            self.ability = "SPEED-"
            self.color = RED
        elif rand == 2:
            self.ability = "NOTRAIL"
            self.color = DARKGRAY

        self.image = pygame.Surface([PWIDTH, PHEIGHT])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, WIDTH)
        self.rect.y = randint(0, HEIGHT)

    def getAbility(self):
        return self.ability

    def isAlive(self):
        if self.alive == True:
            return True
        else:
            return False
        
    def die(self):
        self.alive = False

