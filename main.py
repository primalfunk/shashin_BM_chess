from board import Board
import chess
import chess.svg
from evaluate import Evaluator
import os
from search import Searcher
import sys
import webbrowser

class UCHEngine:
    def __init__(self):
        self.board = Board()
        self.searcher = Searcher()
        self.evaluator = Evaluator()

    def run(self):
        while True:
            command = input()
            if command == "uci":
                self.uci()
            elif command == "isready":
                self.is_ready()
            elif command.startswith("ucinewgame"):
                self.ucinewgame()
            elif command.startswith("position"):
                self.position(command)
            elif command.startswith("go"):
                self.go()
            elif command == "quit":
                break

    def uci(self):
        print("id name BestPlayAI")
        print("id author Shashin / Menard")
        print("uciok")

    def is_ready(self):
        print("readyok")

    def ucinewgame(self):
        self.board = Board()

    def position(self, command):
        parts = command.split(" ")
        if parts[1] == "startpos":
            self.board.set_fen(chess.STARTING_FEN)
            movelist = parts[3:]  # assumes 'moves' is always the third element
        else:
            fen = " ".join(parts[1:7])
            self.board.set_fen(fen)
            movelist = parts[8:]

        for move_uci in movelist:
            move = chess.Move.from_uci(move_uci)
            self.board.make_move(move)

    def go(self):
        depth = 4  # or parse this from the 'go' command parameters
        best_move = self.searcher.find_best_move(self.board, depth)
        evaluation = self.evaluator.evaluate_position(self.board.board)  # Pass the correct chess.Board object
        print(f"bestmove {best_move.uci()}")

        # Optionally output the evaluation for the current board position
        print(f"info score cp {int(evaluation * 100)}")  # Convert to centipawns for standard UCI output
        # Show the board using SVG in the default browser
        self.show_board(self.board.board)  # Pass the correct chess.Board object

    def show_board(self, board):
        # Generate the SVG of the board
        board_svg = chess.svg.board(board)  # Ensure this 'board' is a python-chess Board object
        # Write it to an SVG file
        with open("chess_board.svg", "w") as f:
            f.write(board_svg)
        # Open the SVG file with the default web browser
        webbrowser.open("file://" + os.path.realpath("chess_board.svg"))

if __name__ == "__main__":
    engine = UCHEngine()
    engine.run()

