from tournament import Tournament

def main():
    t = Tournament(size=6, discount=0.9)
    t.play_games(50_000)
    t.export_csv()

if __name__ == "__main__":
    main()