import pygame, math
from globals import *

class TailNode(pygame.sprite.Sprite):
    def __init__(self, x, y, color = BLACK, width = SNAKE_SIZE, height = SNAKE_SIZE):
        super(TailNode, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Snake(pygame.sprite.Sprite):
    # Class variable. Kind of like static variables in C++
    snake_id = 0

    def __init__(self, color = RED, tailColor = RED, width = SNAKE_SIZE, height = SNAKE_SIZE):
        super(Snake, self).__init__()
        
        self.id = Snake.snake_id
        Snake.snake_id += 1
        
        self.image = pygame.Surface((width, height))
        
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        
        self.forward = {'x':1,
                        'y':0}
        self.angle = 0
        self.turnSpeed = 0
        self.moveSpeed = 5
        
        self.tailColor = tailColor
        self.tailNodes = []
        self.trailGroup = pygame.sprite.Group()

        self.layingTrail = True
        self.hasPowerup = False
        self.powerupExpire = 0
        
    # Currently ALWAYS collides with the tail because they will usually overlap
    def isColliding(self, otherGroup):
        if pygame.sprite.spritecollide(self, otherGroup, False):
            return True
        return False
        
    def setImage(self, filename = None):
        if filename != None:
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, (SNAKE_SIZE, SNAKE_SIZE))
            
            self.rect = self.image.get_rect()
        
    def startMovingRight(self):
        self.turnSpeed = -10
        
    def startMovingLeft(self):
        self.turnSpeed = 10
        
    def stopMoving(self):
        self.turnSpeed = 0
        
    def move(self):
        self.angle += self.turnSpeed
        # self.image = pygame.transform.rotate(self.image, self.angle) #Figure out a way to rotate the head to self.forward's direction
        if self.layingTrail == True:
            self.tailNodes.append(TailNode(self.rect.x, self.rect.y, self.tailColor))
            self.trailGroup.add(self.tailNodes[len(self.tailNodes) - 1])
        self.setPos(int(round(self.rect.x + (self.forward['x'] * self.moveSpeed))), int(round(self.rect.y - (self.forward['y'] * self.moveSpeed))))
        
    def update(self):
        self.forward['x'] = math.cos(self.angle*3.1415 / 180)
        self.forward['y'] = math.sin(self.angle*3.1415 / 180)
        
        if self.angle >= 359:
            self.angle = 0
        elif self.angle <= 0:
            self.angle = 359
           
    def powerup(self, ability, collided):
        if collided == True:
            self.hasPowerup = True
            self.powerupExire = pygame.time.get_ticks() + POWERUPLIFESPAN
            if ability == "SPEED+":
                self.moveSpeed = 8
        else:
            if ability == "SPEED-":
                self.moveSpeed = 3
            elif ability == "NOTRAIL":
                self.layingTrail = False

    def reset(self):
        self.moveSpeed = 5
        self.layingTrail = True
        self.hasPowerup = False
        
    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y
