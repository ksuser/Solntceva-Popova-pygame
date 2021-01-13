class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    # принимает парааметр Move и выполняет его(не работает для рокировки)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Добавление хода в список для возможности его отмены позже
        self.whiteToMove = not self.whiteToMove  # Ход другого игрока
        # Обновление местоположения короля, если игрок его переместит
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    # Определение, проверяется ли игрок
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # Определение, может ли вражеская фигура атаковать клетку
    def squareUnderAttack(self, row, column):
        self.whiteToMove = not self.whiteToMove  # Ход соперника
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # Обновление хода
        for move in oppMoves:
            if move.endRow == row and move.endCol == column:  # Клетка находится под ударом (королю объявлен шах)
                """self.whiteToMove = not self.whiteToMove  # Курсор возвращается назад, если игрок жмет на фигуру,
                # которая не может защитить короля / не на короля (??)  // Обновление хода"""
                return True
        return False

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
            if self.board[row - 1][column] == "--":
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column]:
                    moves.append(Move((row, column), (row - 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == 'b':
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
            if column + 1 <= 7:  # len(self.road)
                if self.board[row - 1][column + 1][0] == 'b':
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))
        else:  # движение чёрной пешки
            if self.board[row + 1][column] == '--':  # Продвижение пешки на 1 клетку
                moves.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == '--':  # Продвижение пешки на 2 клетки
                    moves.append(Move((row, column), (row + 2, column), self.board))
                # Захват вражеских фигур
                if column - 1 >= 0:
                    if self.board[row + 1][column - 1][0] == 'w':  # Захват фигуры врага: движение по левой диагонали
                        moves.append(Move((row, column), (row + 1, column - 1), self.board))
                if column + 1 <= 7:
                    if self.board[row + 1][column + 1][0] == 'w':  # Захват фигуры врага: движение по правой диагонали
                        moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def getRookMoves(self, row, column, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Направления вверх, вниз, влево и вправо
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        for j in directions:
            for i in range(1, 8):
                endRow = row + j[0] * i
                endCol = column + j[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # На доске
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Допустимая свободная клетка
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Клетка, на которой расположена вражеская фигура
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else:  # При нажатии на клетку, где расположена фигура того же цвета, что и ладья
                        break
                else:  # Доска закрывается
                    break

    def getKnightMoves(self, row, column, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'
        for i in knightMoves:
            endRow = row + i[0]
            endCol = column + i[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Пустая клетка или вражеская фигура
                    moves.append(Move((row, column), (endRow, endCol), self.board))

    def getBishopMoves(self, row, column, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        for j in directions:
            for i in range(1, 8):  # Слон может двигаться максимум на 7 клеток
                endRow = row + j[0] * i
                endCol = column + j[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Допустимая свободная клетка
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Клетка, где расположена вражеская фигура
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else:  # Нажатие на клетку, где расположена вражеская фигура
                        break
                else:  # Доска закрывается
                    break

    def getQueenMoves(self, row, column, moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'
            for i in range(8):
                endRow = row + kingMoves[i][0]
                endCol = column + kingMoves[i][1]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:  # Пустая клетка или вражеская фигура
                        moves.append(Move((row, column), (endRow, endCol), self.board))

    def undoMove(self):
        if len(self.moveLog) != 0: # есть что отменять
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)


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
