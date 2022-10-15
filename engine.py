class GameState:
    def __init__(self):
        self.board = []
        
        self.player_1 = True

    def makeMove(self, move):
        if move.playingType == "inverted":
            allValidCoords = [(move.Row, move.Col-1), (move.Row, move.Col+1), (move.Row-1, move.Col), (move.Row+1, move.Col), (move.Row-1, move.Col-1), (move.Row-1, move.Col+1), (move.Row+1, move.Col-1), (move.Row+1, move.Col+1)]
        elif move.playingType == "normal":
            allValidCoords = [(move.Row, move.Col)]
        elif move.playingType == "diagonal":
            allValidCoords = [(move.Row-1, move.Col-1), (move.Row-1, move.Col+1), (move.Row+1, move.Col-1), (move.Row+1, move.Col+1)]
        else:
            allValidCoords = [(move.Row, move.Col-1), (move.Row, move.Col+1), (move.Row-1, move.Col), (move.Row+1, move.Col)]
        
        for i in range(len(allValidCoords)-1, -1, -1):
            if allValidCoords[i][0] < 0 or allValidCoords[i][0] >= len(self.board) or allValidCoords[i][1] < 0 or allValidCoords[i][1] >= len(self.board):
                allValidCoords.pop(i)
        
        for item in allValidCoords:
            self.board[item[0]][item[1]] = move.color
        
        self.player_1 = not self.player_1
        
    def color_count(self, color):
        i = 0
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == color:
                    i += 1
        
        return i
    
    def end_game(self):
        return self.color_count("white") == 0


class Move:
    def __init__(self, Sq, color, playingType = "inverted"):
        self.Row = Sq[0]
        self.Col = Sq[1]
        self.color = color
        self.playingType = playingType
