import pygame, math
from os import path
from random import randint
from globals import *
from snake import Snake

SOURCE_FOLDER = path.dirname(path.abspath(__file__))

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
    snakeTwo = Snake(RED)
    gSnakeGroup = pygame.sprite.Group()
    gSnakeGroup.add(snakeOne, snakeTwo)
    gSnakeList = [snakeOne, snakeTwo]
    
    # Random spawn location
    for snake in gSnakeList:
        snake.setPos(randint(5, WIDTH - 15), randint(5, HEIGHT - 5))
    
def gameRender():
    DISPLAYSURF.fill(BGCOLOR)
    
    # Draw tails
    for snake in gSnakeGroup:
        snake.trailGroup.draw(DISPLAYSURF)
        
    # Draw heads
    gSnakeGroup.draw(DISPLAYSURF)
    
def gameUpdate():
    ## INPUT ####################################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        
            ## PLAYER ONE ######################
            if event.key == pygame.K_LEFT:
                gSnakeList[PLAYER_ONE].startMovingLeft()
            elif event.key == pygame.K_RIGHT:
                gSnakeList[PLAYER_ONE].startMovingRight()
                
            ## PLAYER TWO ######################
            if event.key == pygame.K_a:
                gSnakeList[PLAYER_TWO].startMovingLeft()
            if event.key == pygame.K_d:
                gSnakeList[PLAYER_TWO].startMovingRight()
                
        if event.type == pygame.KEYUP:
            ## PLAYER ONE ######################
            if event.key == pygame.K_LEFT:
                # If they are still pressing right arrow when letting go of left arrow
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    gSnakeList[PLAYER_ONE].startMovingRight()
                else:
                    gSnakeList[PLAYER_ONE].stopMoving()
                    
            if event.key == pygame.K_RIGHT:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    gSnakeList[PLAYER_ONE].startMovingLeft()
                else:
                    gSnakeList[PLAYER_ONE].stopMoving()
                    
            ## PLAYER TWO ######################
            if event.key == pygame.K_a:
                if pygame.key.get_pressed()[pygame.K_d]:
                    gSnakeList[PLAYER_TWO].startMovingRight()
                else:
                    gSnakeList[PLAYER_TWO].stopMoving()
                    
            if event.key == pygame.K_d:
                if pygame.key.get_pressed()[pygame.K_a]:
                    gSnakeList[PLAYER_TWO].startMovingLeft()
                else:
                    gSnakeList[PLAYER_TWO].stopMoving()
    ## END INPUT ########################################################
                
                
    for snake in gSnakeGroup:
        snake.update()
        snake.move()
        
        # Check if out of bounds
        if snake.rect.x >= WIDTH:
            snake.rect.x = 1
        if snake.rect.x <= 0:
            snake.rect.x = WIDTH - 1
        if snake.rect.y >= HEIGHT:
            snake.rect.y = 1
        if snake.rect.y <= 0:
            snake.rect.y = HEIGHT - 1
            
        ## COLLISIONS #########################################
            
        # Check collision between snake and other snake bodies/trails
        gSnakeGroup.remove(snake)
        for otherSnake in gSnakeGroup:
            if snake.isColliding(otherSnake.trailGroup):
                gSnakeGroup.add(snake)
                print (str(snake.id) + " colliding with snake " + str(otherSnake.id) + " body")
                return True
        gSnakeGroup.add(snake)
            
        # Check collision between snake and snake's own body/trail
        if len(snake.tailNodes) > 1:
            # Remove the closest nodes
            for i in range(1, 5):
                snake.trailGroup.remove(snake.tailNodes[len(snake.tailNodes) - i])
            # Check for collisions with the remaining nodes
            if snake.isColliding(snake.trailGroup):
                # Add the nodes back
                for i in range(1, 5):
                        snake.trailGroup.add(snake.tailNodes[len(snake.tailNodes) - i])
                print (str(snake.id) + " colliding with self")
                return True
            # Add the nodes back
            for i in range(1, 5):
                    snake.trailGroup.add(snake.tailNodes[len(snake.tailNodes) - i])
                    
        ## END COLLISIONS ######################################
        
        
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