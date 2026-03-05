import pygame
from constants import CELL_SIZE, GREEN, GRID_COLOR, HEADER_HEIGHT

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.piece = None

    def is_empty(self):
        return self.piece is None

    def place_piece(self, piece):
        self.piece = piece

    def draw(self, surface):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE + HEADER_HEIGHT

        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(surface, GREEN, rect)
        pygame.draw.rect(surface, GRID_COLOR, rect, 1)

        if self.piece:
            center_x = x + CELL_SIZE // 2
            center_y = y + CELL_SIZE // 2
            self.piece.draw(surface, center_x, center_y)