from fastapi import FastAPI
from pydantic import BaseModel
from board import Board
from constants import *

app = FastAPI()

class GameState(BaseModel):
    board: list[list[int]]
    current_player: int
    valid_moves: list[tuple[int, int]]
    game_over: bool
    winner: int | None

@app.post("/new_game")
def new_game():
    board = Board()
    return GameState(
        board=board.board,
        current_player=board.current_player,
        valid_moves=board.get_valid_moves(),
        game_over=board.is_game_over(),
        winner=board.get_winner()
    )

@app.post("/make_move")
def make_move(move: tuple[int, int], current_board: list[list[int]], current_player: int):
    board = Board(current_board, current_player)
    if board.is_valid_move(move):
        board.make_move(move)
        return GameState(
            board=board.board,
            current_player=board.current_player,
            valid_moves=board.get_valid_moves(),
            game_over=board.is_game_over(),
            winner=board.get_winner()
        )
    else:
        return {"error": "Invalid move"}