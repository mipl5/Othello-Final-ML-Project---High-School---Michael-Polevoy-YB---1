from tournament import Tournament

def main():
    tournament = Tournament()
    tournament.play_games(100_000)
    tournament.print_tournament_results()
    tournament.save_to_csv()

if __name__ == "__main__":
    main()