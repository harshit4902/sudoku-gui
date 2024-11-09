import pygame
from typing import Tuple
from sudoku import Sudoku
import random
import os

pygame.init()
WIDTH = 720
HEIGHT = 770
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUDOKU")

EASY = random.randint(32, 40)
MEDIUM = random.randint(40, 48)
HARD = random.randint(48, 55)
logo = pygame.image.load("assets/sudoku.png")
easy = pygame.image.load("assets/EASY.PNG")
medium = pygame.image.load(
    "assets/MEDIUM.PNG")
hard = pygame.image.load("assets/HARD.PNG")
gameover = pygame.image.load(
    "assets/gameover.png")
paused = pygame.image.load(
    "assets/paused.png")
pauselogo = pygame.image.load(
    "assets/pause.png")
newgamebutton = pygame.image.load(
    "assets/newgame.png")
excellent = pygame.image.load(
    "assets/excellent.png")
noteon = pygame.image.load("assets/on.png")
noteoff = pygame.image.load("assets/off.png")


class Note:
    # data = [[[False]*10]*9]*9
    data = []
    font = pygame.font.SysFont("arial", 20)

    @staticmethod
    def init():
        for i in range(9):
            line = []
            for j in range(9):
                box = [False]
                for num in range(1, 10):
                    box.append(False)
                line.append(box)
            Note.data.append(line)

    @staticmethod
    def draw(board, isnote):
        if isnote:
            WIN.blit(noteon, (570, 12))
        else:
            WIN.blit(noteoff, (570, 12))
        for i in range(9):
            for j in range(9):
                for num in range(1, 10):
                    if Note.data[i][j][num] and not board[i][j][1]:
                        text = Note.font.render(str(num), 1, "grey")
                        x = j*80 + 17 + ((num-1) % 3)*27 - text.get_width()
                        y = i*80 + 75 + ((num-1)//3)*27 - text.get_height()
                        WIN.blit(text, (x, y))

    @staticmethod
    def update(row, column, num):
        Note.data[row][column] = [False]*10
        for i in range(9):
            Note.data[row][i][num] = False
            Note.data[i][column][num] = False
        r = row//3*3
        c = column//3*3
        for i in range(r, r+3):
            for j in range(c, c+3):
                Note.data[i][j][num] = False

    @staticmethod
    def reset():
        Note.data = []
        Note.init()


def box(x, y, width, height):
    pygame.draw.line(WIN, "red", (x, y), (x, y+height), 4)
    pygame.draw.line(WIN, "red", (x, y), (x+width, y), 4)
    pygame.draw.line(WIN, "red", (x+width, y), (x+width, y+height), 4)
    pygame.draw.line(WIN, "red", (x, y+height), (x+width, y+height), 4)


def start():
    clock = pygame.time.Clock()
    start = True
    while start:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] in range(200, 500) and pos[1] in range(350, 430):
                    difficulty = EASY
                    start = False

                elif pos[0] in range(150, 560) and pos[1] in range(490, 570):
                    difficulty = MEDIUM
                    start = False
                elif pos[0] in range(200, 500) and pos[1] in range(630, 710):
                    difficulty = HARD
                    start = False
        WIN.fill("white")
        WIN.blit(logo, (3, 50))
        WIN.blit(easy, (720//2-easy.get_width()//2, 340))
        box(200, 350, 300, 80)
        WIN.blit(medium, (720//2-medium.get_width()//2, 480))
        box(150, 490, 410, 80)
        WIN.blit(hard, (720//2-hard.get_width()//2, 620))
        box(200, 630, 300, 80)
        pygame.display.update()
    sudoku = Sudoku(9, difficulty)
    sudoku.fillValues()
    board = initboard(sudoku)
    sudoku.solve()
    solved = sudoku.board
    return board, solved


def initboard(sudoku):
    board = []
    for i in range(9):
        line = []
        for j in range(9):
            line.append((sudoku.board[i][j] if sudoku.board[i]
                        [j] != None else 0, bool(sudoku.board[i][j])))
        board.append(line)

    return board


class Block:
    def __init__(self, size: int, width: int, color="black"):
        self.size = size
        self.width = width
        self.color = color

    def draw(self, pos: Tuple[int]):
        self.pos = pos
        size = self.size
        width = self.width
        color = self.color
        x, y = pos
        pygame.draw.line(WIN, color, (x, y), (x+size, y), width)
        pygame.draw.line(WIN, color, (x, y), (x, y+size), width)
        pygame.draw.line(WIN, color, (x+size, y), (x+size, y+size), width)
        pygame.draw.line(WIN, color, (x, y+size), (x+size, y+size), width)


def drawBlocks():
    block = Block(240, 4)
    for i in range(0, 720, block.size):
        for j in range(50, 720+50, block.size):
            block.draw((i, j))


def drawBox():
    box = Block(80, 2, "grey")
    for i in range(0, 720, box.size):
        for j in range(50, 720+50, box.size):
            box.draw((i, j))


def drawNumbers(board, solved):
    font = pygame.font.SysFont("arial", 30, bold=True)
    for i in range(9):
        for j in range(9):
            if board[i][j][0] == 0:
                continue
            if board[i][j][1]:
                text = font.render(str(board[i][j][0]), 1, "black")
            else:
                if board[i][j][0] == solved[i][j]:
                    text = font.render(str(board[i][j][0]), 1, "blue")
                else:
                    text = font.render(str(board[i][j][0]), 1, "red")

            WIN.blit(text, (j*(720//9)+40-text.get_width() //
                     2, i*(720//9)+40-text.get_height()//2+50))


def formatTime(time: int):
    s = str(time % 60)
    m = str(time//60 % 60)
    h = str(time//3600)
    s = s if len(s) == 2 else "0"+s
    m = m if len(m) == 2 else "0"+m
    h = h if len(h) == 2 else "0"+h
    return f"{h}:{m}:{s}"


def drawMenu(time: int, mistake: int):
    font1 = pygame.font.SysFont("cambria", 30, bold=True)
    font2 = pygame.font.SysFont("cambria", 30)
    text = font1.render("Time: ", 1, "black")
    time = font2.render(formatTime(time), 1, "black")
    WIN.blit(text, (20, 10))
    WIN.blit(time, (20+text.get_width(), 10))
    text = font1.render("Mistake: ", 1, "black")
    mistake = font2.render(str(mistake)+"/3", 1, "black")
    WIN.blit(text, (280, 10))
    note = font1.render("Note : ", 1, "black")
    WIN.blit(note, (570-note.get_width(), 10))
    WIN.blit(mistake, (280+text.get_width(), 10))
    WIN.blit(pauselogo, (670, 5))


def pause():
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] in range(160, 570) and pos[1] in range(420, 510):
                    return False
                if pos[0] in range(147, 583) and pos[1] in range(553, 640):
                    return True
        WIN.fill("white")
        WIN.blit(logo, (3, 50))
        WIN.blit(paused, (720//2 - paused.get_width()//2, 390))
        pygame.display.update()


def checkSolve(board, sudoku):
    for i in range(9):
        for j in range(9):
            if board[i][j][0] != sudoku[i][j]:
                return False
    return True


def main():
    board, solved = start()
    clock = pygame.time.Clock()
    redBox = Block(720//9, 4, "red")
    Note.init()
    locked = False
    pos = None
    time = 0
    mistake = 0
    newgame = False
    again = False
    isnote = False
    while True:
        clock.tick(FPS)
        if not locked:
            time += 1/FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if mistake >= 3:
                    if pos[0] in range(140, 575) and pos[1] in range(427, 517):
                        newgame = True
                else:
                    if pos[0] in range(680, 707) and pos[1] in range(15, 42):
                        newgame = pause()
                    elif pos[0] in range(570, 631) and pos[1] in range(12, 44):
                        isnote = not isnote
                if pos[1] > 50:
                    col, row = pos[0]//(720//9), (pos[1]-50)//(720//9)
                pos = (col*(720//9), row*(720//9)+50)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and again:
                    newgame = True
                    again = False
                if event.key == pygame.K_ESCAPE and mistake < 3:
                    for i in range(9):
                        for j in range(9):
                            board[i][j] = (solved[i][j], board[i][j][1])
                if not pos:
                    break
                if event.key == pygame.K_UP and row != 0:
                    row -= 1
                    pos = (col*(720//9), row*(720//9)+50)
                if event.key == pygame.K_DOWN and row != 8:
                    row += 1
                    pos = (col*(720//9), row*(720//9)+50)
                if event.key == pygame.K_LEFT and col != 0:
                    col -= 1
                    pos = (col*(720//9), row*(720//9)+50)
                if event.key == pygame.K_RIGHT and col != 8:
                    col += 1
                    pos = (col*(720//9), row*(720//9)+50)
                if mistake >= 3:
                    if event.key == pygame.K_ESCAPE:
                        mistake = 2
                        locked = False
                if event.key == pygame.K_BACKSPACE and not locked:
                    if board[row][col][1] == 0:
                        board[row][col] = (0, 0)
                elif not locked:
                    if event.key == pygame.K_LSHIFT:
                        isnote = not isnote
                    num = event.unicode
                    if num.isdigit() and not board[row][col][1]:
                        if isnote and board[row][col][1] == 0:
                            Note.data[row][col][int(
                                num)] = not Note.data[row][col][int(num)]
                            board[row][col] = (0, 0)
                        else:
                            if board[row][col][0] == int(num):
                                board[row][col] = (0, 0)
                            else:
                                if solved[row][col] != int(num):
                                    mistake += 1
                                board[row][col] = (int(num), 0)
                                Note.update(row, col, int(num))

        WIN.fill("white")
        if newgame:
            board, solved = start()
            time = 0
            mistake = 0
            newgame = False
            pos = None
            locked = False
            isnote = False
            Note.reset()

        if mistake >= 3:
            WIN.blit(gameover, (720//2-gameover.get_width()//2, 100))
            WIN.blit(newgamebutton, (720//2-newgamebutton.get_width()//2, 400))
            locked = True
        else:
            drawMenu(int(time), mistake)
            drawBox()
            drawBlocks()
            drawNumbers(board, solved)
            Note.draw(board, isnote)
            if pos:
                if pos[1] > 0:
                    redBox.draw(pos)

        if checkSolve(board, solved):
            locked = True
            again = True
            WIN.blit(excellent, (72, 200))
            pygame.draw.rect(WIN, "cyan", (100, 420, 520, 70),
                             border_radius=10)
            font = pygame.font.SysFont("arial", 20)
            text1 = font.render(
                f"You took {formatTime(int(time))} to solve.", 1, "black")
            text2 = font.render(f"Press Enter to start again.", 1, "black")
            WIN.blit(text1, (270, 430))
            WIN.blit(text2, (275, 460))

        pygame.display.update()


try:
    main()
except:
    pass
