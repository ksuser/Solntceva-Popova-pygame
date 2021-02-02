import pygame as p
import ChessEngine56
from ChessEngine56 import GameState, Move

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
            p.image.load(r"C:\Yandex\Python\PyGame_Project\Figure\\" + piece + ".png"),
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
                    move = ChessEngine56.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # Сброс кликов игрока
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Отмена хода при нажании клавиши "z"
                    gs.undoMove()
                if e.key == p.K_r:
                    gs = ChessEngine56.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(max_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
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


if __name__ == '__main__':
    main()
