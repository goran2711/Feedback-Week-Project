import pygame, math
from os import path
from random import randint
from globals import *
from snake import Snake
from powerups import Powerup
from player import Player

SOURCE_FOLDER = path.dirname(path.abspath(__file__))

gameOver = False

def main():
    init()
    while True:
        gameLoop()
        gameOverScreen()

def init():
    global DISPLAYSURF, FPSCLOCK, gPlayerList

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('What am I doing')
    
    playerOne = Player()
    playerTwo = Player()
    
    gPlayerList = [playerOne, playerTwo]
    
def initGame():
    global gSnakeList, gSnakeGroup, gPowerupList, gPowerupGroup, gNextPowerupSpawn
    
    snakeOne = Snake(BLACK, GREEN)
    snakeOne.setImage(SOURCE_FOLDER + "/img/head.gif")
    snakeTwo = Snake(RED, RED)
    gSnakeGroup = pygame.sprite.Group()
    gSnakeGroup.add(snakeOne, snakeTwo)
    gSnakeList = [snakeOne, snakeTwo]
    gPowerupList = []
    gPowerupGroup = pygame.sprite.Group()
    gNextPowerupSpawn = POWERUP_TIMER
    
    for i in range(len(gPlayerList)):
        gPlayerList[i].newRoundReset()
        gPlayerList[i].assignSnake(gSnakeList[i].id)
    
    # Random spawn location
    for snake in gSnakeList:
        snake.setPos(randint(5, WIDTH - 15), randint(5, HEIGHT - 5))
        
def spawnPowerup():
    global gNextPowerupSpawn # UnboundLocalError without this. Don't know why
    
    currentTime = pygame.time.get_ticks()

    if currentTime >= gNextPowerupSpawn:
        newPowerup = Powerup()
        gPowerupList.append(newPowerup)
        gPowerupGroup.add(newPowerup)
        gNextPowerupSpawn = currentTime + randint(POWERUP_TIMER - randint(0, 3), POWERUP_TIMER + randint(0, 3))

def gameRender():
    DISPLAYSURF.fill(BGCOLOR)
    
    # Draw tails
    for snake in gSnakeGroup:
        snake.trailGroup.draw(DISPLAYSURF)
        
    # Draw heads
    gSnakeGroup.draw(DISPLAYSURF)

    # PowerupGroup is empty for collision detection
    for powerup in range(len(gPowerupList)):
        if gPowerupList[powerup].isAlive():
            gPowerupGroup.add(gPowerupList[powerup])

    gPowerupGroup.draw(DISPLAYSURF)
    
    for powerup in range(len(gPowerupList)):
         gPowerupGroup.remove(gPowerupList[powerup])
         
    drawScore()
    
def gameUpdate():
    ## INPUT ####################################################
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()

    keys = pygame.key.get_pressed()

    ## PLAYER ONE ###############################################
    if keys[pygame.K_RIGHT]:
        gSnakeList[PLAYER_ONE].startMovingRight()
    elif keys[pygame.K_LEFT]:
        gSnakeList[PLAYER_ONE].startMovingLeft()
    else:
        gSnakeList[PLAYER_ONE].stopMoving()

    ## PLAYER TWO ###############################################
    if keys[pygame.K_d]:
        gSnakeList[PLAYER_TWO].startMovingRight()
    elif keys[pygame.K_a]:
        gSnakeList[PLAYER_TWO].startMovingLeft()
    else:
        gSnakeList[PLAYER_TWO].stopMoving()
        
    ## END INPUT ################################################
                
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
                # Increment other player's score
                for player in gPlayerList:
                    if player.snake_id == otherSnake.id:
                        player.score += 1
                        player.lost()
                gSnakeGroup.add(snake)
                print (str(snake.id) + " colliding with snake " + str(otherSnake.id) + " body")
                return True
            
        # Check collision between snake and pickups
            for powerup in range(len(gPowerupList)):
                if gPowerupList[powerup].isAlive() == True:
                    gPowerupGroup.add(gPowerupList[powerup])
                    if snake.isColliding(gPowerupGroup):
                        ability = gPowerupList[powerup].getAbility()
                        snake.powerup(ability, True)        # Functions for both snakes as some pickups effect the other player
                        otherSnake.powerup(ability, False)  # Boolean variables confirm which snake has collided with the pickup and they can act accordingly
                        gPowerupList[powerup].die()
                    gPowerupGroup.remove(gPowerupList[powerup])
                
        gSnakeGroup.add(snake)
            
        # Check collision between snake and snake's own body/trail
        if len(snake.tailNodes) > 5:
            # Remove the closest nodes (Range may need to be changed if SNAKE_SIZE is altered)
            for i in range(1, 10):
                snake.trailGroup.remove(snake.tailNodes[len(snake.tailNodes) - i])
            # Check for collisions with the remaining nodes
            if snake.isColliding(snake.trailGroup):
                # Increment other player's score
                for player in gPlayerList:
                    if player.snake_id != snake.id:
                        player.score += 1
                        player.lost()
                # Add the nodes back
                for i in range(1, 10):
                        snake.trailGroup.add(snake.tailNodes[len(snake.tailNodes) - i])
                print (str(snake.id) + " colliding with self")
                return True
            # Add the nodes back
            for i in range(1, 10):
                    snake.trailGroup.add(snake.tailNodes[len(snake.tailNodes) - i])
                    
        ## END COLLISIONS ######################################
        
    # Keep track of powerup timer
    for snake in gSnakeList:
        if snake.hasPowerup == True:
            if pygame.time.get_ticks() >= snake.powerupExire:
                for snake_ in gSnakeList:
                    snake_.reset()
        
    spawnPowerup()
        
    pygame.display.update()
    FPSCLOCK.tick(FPS)
                    
    return False
    
