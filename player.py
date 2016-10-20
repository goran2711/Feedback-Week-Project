class Player():
    numPlayers = 1

    def __init__(self):
        self.snake_id = -1
        self.player_id = Player.numPlayers
        Player.numPlayers += 1
        self.score = 0
        self.isWinner = False
        
    def assignSnake(self, snake_id):
        self.snake_id = snake_id
        
    def won(self):
        self.isWinner = True
        
    def newRoundReset(self):
        self.isWinner = False