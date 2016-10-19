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
    def __init__(self, color = RED, width = SNAKE_SIZE, height = SNAKE_SIZE):
        super(Snake, self).__init__()
        
        self.image = pygame.Surface((width, height))
        
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        
        self.forward = {'x':1,
                        'y':0}
        self.angle = 0
        self.turnSpeed = 0
        self.moveSpeed = 5
        
        self.tailNodes = []
        self.trailGroup = pygame.sprite.Group()
        
    # Currently ALWAYS collides with the tail because they will usually overlap
    def isColliding(self, otherGroup):
        if pygame.sprite.spritecollide(self, otherGroup, False):
            return True
        return False
        
    def setImage(self, filename = None):
        if filename != None:
            self.image = pygame.image.load(filename)
            
            self.rect = self.image.get_rect()
        
    def startMovingRight(self):
        self.turnSpeed = -10
        
    def startMovingLeft(self):
        self.turnSpeed = 10
        
    def stopMoving(self):
        self.turnSpeed = 0
        
    def move(self):
        self.angle += self.turnSpeed
        pygame.transform.rotate(self.image, self.angle)
        self.tailNodes.append(TailNode(self.rect.x, self.rect.y))
        self.trailGroup.add(self.tailNodes[len(self.tailNodes) - 1])
        self.setPos(int(round(self.rect.x + (self.forward['x'] * self.moveSpeed))), int(round(self.rect.y - (self.forward['y'] * self.moveSpeed))))
        
    def update(self):
        self.forward['x'] = math.cos(self.angle*3.1415 / 180)
        self.forward['y'] = math.sin(self.angle*3.1415 / 180)
        
        if self.angle >= 359:
            self.angle = 0
        elif self.angle <= 0:
            self.angle = 359
           
        
    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y