from game import Game
import csv
import random
import numpy as np

class Tournament:
    def __init__(self, size=6, discount=0.9):
        self.size = size
        self.gamma = discount
        self.data_log = []

    def play_games(self, count=1):
        for g_id in range(count):
            game = Game(self.size)
            turns = []
            print(f"=== NEW TOURNAMENT GAME: {g_id + 1} ===")
            game.print_board()

            current_player = 1
            
            while True:
                moves = game.get_valid_moves(current_player)

                if not moves:
                    if not game.get_valid_moves(-current_player):
                        break
                    current_player = -current_player
                    continue

                turns.append((current_player, game.board.copy()))
                r, c = random.choice(moves)
                game.make_move(r, c, current_player)

                if current_player == 1:
                    print(f"Agent (B) places at: ({r}, {c})")
                else:
                    print(f"Rival (W) places at: ({r}, {c})")

                game.print_board()
                current_player = -current_player
            
            winner = self._get_winner(game)
            self._process_history(g_id, turns, winner)

    def _get_winner(self, game):
        black = np.sum(game.board == 1)
        white = np.sum(game.board == -1)
        print(f"GAME OVER. Black: {black}, White: {white}")
        if black > white: return 1
        if white > black: return -1
        return 0

    def _process_history(self, g_id, turns, winner):
        turns.reverse()
        for i, (player, board) in enumerate(turns):
            if winner == 0:
                base = 0.2
            else:
                base = 1.0 if player == winner else 0.0
            
            # Recursive discount logic
            score = base * (self.gamma ** i)
            self.data_log.append({
                'game_id': g_id, 
                'score': round(score, 4), 
                'state': board.flatten()
            })

    def export_csv(self, filename="othello_training_data.csv"):
        headers = ['game_id', 'score'] + [f's{i}' for i in range(self.size**2)]
        with open(filename, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(headers)
            for row in self.data_log:
                w.writerow([row['game_id'], row['score']] + list(row['state']))
        print(f"Exported {len(self.data_log)} board states to {filename}")