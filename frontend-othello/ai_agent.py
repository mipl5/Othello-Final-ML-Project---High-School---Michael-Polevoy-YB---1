import tensorflow as tf
import numpy as np
from constants import BOARD_SIZE, BLACK, WHITE
import os

class AIAgent:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        self.model = tf.keras.models.load_model(model_path)

    def get_move(self, board):
        valid_moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                flips = board.get_flips(r, c, BLACK)
                if flips and board.grid[r][c].is_empty():
                    valid_moves.append((r, c))

        if not valid_moves:
            return None

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

    def _get_state_from_board(self, board):
        state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = board.grid[r][c]
                if not cell.is_empty():
                    if cell.piece.color == BLACK:
                        state[r, c] = 1
                    else:
                        state[r, c] = -1
        return state
