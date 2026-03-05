import pygame
from board import Board
from constants import *

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Othello")

clock = pygame.time.Clock()

board = Board()

current_player = BLACK

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if board.make_move(row, col, current_player):

                if current_player == BLACK:
                    current_player = WHITE
                else:
                    current_player = BLACK

    board.draw(screen)

    pygame.display.flip()

pygame.quit()