from game import Game
from tournament import Tournament
import random
import numpy as np

class SmartTournament(Tournament):
    def __init__(self, size=6, discount=0.9):
        super().__init__(size, discount)

    def get_smart_move(self, game, player):
        moves = game.get_valid_moves(player)
        if not moves:
            return None

        # 1. Corners (High Priority)
        corners = [(0, 0), (0, self.size - 1), (self.size - 1, 0), (self.size - 1, self.size - 1)]
        available_corners = [m for m in moves if m in corners]
        if available_corners:
            return random.choice(available_corners)

        # 2. Weighted Evaluation
        # Define weights for 6x6 board
        # Corners: 150
        # X-squares: -60 (diagonal to corner)
        # C-squares: -30 (adjacent to corner on edge)
        weights = np.array([
            [ 150, -30,  20,  20, -30, 150],
            [-30, -60,  -5,  -5, -60, -30],
            [  20,  -5,  10,  10,  -5,  20],
            [  20,  -5,  10,  10,  -5,  20],
            [-30, -60,  -5,  -5, -60, -30],
            [ 150, -30,  20,  20, -30, 150]
        ])

        best_move = moves[0]
        max_score = -float('inf')

        for r, c in moves:
            # Score = Square Weight + (Number of Flips * 1)
            # Lowered flip weight to emphasize positioning over bulk flipping
            
            sim_game = Game(self.size)
            sim_game.board = game.board.copy()
            
            before_count = np.sum(sim_game.board == player)
            sim_game.make_move(r, c, player)
            after_count = np.sum(sim_game.board == player)
            
            flips = after_count - before_count
            score = weights[r, c] + (flips * 1)
            
            if score > max_score:
                max_score = score
                best_move = (r, c)
                
        return best_move

    def play_games(self, count=1):
        for g_id in range(count):
            game = Game(self.size)
            turns = []
            if count <= 10: # Only print for small counts
                print(f"=== NEW SMART TOURNAMENT GAME: {g_id + 1} ===")
            
            current_player = 1 # Black
            
            while True:
                moves = game.get_valid_moves(current_player)

                if not moves:
                    if not game.get_valid_moves(-current_player):
                        break
                    current_player = -current_player
                    continue

                turns.append((current_player, game.board.copy()))
                
                if current_player == 1: # Smart Agent (Black)
                    r, c = self.get_smart_move(game, current_player)
                else: # Random Rival (White)
                    r, c = random.choice(moves)
                    
                game.make_move(r, c, current_player)
                current_player = -current_player
            
            winner = self._get_winner(game)
            self.total_games += 1
            if winner == 1:
                self.black_wins += 1
            elif winner == -1:
                self.white_wins += 1
            else:
                self.draws += 1
                
            self._process_history(g_id, turns, winner)

        if self.total_games > 0:
            win_rate_black = (self.black_wins / self.total_games) * 100
            print("\n=== SMART TOURNAMENT SUMMARY ===")
            print(f"Total Games:  {self.total_games}")
            print(f"Black Wins:   {self.black_wins}")
            print(f"White Wins:   {self.white_wins}")
            print(f"Draws:        {self.draws}")
            print(f"Black Winrate: {win_rate_black:.2f}%")
            print("================================\n")
