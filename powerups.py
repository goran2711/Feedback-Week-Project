import pygame
from random import randint
from globals import *

PWIDTH = 40
PHEIGHT = 40

POWERUP_NOTRAIL = SOURCE_FOLDER + "/img/powerup_notrail.png"
POWERUP_SPEEDUP = SOURCE_FOLDER + "/img/powerup_speedup.png"
POWERUP_SLOWDOWN = SOURCE_FOLDER + "/img/powerup_slowdown.png"

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super(Powerup, self).__init__()
        self.alive = True
        self.generate()

    def generate(self):
        rand = randint(0, 2)
        if rand == 0:
            self.ability = "SPEED+"
            self.sprite = POWERUP_SPEEDUP
        elif rand == 1:
            self.ability = "SPEED-"
            self.sprite = POWERUP_SLOWDOWN
        elif rand == 2:
            self.ability = "NOTRAIL"
            self.sprite = POWERUP_NOTRAIL

        self.image = pygame.image.load(self.sprite)
        self.image = pygame.transform.scale(self.image, (PWIDTH, PHEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, WIDTH - PWIDTH / 2)
        self.rect.y = randint(0, HEIGHT - PHEIGHT / 2)

    def getAbility(self):
        return self.ability

    def isAlive(self):
        if self.alive == True:
            return True
        else:
            return False
        
    def die(self):
        self.alive = False

