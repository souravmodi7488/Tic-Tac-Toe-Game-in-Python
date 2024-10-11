import numpy as np # Sourav Kumar
import pygame, sys

pygame.init()

# variables
width = 600
height = 600
boardrow = 3
boardcolumn = 3
linecolor = (255, 0, 0)
widthline = 15
circleradius = 60
circlewidth = 15
space = 55
crosswidth = 15

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Tic Tac Toe')

board = np.zeros((boardrow, boardcolumn))

screen.fill((0, 0, 0))

def drawline():
    pygame.draw.line(screen, linecolor, (0, 200), (600, 200), widthline)
    pygame.draw.line(screen, linecolor, (0, 400), (600, 400), widthline)
    pygame.draw.line(screen, linecolor, (200, 0), (200, 600), widthline)
    pygame.draw.line(screen, linecolor, (400, 0), (400, 600), widthline)

def drawfig():
    for row in range(boardrow):
        for col in range(boardcolumn):
            if board[row][col] == 1:
                pygame.draw.circle(screen, (255, 255, 0), (int(col * 200 + 100), int(row * 200 + 100)), circleradius, circlewidth)
            elif board[row][col] == 2:
                pygame.draw.line(screen, (255, 255, 0), (col * 200 + space, row * 200 + 200 - space), (col * 200 + 200 - space, row * 200 + space), crosswidth)
                pygame.draw.line(screen, (255, 255, 0), (col * 200 + space, row * 200 + space), (col * 200 + 200 - space, row * 200 + 200 - space), crosswidth)

def mark(row, column, player):
    board[row][column] = player

def available(row, column):
    return board[row][column] == 0

def drawverticalwinningline(column, player):
    posX = column * 200 + 100
    pygame.draw.line(screen, (255, 0, 0), (posX, 15), (posX, height - 15), 15)

def drawhorizontalwinningline(row, player):
    posY = row * 200 + 100
    pygame.draw.line(screen, (255, 0, 0), (15, posY), (width - 15, posY), 15)

def drawascendingwinningline(player):
    pygame.draw.line(screen, (255, 0, 0), (15, height - 15), (width - 15, 15), 15)

def drawdescendingwinningline(player):
    pygame.draw.line(screen, (255, 0, 0), (15, 15), (width - 15, height - 15), 15)

def isboardful():
    for row in range(boardrow):
        for column in range(boardcolumn):
            if board[row][column] == 0:
                return False
    return True

def checkwinner(player):
    # Vertical check
    for column in range(boardcolumn):
        if board[0][column] == player and board[1][column] == player and board[2][column] == player:
            drawverticalwinningline(column, player)
            return True

    # Horizontal check
    for row in range(boardrow):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            drawhorizontalwinningline(row, player)
            return True

    # Ascending diagonal check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        drawascendingwinningline(player)
        return True

    # Descending diagonal check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        drawdescendingwinningline(player)
        return True

    return False

def restart():
    screen.fill((100, 170, 100))
    drawline()
    for row in range(boardrow):
        for column in range(boardcolumn):
            board[row][column] = 0

drawline()
player = 1
gameover = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clickedrow = int(mouseY // 200)
            clickedcolumn = int(mouseX // 200)

            if available(clickedrow, clickedcolumn):
                mark(clickedrow, clickedcolumn, player)
                if checkwinner(player):
                    gameover = True
                player = 3 - player  # switch between player 1 and 2
                drawfig()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                gameover = False

    pygame.display.update()
