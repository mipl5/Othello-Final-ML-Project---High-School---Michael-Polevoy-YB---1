from smart_tournament import SmartTournament
from tournament import Tournament

def main():
    t = SmartTournament(size=6, discount=0.9)
    #t = Tournament(size=6, discount=0.9)
    t.play_games(50_000)
    t.export_csv("othello_training_data.csv")

if __name__ == "__main__":
    main()