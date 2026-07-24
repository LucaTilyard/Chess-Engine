import chess
import math

MVV_LVA_VALUES = [0, 1, 3, 3, 5, 9, 1000]

PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR = 1

PAWN_PST = [
     0,  0,  0,  0,  0,  0,  0,  0, # Rank 1 (Promotion rank for Black)
     5, 10, 10,-20,-20, 10, 10,  5, # Rank 2
     5, -5,-10,  0,  0,-10, -5,  5, # Rank 3
     0,  0,  0, 20, 20,  0,  0,  0, # Rank 4
     5,  5, 10, 25, 25, 10,  5,  5, # Rank 5
    10, 10, 20, 30, 30, 20, 10, 10, # Rank 6
    50, 50, 50, 50, 50, 50, 50, 50, # Rank 7
     0,  0,  0,  0,  0,  0,  0,  0  # Rank 8 (Promotion rank for White)
]

KNIGHT_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50, # Rank 1
    -40,-20,  0,  5,  5,  0,-20,-40, # Rank 2
    -30,  5, 10, 15, 15, 10,  5,-30, # Rank 3
    -30,  0, 15, 20, 20, 15,  0,-30, # Rank 4
    -30,  5, 15, 20, 20, 15,  5,-30, # Rank 5
    -30,  0, 10, 15, 15, 10,  0,-30, # Rank 6
    -40,-20,  0,  0,  0,  0,-20,-40, # Rank 7
    -50,-40,-30,-30,-30,-30,-40,-50  # Rank 8
]

BISHOP_PST = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_PST = [
     0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     5, 10, 10, 10, 10, 10, 10,  5, # The "Pig" on the 7th rank
     0,  0,  0,  0,  0,  0,  0,  0
]

QUEEN_PST = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_PST = [ # Specifically middle game 
     20, 30, 10,  0,  0, 10, 30, 20, # Rank 1: King safety (G1/C1 for castling)
     20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30
]

PST = {
    chess.PAWN: PAWN_PST,
    chess.KNIGHT: KNIGHT_PST,
    chess.BISHOP: BISHOP_PST,
    chess.ROOK: ROOK_PST,
    chess.QUEEN: QUEEN_PST,
    chess.KING: KING_PST
}

MATERIAL_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000 
}

def evaluate_board(board, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1): 

    # Avoiding/Achiving chackmake is the overall goal and thus is given highest priority.
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -math.inf  # Black wins
        else:
            return math.inf  # White wins

    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0  # Draw

    # Initialise score
    total_score = 0

    for piece_type in range(chess.PAWN, chess.KING + 1):
        # Base Material Score
        total_score += len(board.pieces(piece_type, chess.WHITE)) * MATERIAL_VALUES[piece_type]
        total_score -= len(board.pieces(piece_type, chess.BLACK)) * MATERIAL_VALUES[piece_type]

        # Positional Bonuses (PST)
        if piece_type in PST:
            for square in board.pieces(piece_type, chess.WHITE):
                total_score += PST[piece_type][square] * PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR
                
            for square in board.pieces(piece_type, chess.BLACK):
                # Mirror the square index so Black uses the table from its own perspective
                mirrored_square = chess.square_mirror(square)
                total_score -= PST[piece_type][mirrored_square] * PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR
    return total_score
