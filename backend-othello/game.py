import random
import numpy as np
import csv

class Game:
    def __init__(self, size=6):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.init_board()
    
    def init_board(self):
        mid = self.size // 2
        self.board[mid-1, mid-1], self.board[mid, mid] = -1, -1
        self.board[mid-1, mid], self.board[mid, mid-1] = 1, 1
    
    def is_valid_move(self, r, c, player):
        if self.board[r, c] != 0: return False
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr, nc] == -player:
                nr += dr; nc += dc
                while 0 <= nr < self.size and 0 <= nc < self.size:
                    if self.board[nr, nc] == player: return True
                    if self.board[nr, nc] == 0: break
                    nr += dr; nc += dc
        return False

    def get_valid_moves(self, player):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.is_valid_move(r, c, player)]

    def make_move(self, r, c, player):
        if not self.is_valid_move(r, c, player): return
        self.board[r, c] = player
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for dr, dc in directions:
            to_flip = []
            nr, nc = r + dr, c + dc
            while 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr, nc] == -player:
                to_flip.append((nr, nc))
                nr += dr; nc += dc
            if to_flip and 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr, nc] == player:
                for fr, fc in to_flip: self.board[fr, fc] = player



    def print_board(self):
        symbols = {0: '.', 1: 'B', -1: 'W'}
        print("  " + " ".join(map(str, range(self.size))))
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join([symbols[x] for x in row]))
        print()