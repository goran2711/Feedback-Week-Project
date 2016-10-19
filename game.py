import pygame, math, os
from globals import *
from snake import Snake

SOURCE_FOLDER = os.path.dirname(os.path.abspath(__file__))

gameOver = False

def main():
    init()
    gameLoop()

def init():
    global DISPLAYSURF, FPSCLOCK

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('What am I doing')
    
def initGame():
    global gSnakeList, gSnakeGroup
    snakeOne = Snake(BLACK)
    snakeOne.setImage(SOURCE_FOLDER + "/img/head.gif")
    gSnakeGroup = pygame.sprite.Group()
    gSnakeGroup.add(snakeOne)
    gSnakeList = [snakeOne]
    
def gameRender():
    DISPLAYSURF.fill(BGCOLOR)
    for snake in gSnakeGroup:
        snake.trailGroup.draw(DISPLAYSURF)
    gSnakeGroup.draw(DISPLAYSURF)
    
def gameUpdate():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gSnakeList[PLAYER_ONE].startMovingLeft()
            elif event.key == pygame.K_RIGHT:
                gSnakeList[PLAYER_ONE].startMovingRight()
                
            # if event.key == pygame.K_a:
                # snakeTwo.startMovingLeft()
            # if event.key == pygame.K_d:
                # snakeTwo.startMovingRight()
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                gSnakeList[PLAYER_ONE].stopMoving()
            if event.key == pygame.K_RIGHT:
                gSnakeList[PLAYER_ONE].stopMoving()
            # if event.key == pygame.K_a:
                # snakeTwo.stopMoving()
            # if event.key == pygame.K_d:
                # snakeTwo.stopMoving()
                
                
    for snake in gSnakeGroup:
        snake.update()
        snake.move()
        
        
    pygame.display.update()
        
    FPSCLOCK.tick(FPS)
    return False
    
def gameLoop():
    initGame()
    while True:
        gameOver = gameUpdate()
        gameRender()
        if gameOver:
            break
    quitGame()
        
def quitGame():
    pygame.quit()
    quit()
    
# Program starts here
if __name__ == '__main__':
    main()