def gameLoop():
    initGame()
    while True:
        gameOver = gameUpdate()
        gameRender()
        if gameOver:
            return
        
def waitForKeyPress():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
            else:
                return True
    return False
        
def drawPressAnyKeyToContinue():
    msgFont = pygame.font.Font('freesansbold.ttf', 30)
    msgSurf = msgFont.render('Press any key to continue', True, DARKGRAY)
    msgRect = msgSurf.get_rect()
    msgRect.midtop = (WIDTH /2, HEIGHT - (msgRect.height + 20))
    DISPLAYSURF.blit(msgSurf, msgRect)
    
def drawScore():
    scoreFont = pygame.font.Font('freesansbold.ttf', 20)
    scoreTitleSurf = scoreFont.render('Scores:', True, DARKGRAY)
    scoreTitleRect = scoreTitleSurf.get_rect()
    scoreTitleRect.topleft = (10, 10)
    DISPLAYSURF.blit(scoreTitleSurf, scoreTitleRect)
    
    scoreSurfList = []
    scoreRectList = []
    
    i = 1
    for player in gPlayerList:
        newScoreSurf = scoreFont.render('Player ' + str(player.player_id) + ': ' + str(player.score), True, DARKGRAY)
        scoreSurfList.append(newScoreSurf)
        newScoreRect = newScoreSurf.get_rect()
        newScoreRect.topleft = (10, 10 + (newScoreRect.height * i))
        scoreRectList.append(newScoreRect)
        DISPLAYSURF.blit(newScoreSurf, newScoreRect)
        i += 1
    
def drawPlayerXLoses(player):
    msgFont = pygame.font.Font('freesansbold.ttf', 30)
    msg = "Player " + str(player.player_id) + " loses!"
    msgSurf = msgFont.render(msg, True, DARKGRAY)
    msgRect = msgSurf.get_rect()
    msgRect.midtop = (WIDTH/2, msgRect.height + 20)
    DISPLAYSURF.blit(msgSurf, msgRect)
         
def gameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    
    gameSurf = gameOverFont.render('Game', True, DARKGRAY)
    overSurf = gameOverFont.render('Over', True, DARKGRAY)
  
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
   
    gameRect.midtop = (WIDTH / 2, (HEIGHT / 2) - gameRect.height)
    overRect.midtop = (WIDTH / 2, gameRect.midbottom[1] + 20)
    
    for player in gPlayerList:
        if player.isLoser == True:
            drawPlayerXLoses(player)
    
    drawPressAnyKeyToContinue()
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    
    # Debug
    print("P1 score: " + str(gPlayerList[PLAYER_ONE].score))
    print("P2 score: " + str(gPlayerList[PLAYER_TWO].score))

    pygame.display.update()
    pygame.time.wait(500)
    
    # pygame.event.get()  #clear out event queue 
    while True:
        if waitForKeyPress():
            return
        
        # Limit loops per second
        FPSCLOCK.tick(FPS)
        
def quitGame():
    pygame.quit()
    quit()
    
# Program starts here
if __name__ == '__main__':
    main()
