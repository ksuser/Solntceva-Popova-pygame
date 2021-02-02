import pygame as p
import ChessEngine
from ChessEngine import GameState, Move

width = height = 512
dimension = 8  # поле шахматное 8 * 8
sq_size = height // dimension
max_FPS = 15  # для анимации
images = {}


def loadImages():
    pieces = ["wp", "bp", "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "wR", "wN", "wB", "wQ", "wK", "wB", "wN",
              "wR"]
    for piece in pieces:
        images[piece] = p.transform.scale(
            p.image.load(r"..\PyGame_Project\Figure\\" + piece + ".png"),
            (sq_size, sq_size))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    p.display.set_caption('PyGame Project: Шахматы.')
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()  # Отслеживание последнего щелчка игрока
    playerClicks = []  # Отслеживание щелчков игрока на доске

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # Позиция мышки (x, y)
                col = location[0] // sq_size
                row = location[1] // sq_size
                if sqSelected == (row, col):  # Проверка, щелкнул ли игрок на один и тот же квадрат дважды или нет
                    sqSelected = ()  # Отмена двойного нажатия
                    playerClicks = []  # Сброс кликов игрока
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # Добавление и первого, и второго клика в список
                if len(playerClicks) == 2:  # Проверка после второго клика - был ли он совершен
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        animate = True
                        sqSelected = ()  # Сброс кликов игрока
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Отмена хода при нажании клавиши "z"
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(max_FPS)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        row, column = sqSelected
        if gs.board[row][column][0] == ('w' if gs.whiteToMove else 'b'):  # Может ли двигаться фигура на клетке
            # Выделение клетки(ок)
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100)  # Прозрачность
            s.fill(p.Color('blue'))
            screen.blit(s, (sq_size * column, sq_size * row))
            # Перемещение подсветки на клетку(и)
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startCol == column:
                    screen.blit(s, (move.endCol * sq_size, move.endRow * sq_size))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for rows in range(dimension):
        for columns in range(dimension):
            color = colors[((rows + columns) % 2)]
            p.draw.rect(screen, color, p.Rect(columns * sq_size, rows * sq_size, sq_size, sq_size))


def drawPieces(screen, board):
    for rows in range(dimension):
        for columns in range(dimension):
            piece = board[rows][columns]
            if piece != "--":
                screen.blit(images[piece], p.Rect(columns * sq_size, rows * sq_size, sq_size, sq_size))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, column = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * sq_size, move.endRow * sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)
        screen.blit(images[move.pieceMoved], p.Rect(column * sq_size, row * sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
