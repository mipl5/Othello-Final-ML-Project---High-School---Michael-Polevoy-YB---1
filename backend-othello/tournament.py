import csv
from game import Game

class Tournament:
    def __init__(self):
        self.games_played = 0
        self.agent_wins = 0
        self.rival_wins = 0
        self.draws = 0
        self.game_data = []
        self.boards_dict = {}
    
    def map_board_value(self, value):
        return value

    def update_boards_dict(self):
        
    def play_games(self):
        # ...
    def print_tournament_results(self):
        # ...
    def save_to_csv(self):
        # ...