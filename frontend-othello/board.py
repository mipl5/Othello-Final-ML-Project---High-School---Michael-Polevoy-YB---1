from cell import Cell
from player import Piece
from constants import BOARD_SIZE, BLACK, WHITE

DIRECTIONS = [
    (-1, 0), (1, 0),
    (0, -1), (0, 1),
    (-1, -1), (-1, 1),
    (1, -1), (1, 1)
]

class Board:
    def __init__(self):
        self.grid = [
            [Cell(r, c) for c in range(BOARD_SIZE)]
            for r in range(BOARD_SIZE)
        ]

        self.initialize()

    def initialize(self):
        mid = BOARD_SIZE // 2

        self.grid[mid-1][mid-1].place_piece(Piece(WHITE))
        self.grid[mid][mid].place_piece(Piece(WHITE))
        self.grid[mid-1][mid].place_piece(Piece(BLACK))
        self.grid[mid][mid-1].place_piece(Piece(BLACK))

    def draw(self, surface):
        for row in self.grid:
            for cell in row:
                cell.draw(surface)

    def in_bounds(self, r, c):
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def opponent(self, color):
        return BLACK if color == WHITE else WHITE

    def get_flips(self, row, col, color):
        flips = []

        for dr, dc in DIRECTIONS:
            r = row + dr
            c = col + dc
            line = []

            while self.in_bounds(r, c):
                cell = self.grid[r][c]

                if cell.is_empty():
                    break

                if cell.piece.color == self.opponent(color):
                    line.append(cell)

                elif cell.piece.color == color:
                    flips.extend(line)
                    break

                r += dr
                c += dc

        return flips

    def make_move(self, row, col, color):
        cell = self.grid[row][col]

        if not cell.is_empty():
            return False

        flips = self.get_flips(row, col, color)

        if not flips:
            return False

        cell.place_piece(Piece(color))

        for flip_cell in flips:
            flip_cell.piece.flip()

        return True