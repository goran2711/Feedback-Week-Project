class Player():
    numPlayers = 1

    def __init__(self):
        self.snake_id = -1
        self.player_id = Player.numPlayers
        Player.numPlayers += 1
        self.score = 0
        self.isLoser = False
        
    def assignSnake(self, snake_id):
        self.snake_id = snake_id
        
    def lost(self):
        self.isLoser = True
        
    def newRoundReset(self):
        self.isLoser = False