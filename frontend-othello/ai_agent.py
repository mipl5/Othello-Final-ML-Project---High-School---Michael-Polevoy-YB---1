import tensorflow as tf
import numpy as np
from constants import BOARD_SIZE, BLACK, WHITE
import os
import random

class AIAgent:
    def __init__(self, model_path, color=WHITE, difficulty=1.0):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        self.color = color
        self.difficulty = difficulty

    def get_move(self, board):
        valid_moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                flips = board.get_flips(r, c, self.color)
                if flips and board.grid[r][c].is_empty():
                    valid_moves.append((r, c))

        if not valid_moves:
            return None

        # --- DIFFICULTY SCALING (Epsilon-Greedy) ---
        # random.random() generates a decimal between 0.0 and 1.0.
        # If it is less than our difficulty (e.g. 0.75), the AI uses the neural network 
        # to find the absolute best move. Otherwise, it skips to the 'else' block
        # and picks a completely random move. 
        # CATCH: While this efficiently scales difficulty and mathematical win-rate, 
        # the random moves might occasionally be terribly bad rather than understandable "human-like" mistakes.
        if random.random() < self.difficulty:
            best_move = None
            highest_score = -1

            for r, c in valid_moves:
                state = self._get_state_from_board(board)
                flat_state = state.flatten()

                input_tensor = np.expand_dims(flat_state, axis=0)
                score = self.model.predict(input_tensor, verbose=0)[0][0]

                if score > highest_score:
                    highest_score = score
                    best_move = (r, c)
            return best_move
        else:
            return random.choice(valid_moves)

    def _get_state_from_board(self, board):
        state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = board.grid[r][c]
                if not cell.is_empty():
                    if cell.piece.color == self.color:
                        state[r, c] = 1
                    else:
                        state[r, c] = -1
        return state
