from os import path
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = WHITE

SOURCE_FOLDER = path.dirname(path.abspath(__file__))

WIDTH = 1280
HEIGHT = 720

FPS = 30

SNAKE_SIZE = 24

DEFAULT_MOVESPEED = 8
DEFAULT_TURNSPEED = 10

PLAYER_ONE      = 0
PLAYER_TWO      = 1
PLAYER_THREE    = 2

POWERUP_TIMER = 5000 # Time in milliseconds
POWERUPLIFESPAN = 5000 # Time in milliseconds
POWERUPAMOUNT = 5
