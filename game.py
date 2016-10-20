import pygame
from random import randint
from globals import *
from snake import Snake
from powerups import Powerup
from player import Player

gameOver = False

IMG_BG = SOURCE_FOLDER + "/img/bg.jpg"
IMG_LOGO = SOURCE_FOLDER + "/img/logo.png"

def main():
    init()
    startScreen()
    while True:
        gameLoop()
        gameOverScreen()

def init():
    global DISPLAYSURF, FPSCLOCK, gPlayerList, gBgImg, gBgRect

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(SOURCE_FOLDER + "/sfx/pickup.mp3")
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Slithery Snake')
    
    gPlayerList = [Player(), Player()]
    
    gBgImg = pygame.image.load(IMG_BG)
    gBgImg = pygame.transform.scale(gBgImg, (WIDTH, HEIGHT))
    gBgRect = gBgImg.get_rect()
    
def initGame():
    global gSnakeList, gSnakeGroup, gPowerupList, gPowerupGroup, gPowerupRenderGroup, gNextPowerupSpawn
    
    # Snakes
    snakeOne = Snake(PLAYER_ONE)
    snakeTwo = Snake(PLAYER_TWO)
    gSnakeGroup = pygame.sprite.Group()
    gSnakeGroup.add(snakeOne, snakeTwo)
    gSnakeList = [snakeOne, snakeTwo]
    
    # Powerups
    gPowerupList = []
    gPowerupGroup = pygame.sprite.Group()
    gPowerupRenderGroup = pygame.sprite.Group()
    gNextPowerupSpawn = pygame.time.get_ticks() + POWERUP_TIMER
    
    # Player assignment
    for i in range(len(gPlayerList)):
        gPlayerList[i].newRoundReset()
        gPlayerList[i].assignSnake(gSnakeList[i].id)
    
    # Random spawn location
    for snake in gSnakeList:
        snake.setPos(randint(SNAKE_SIZE, WIDTH - SNAKE_SIZE), randint(SNAKE_SIZE, HEIGHT - SNAKE_SIZE))
        
        
def spawnPowerup():
    global gNextPowerupSpawn # UnboundLocalError without this. Don't know why
    
    currentTime = pygame.time.get_ticks()

    if currentTime >= gNextPowerupSpawn:
        newPowerup = Powerup()
        gPowerupList.append(newPowerup)
        gPowerupRenderGroup.add(newPowerup)
        gNextPowerupSpawn = currentTime + randint(POWERUP_TIMER - randint(0, 3), POWERUP_TIMER + randint(0, 3))

def gameRender():
    DISPLAYSURF.blit(gBgImg, gBgRect)
    
    # Draw tails
    for snake in gSnakeGroup:
        snake.trailGroup.draw(DISPLAYSURF)
        
    # Draw heads
    gSnakeGroup.draw(DISPLAYSURF)

    # Draw powerups
    gPowerupRenderGroup.draw(DISPLAYSURF)

    # Draw score
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
        gSnakeList[PLAYER_ONE].stopTurning()

    ## PLAYER TWO ###############################################
    if keys[pygame.K_d]:
        gSnakeList[PLAYER_TWO].startMovingRight()
    elif keys[pygame.K_a]:
        gSnakeList[PLAYER_TWO].startMovingLeft()
    else:
        gSnakeList[PLAYER_TWO].stopTurning()
        
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
                        player.won()
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
                        gPowerupRenderGroup.remove(gPowerupList[powerup])
                        pygame.mixer.music.play()
                    gPowerupGroup.remove(gPowerupList[powerup])
                
        gSnakeGroup.add(snake)
            
        # Check collision between snake and snake's own body/trail
        if len(snake.tailNodes) > 5:
            # Has to be dynamic so that snake doesn't collide with itself when slowed by powerup
            nodesToRemove = int(10 + (15/snake.moveSpeed))
            
            # Remove the closest nodes (Range may need to be changed if SNAKE_SIZE is altered)
            for i in range(1, nodesToRemove):
                snake.trailGroup.remove(snake.tailNodes[len(snake.tailNodes) - i])
            # Check for collisions with the remaining nodes
            if snake.isColliding(snake.trailGroup):
                # Increment other player's score
                for player in gPlayerList:
                    if player.snake_id != snake.id:
                        player.score += 1
                        player.won()
                # Add the nodes back
                for i in range(1, nodesToRemove):
                        snake.trailGroup.add(snake.tailNodes[len(snake.tailNodes) - i])
                print (str(snake.id) + " colliding with self")
                return True
            # Add the nodes back
            for i in range(1, nodesToRemove):
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
    scoreTitleSurf = scoreFont.render('Scores:', True, WHITE)
    scoreTitleRect = scoreTitleSurf.get_rect()
    scoreTitleRect.topleft = (10, 10)
    DISPLAYSURF.blit(scoreTitleSurf, scoreTitleRect)
    
    i = 1
    for player in gPlayerList:
        newScoreSurf = scoreFont.render('Player ' + str(player.player_id) + ': ' + str(player.score), True, WHITE)
        newScoreRect = newScoreSurf.get_rect()
        newScoreRect.topleft = (10, 10 + (newScoreRect.height * i))
        DISPLAYSURF.blit(newScoreSurf, newScoreRect)
        i += 1
    
def drawPlayerXWins(player):
    msgFont = pygame.font.Font('freesansbold.ttf', 30)
    msg = "Player " + str(player.player_id) + " wins!"
    msgSurf = msgFont.render(msg, True, DARKGRAY)
    msgRect = msgSurf.get_rect()
    msgRect.midtop = (WIDTH/2, msgRect.height + 10)
    DISPLAYSURF.blit(msgSurf, msgRect)
         
def startScreen():
    logoSurf = pygame.image.load(IMG_LOGO)
    logoRect = logoSurf.get_rect()
    logoRect.center = (WIDTH/2, HEIGHT/2)
    
    DISPLAYSURF.blit(gBgImg, gBgRect)
    DISPLAYSURF.blit(logoSurf, logoRect)
    drawPressAnyKeyToContinue()
    
    pygame.display.update()
    
    while True:
        if waitForKeyPress():
            return
            
    FPSCLOCK.tick(FPS)
         
def gameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    
    gameSurf = gameOverFont.render('Game', True, DARKGRAY)
    overSurf = gameOverFont.render('Over', True, DARKGRAY)
  
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
   
    gameRect.midtop = (WIDTH / 2, (HEIGHT / 2) - gameRect.height)
    overRect.midtop = (WIDTH / 2, gameRect.midbottom[1] + 20)
    
    for player in gPlayerList:
        if player.isWinner == True:
            drawPlayerXWins(player)
    
    drawPressAnyKeyToContinue()
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    
    # Debug
    print("P1 score: " + str(gPlayerList[PLAYER_ONE].score))
    print("P2 score: " + str(gPlayerList[PLAYER_TWO].score))

    pygame.display.update()
    pygame.time.wait(500)
     
    pygame.event.get() # Not sure if this makes a difference
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
