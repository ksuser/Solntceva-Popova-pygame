class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--" , "--", "--", "--", "--", "--", "--"],
            ["--", "--" , "--", "--", "--", "--", "--", "--"],
            ["--", "--" , "--", "--", "--", "--", "--", "--"],
            ["--", "--" , "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.movelog = []
       
    #принимает парааметр Move и выполняет его(не работает для рокировки)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Добавление хода в список для возможности его отмены позже
        self.whiteToMove = not self.whiteToMove  # Ход другого игрока


    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][column][1]
                    self.moveFunctions[piece](row, column, moves)
        return moves           
                    
    
    def getPawnMoves(self, row, column, moves):
        if self.whiteToMove:
            if self.board[row-1][column] == "--":
                moves.append(Move((row, column), (row-1, column), self.board))
                if row == 6 and self.board[row-2][column]:
                    moves.append(Move((row, column), (row-2, column), self.board))
            if column - 1 >= 0:
                if self.board[row-1][column-1][0] == 'b':
                    moves.append(Move((row, column), (row-1, column-1), self.board))
            if column + 1 <= 7: #len(self.road)
                if self.board[row-1][column+1][0] == 'b':
                    moves.append(Move((row, column), (row-1, column+1), self.board))
        else: #движение чёрной пешки


    def getRookMoves(self, row, column, moves):
        pass

    def getKnightMoves(self, row, column, moves):
        pass

    def getBishopMoves(self, row, column, moves):
        pass

    def getQueenMoves(self, row, column, moves):
        pass

    def getKingMoves(self, row, column, moves):
        pass

    
class Move:
    # Сопоставляет ключи со значениями
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 1000 + self.endRow * 10 + self.endCol
        print(self.moveID)

    def __eq__(self, other):
        if isinstance(other, Move):
           return self.moveID == other.moveID
        return False 


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
