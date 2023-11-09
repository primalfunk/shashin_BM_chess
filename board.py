import chess

class Board:
    def __init__(self):
        self.board = chess.Board()

    def get_legal_moves(self):
        return list(self.board.legal_moves)

    def make_move(self, move):
        """ Make a move on the board. If the move is illegal, it raises a ValueError. """
        try:
            self.board.push(move)
        except ValueError:
            raise ValueError("Illegal move attempted.")

    def is_game_over(self):
        """ Check if the game is over. """
        return self.board.is_game_over()

    def undo_move(self):
        """ Undo the last move. """
        self.board.pop()

    def get_fen(self):
        """ Get the current board position in FEN notation. """
        return self.board.fen()

    def set_fen(self, fen):
        """ Set the board position from a FEN string. """
        self.board.set_fen(fen)

    # Add any additional helper methods as needed.