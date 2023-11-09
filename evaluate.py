import chess
import chess.svg
import logging
import os
import webbrowser

# Configure logging
logging.basicConfig(filename='debugging.log',
                    filemode='w',
                    format='%(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

# Create logger
logger = logging.getLogger('ChessEvalLogger')

class Evaluator:
    def __init__(self):
        # Piece values dictionary for dynamic piece weighting
        self.piece_values = {'P': 1, 'N': 3, 'B': 3.25, 'R': 5, 'Q': 9, 'K': 0}

    # Calculate material for a given side
    def calculate_material(self, board, side):
        material_sum = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            num_pieces = len(board.pieces(piece_type, side))
            piece_symbol = chess.piece_name(piece_type).upper()
            piece_value = self.piece_values[piece_symbol[0]]
            material_sum += num_pieces * piece_value
            # Log the count and value of each piece type
        # Log the final material sum for the side
        return material_sum

    # Calculate material ratio, white material divided by black material
    def material_ratio(self, board):
        white_material = self.calculate_material(board, True)
        black_material = self.calculate_material(board, False)
        m = white_material - black_material
        return m

    # Calculate the number of legal moves for each side
    def time_factor(self, board):
        white_moves = board.legal_moves.count()
        board.push(chess.Move.null())
        black_moves = board.legal_moves.count()
        board.pop()
        t = white_moves - black_moves
        return t

    # Calculate the compactness of the pieces on the board
    def compactness_factor(self, board, side):
        pieces_squares = [square for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).color == side]
        if not pieces_squares:
            return 0
        ranks = [chess.square_rank(square) for square in pieces_squares]
        files = [chess.square_file(square) for square in pieces_squares]
        area = (max(ranks) - min(ranks) + 1) * (max(files) - min(files) + 1)
        k = area / len(pieces_squares)
        return k

    # Calculate the average rank of the pieces, which represents expansion
    def expansion_factor(self, board, side):
        # Calculate the expansion factor for white
        white_squares = [square for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).color == chess.WHITE]
        white_expansion = sum(chess.square_rank(square) + 1 for square in white_squares) / len(white_squares) if white_squares else 0
        # Calculate the expansion factor for black
        black_squares = [square for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).color == chess.BLACK]
        black_expansion = sum(8 - chess.square_rank(square) for square in black_squares) / len(black_squares) if black_squares else 0
        if board.turn == chess.WHITE:
            return white_expansion - black_expansion
        else:
            return black_expansion - white_expansion

    # Calculate the safety factor around the king with updated logic
    def get_king_safety(self, board, color):
        king_square = board.king(color)
        safety_squares = 0
        total_squares = 0
        if king_square is not None:
            king_neighbors = [
                square for square in chess.SQUARES if chess.square_distance(king_square, square) == 1
            ]
            for square in king_neighbors:
                attackers = board.attackers(color, square)
                defenders = board.attackers(not color, square)
                if board.is_attacked_by(color, square):
                    safety_squares += 1
                if not board.is_attacked_by(not color, square):
                    total_squares += 1
            safety_factor = safety_squares / total_squares if total_squares > 0 else 0
        else:
            safety_factor = 0

        return safety_factor

    # Integrate all the factors into an overall position evaluation
    def evaluate_position(self, board):
        # Material ratio evaluation
        m = self.material_ratio(board)
        # Time factor evaluation
        t = self.time_factor(board)
        logger.debug(f"Time Factor: {'White' if t > 0 else 'Black'} advantage of {abs(t):.2f}")
        # Compactness factors for white and black
        k_white = self.compactness_factor(board, True)
        k_black = self.compactness_factor(board, False)
        logger.debug(f"Compactness Factor: White - {k_white:.2f}, Black - {k_black:.2f}")
        # Expansion factors for white and black
        e_white = self.expansion_factor(board, True)
        e_black = self.expansion_factor(board, False)
        logger.debug(f"Expansion Factor: White - {e_white:.2f}, Black - {e_black:.2f}")
        # King safety factors for white and black
        s_white = self.get_king_safety(board, True)
        s_black = self.get_king_safety(board, False)
        logger.debug(f"King Safety Factor: White - {s_white:.2f}, Black - {s_black:.2f}")
        # Calculate factors difference or ratio as needed for evaluation
        k = k_white - k_black
        e = e_white / e_black if e_black != 0 else 0  # Avoid division by zero
        s = s_white - s_black
        # Log each factor to see which one is non-zero
        weighted_score = (m + t + k + e + s) / 5  # Normalize the score by the number of factors
        # Adjust the score to ensure 0 is even, positive is white's advantage, negative is black's.
        adjusted_score = weighted_score if board.turn else -weighted_score
        logger.debug(f"Adjusted Weighted Score: {adjusted_score:.2f} ({'White' if board.turn else 'Black'} to move)")

        return adjusted_score

