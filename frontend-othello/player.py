import pygame
from constants import BLACK, WHITE, CELL_SIZE

class Piece:
    def __init__(self, color):
        self.color = color

    def flip(self):
        if self.color == BLACK:
            self.color = WHITE
        else:
            self.color = BLACK

    def draw(self, surface, x, y):
        radius = CELL_SIZE // 2 - 6

        if self.color == BLACK:
            color = (0,0,0)
        else:
            color = (255,255,255)

        pygame.draw.circle(surface, color, (x,y), radius)
        