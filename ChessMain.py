import pygame as p
from ChessEngine import GameState

width = height = 512
dimension = 8 #поле шахматное 8 * 8
sq_size = height // dimension
max_FPS = 15 #для анимации
images = {}

def loadImages():
    pieces = ["wp", "bp", "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load((r"C:\Users\Alina\Desktop\learning\YandexLyceum\Chess\images\\") + piece + ".png"), (sq_size, sq_size))

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running == False
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
                screen.blit(images[piece], p.Rect(columns*sq_size, rows*sq_size, sq_size, sq_size))




if __name__ == '__main__':
    main()