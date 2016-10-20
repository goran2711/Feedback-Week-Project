import pygame
from math import cos, sin, pi
from random import randint
from globals import *

GAP_TIME = 500 # Time in milliseconds

IMG_TAIL = [SOURCE_FOLDER + "/img/tail1.png", SOURCE_FOLDER + "/img/tail2.png"]
IMG_BODY = [(SOURCE_FOLDER + "/img/body1_1.png", SOURCE_FOLDER + "/img/body1_2.png"),
            (SOURCE_FOLDER + "/img/body2_1.png", SOURCE_FOLDER + "/img/body2_2.png")]

class TailNode(pygame.sprite.Sprite):
    def __init__(self, x, y, image = None, angle = None, width = SNAKE_SIZE, height = SNAKE_SIZE):
        super(TailNode, self).__init__()
        if image == None:
            self.image = pygame.Surface((width, height))
            self.image.fill(BLACK)
        else:
            self.imageMaster = pygame.image.load(image)
            self.image = pygame.transform.scale(self.imageMaster, (width, height))
            if angle != None:
                self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Snake(pygame.sprite.Sprite):
    # Class variable. Kind of like static variables in C++
    snake_id = 0

    def __init__(self, owner_id, color = RED, tailColor = RED, width = SNAKE_SIZE, height = SNAKE_SIZE):
        super(Snake, self).__init__()
        
        self.owner_id = owner_id
        
        self.id = Snake.snake_id
        Snake.snake_id += 1
        
        self.imageMaster = None
        self.image = pygame.Surface((width, height))
        
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        
        self.forward = {'x':1,
                        'y':0}
        self.angle = 0
        self.turnSpeed = DEFAULT_TURNSPEED
        self.moveSpeed = DEFAULT_MOVESPEED
        
        self.tailColor = tailColor
        self.tailNodes = []
        self.trailGroup = pygame.sprite.Group()

        self.layingTrail = True
        self.hasPowerup = False
        self.powerupExpire = 0
        self.currentPowerupAbility = None
        
        self.nextGapTime = 0
        self.currentTrailIndex = 0  # Determines which body sprite to use
        
    # Currently ALWAYS collides with the tail because they will usually overlap
    def isColliding(self, otherGroup):
        if pygame.sprite.spritecollide(self, otherGroup, False):
            return True
        return False
        
    def setImage(self, filename = None):
        if filename != None:
            self.imageMaster = pygame.image.load(filename)
            self.image = self.imageMaster
            self.image = pygame.transform.scale(self.image, (SNAKE_SIZE, SNAKE_SIZE))
            
            self.rect = self.image.get_rect()
        
    def startMovingRight(self):
        self.turnSpeed = -DEFAULT_TURNSPEED
        
    def startMovingLeft(self):
        self.turnSpeed = DEFAULT_TURNSPEED
        
    def stopTurning(self):
        self.turnSpeed = 0
        
    def move(self):
        self.angle += self.turnSpeed
        print(str(self.snake_id))
        if self.imageMaster != None:
            oldCenter = self.rect.center
            self.image = pygame.transform.rotate(self.imageMaster, self.angle) #Figure out a way to rotate the head to self.forward's direction
            self.image = pygame.transform.scale(self.image, (SNAKE_SIZE, SNAKE_SIZE))
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter
        
        if self.layingTrail == True:
            if self.currentTrailIndex == 0:
                self.tailNodes.append(TailNode(self.rect.x, self.rect.y, IMG_TAIL[self.owner_id], self.angle))
            else:
                self.tailNodes.append(TailNode(self.rect.x, self.rect.y, IMG_BODY[self.owner_id][self.currentTrailIndex % 2], self.angle))
            self.trailGroup.add(self.tailNodes[len(self.tailNodes) - 1])
            self.currentTrailIndex += 1
        self.setPos(int(round(self.rect.x + (self.forward['x'] * self.moveSpeed))), int(round(self.rect.y - (self.forward['y'] * self.moveSpeed))))
        
    def update(self):
        self.forward['x'] = cos(self.angle * pi / 180)
        self.forward['y'] = sin(self.angle * pi / 180)
        
        if self.angle >= 359:
            self.angle = 0
        elif self.angle <= 0:
            self.angle = 359
            
        currentTime = pygame.time.get_ticks()
        
        if self.currentPowerupAbility != "NOTRAIL":
            if self.layingTrail == True:
                if currentTime >= self.nextGapTime:
                    self.layingTrail = False
                    self.currentTrailIndex = 0
                    self.gapTimeExpire = currentTime + GAP_TIME
            else:
                if currentTime >= self.gapTimeExpire:
                    self.layingTrail = True
                    self.nextGapTime = currentTime + randint(1500, 3000) # Random hardcoded numbers (time in ms)
           
    def powerup(self, ability, collided):
        self.currentPowerupAbility = ability
        if collided == True:
            self.hasPowerup = True
            self.powerupExire = pygame.time.get_ticks() + POWERUPLIFESPAN
            if ability == "SPEED+":
                self.moveSpeed = DEFAULT_MOVESPEED * 1.5
        else:
            if ability == "SPEED-":
                self.moveSpeed = DEFAULT_MOVESPEED * 0.5
            elif ability == "NOTRAIL":
                self.layingTrail = False

    def reset(self):
        self.moveSpeed = DEFAULT_MOVESPEED
        self.layingTrail = True
        self.hasPowerup = False
        self.currentPowerupAbility = None
        
    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y
