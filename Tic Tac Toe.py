import numpy as np
import pygame, sys

pygame.init()

# Variables
width = 600
height = 700  # Increased height to make room for messages
boardrow = 3
boardcolumn = 3
linecolor = (0, 0, 255)  # Blue color for lines
widthline = 15
circleradius = 60
circlewidth = 15
space = 55
crosswidth = 15

# Set up the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')

# Fonts for messages
font = pygame.font.Font(None, 60)  # For player turn
winner_font = pygame.font.Font(None, 100)  # For winner display

# Create a 3x3 board initialized to 0
board = np.zeros((boardrow, boardcolumn))

# Fill screen background with black
screen.fill((0, 0, 0))

def drawline():
    # Draw the horizontal and vertical lines (blue)
    pygame.draw.line(screen, linecolor, (0, 200), (600, 200), widthline)
    pygame.draw.line(screen, linecolor, (0, 400), (600, 400), widthline)
    pygame.draw.line(screen, linecolor, (200, 0), (200, 600), widthline)
    pygame.draw.line(screen, linecolor, (400, 0), (400, 600), widthline)

def drawfig():
    # Draw circles and X marks (both in yellow)
    for row in range(boardrow):
        for col in range(boardcolumn):
            if board[row][col] == 1:
                pygame.draw.circle(screen, (255, 255, 0), (int(col * 200 + 100), int(row * 200 + 100)), circleradius, circlewidth)
            elif board[row][col] == 2:
                pygame.draw.line(screen, (255, 255, 0), (col * 200 + space, row * 200 + 200 - space), (col * 200 + 200 - space, row * 200 + space), crosswidth)
                pygame.draw.line(screen, (255, 255, 0), (col * 200 + space, row * 200 + space), (col * 200 + 200 - space, row * 200 + 200 - space), crosswidth)

def display_message(text, color=(255, 255, 255), font_size=60, center=False):
    message_font = pygame.font.Font(None, font_size)
    message = message_font.render(text, True, color)
    message_rect = message.get_rect(center=(width // 2, height - 50))  # Always at the bottom
    screen.fill((0, 0, 0), (0, 600, 600, 100))  # Clear the message area (bottom part of the screen)
    screen.blit(message, message_rect)

def mark(row, column, player):
    board[row][column] = player

def available(row, column):
    return board[row][column] == 0

def drawverticalwinningline(column, player):
    posX = column * 200 + 100
    pygame.draw.line(screen, (255, 0, 0), (posX, 15), (posX, height - 115), 15)  # Adjusted to account for message area

def drawhorizontalwinningline(row, player):
    posY = row * 200 + 100
    pygame.draw.line(screen, (255, 0, 0), (15, posY), (width - 15, posY), 15)

def drawascendingwinningline(player):
    pygame.draw.line(screen, (255, 0, 0), (15, height - 115), (width - 15, 15), 15)

def drawdescendingwinningline(player):
    pygame.draw.line(screen, (255, 0, 0), (15, 15), (width - 15, height - 115), 15)

def isboardful():
    for row in range(boardrow):
        for column in range(boardcolumn):
            if board[row][column] == 0:
                return False
    return True

def checkwinner(player):
    # Check vertical win
    for column in range(boardcolumn):
        if board[0][column] == player and board[1][column] == player and board[2][column] == player:
            drawverticalwinningline(column, player)
            return True

    # Check horizontal win
    for row in range(boardrow):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            drawhorizontalwinningline(row, player)
            return True

    # Check ascending diagonal win
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        drawascendingwinningline(player)
        return True

    # Check descending diagonal win
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        drawdescendingwinningline(player)
        return True

    return False

def restart():
    # Refill screen with black and redraw lines
    screen.fill((0, 0, 0))
    drawline()
    for row in range(boardrow):
        for column in range(boardcolumn):
            board[row][column] = 0

# Draw the initial lines
drawline()
player = 1
gameover = False

# Display the initial player turn
display_message("Player 1's Turn", (255, 0, 0))  # Player 1's message in red

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
                drawfig()
                if checkwinner(player):
                    gameover = True
                    display_message(f"Player {player} Wins!", (0, 255, 0), 60)  # Winner message in green at bottom
                elif isboardful():
                    gameover = True
                    display_message("It's a Tie!", (255, 255, 255), 60)  # Tie message at bottom
                else:
                    player = 3 - player  # Switch between player 1 and player 2
                    # Update turn message with color coding
                    display_message(f"Player {player}'s Turn", (0, 0, 255) if player == 2 else (255, 0, 0))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                gameover = False
                player = 1
                display_message("Player 1's Turn", (255, 0, 0))  # Reset message to Player 1

    pygame.display.update()
