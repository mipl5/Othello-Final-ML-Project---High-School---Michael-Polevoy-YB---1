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

font = pygame.font.SysFont('Arial', 32, bold=True)

def draw_status(surface, board, current_player):
    black_count, white_count = board.get_counts()
    
    pygame.draw.rect(surface, (50, 50, 50), (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))
    
    black_text = font.render(f"Black: {black_count}", True, (255, 255, 255))
    white_text = font.render(f"White: {white_count}", True, (255, 255, 255))
    
    turn_color = "Black" if current_player == BLACK else "White"
    turn_text = font.render(f"{turn_color}'s Turn", True, (255, 215, 0))
    
    surface.blit(black_text, (20, HEADER_HEIGHT // 2 - black_text.get_height() // 2))
    surface.blit(white_text, (WINDOW_WIDTH - white_text.get_width() - 20, HEADER_HEIGHT // 2 - white_text.get_height() // 2))
    surface.blit(turn_text, (WINDOW_WIDTH // 2 - turn_text.get_width() // 2, HEADER_HEIGHT // 2 - turn_text.get_height() // 2))

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()
            
            y -= HEADER_HEIGHT

            if y >= 0:
                col = x // CELL_SIZE
                row = y // CELL_SIZE

                if board.make_move(row, col, current_player):

                    if current_player == BLACK:
                        current_player = WHITE
                    else:
                        current_player = BLACK

    screen.fill(GREEN)
    board.draw(screen)
    draw_status(screen, board, current_player)

    pygame.display.flip()

pygame.quit()