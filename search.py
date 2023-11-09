from board import Board
from evaluate import Evaluator
import chess

class Searcher:
    def __init__(self) -> None:
        self.ev = Evaluator()
    
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """
        Perform the minimax algorithm to find the best move.

        :param board: the current board state as a chess.Board object.
        :param depth: how deep the search should go, in half-moves.
        :param alpha: the best score that the maximizing player is assured of, starts with negative infinity.
        :param beta: the best score that the minimizing player is assured of, starts with positive infinity.
        :param is_maximizing: a boolean indicating if the current move is by the maximizing player.
        :return: the best score for the current player.
        """
        
        # Base case: maximum depth reached or game is over.
        if depth == 0 or board.is_game_over():
            return self.ev.evaluate_position(board)

        if is_maximizing:
            max_eval = float('-inf')  # Initialize the best score for the maximizing player.
            for move in board.legal_moves:  # Iterate over all legal moves.
                board.push(move)  # Make the move on the board.
                eval = self.minimax(board, depth - 1, alpha, beta, False)  # Recursively call minimax for the minimizing player.
                board.pop()  # Undo the move.
                max_eval = max(max_eval, eval)  # Update the best score if a better score is found.
                alpha = max(alpha, eval)  # Alpha-beta pruning step.
                if beta <= alpha:
                    break  # Break out of the loop if a pruning condition is met.
            return max_eval
        else:
            min_eval = float('inf')  # Initialize the best score for the minimizing player.
            for move in board.legal_moves:  # Iterate over all legal moves.
                board.push(move)  # Make the move on the board.
                eval = self.minimax(board, depth - 1, alpha, beta, True)  # Recursively call minimax for the maximizing player.
                board.pop()  # Undo the move.
                min_eval = min(min_eval, eval)  # Update the best score if a better score is found.
                beta = min(beta, eval)  # Alpha-beta pruning step.
                if beta <= alpha:
                    break  # Break out of the loop if a pruning condition is met.
            return min_eval

    def find_best_move(self, board, depth):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in board.get_legal_moves():
            board.make_move(move)
            move_value = self.minimax(board, depth - 1, alpha, beta, False)
            board.undo_move()

            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move
