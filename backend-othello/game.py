import random
import copy
import numpy as np

class Game:
    def __init__(self, size=6):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.winner = None
        self.init_board()
    
    def init_board(self):
        # 1 - Black, -1 - White
        mid = self.size // 2
        self.board[mid-1, mid-1] = -1
        self.board[mid, mid] = -1
        self.board[mid-1, mid] = 1
        self.board[mid, mid-1] = 1
        
    def play(self):
        player = 1 # always black starts the game

    def make_move(self, player):
        # ...

    def check_winner(self):
        # ...

    def perform_agent_move(self):
        self.make(1) # later I will use model to make a move, now random

    def perform_rival_move(self):
        self.make(-1)

    def print_game_result(self):
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == -1)
        print(f'Black: {black_count}, White: {white_count}')
        if black_count > white_count:
            print(f'Black wins! {black_count} vs {white_count}')
        elif white_count > black_count:
            print(f'White wins! {black_count} vs {white_count}')
        else:
            print(f'Draw! {black_count} vs {white_count}')

    def get_board_state(self):
        return copy.deepcopy(self.board)

    def print_board(self):
        symbols = {0: '.', 1: 'B', -1:'W'}
        for row in range(self.size):
            print(' '.join([symbols[self.board[row, col]] for col in range(self.size)]))
        print()

    def calculate_board_scores(self):
        # because there are only values
        # 1 and -1, I can just sum the board to 
        # get the score
        return np.sum(self.board)

    def get_free_cells(self):
        return list(zip(*np.where(self.board == 0)))