import chess
import chess.pgn

from minimax import get_best_move

DEPTH = 5

bot_a_PST_weighting_factor = 1
bot_b_PST_weighting_factor = 1

bot_a_board_vision_weight = 0.2
bot_b_board_vision_weight = 0

board = chess.Board()

while not board.is_game_over():
    if board.turn == chess.WHITE:
        best_move = get_best_move(board, DEPTH, is_maximising=True, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=bot_a_PST_weighting_factor, BOARD_VISION_WEIGHT=bot_a_board_vision_weight)
    else:
        best_move = get_best_move(board, DEPTH, is_maximising=False, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=bot_b_PST_weighting_factor, BOARD_VISION_WEIGHT=bot_b_board_vision_weight)

    board.push(best_move)
    print(board)

print("Game Over, Result: ", board.result())

game = chess.pgn.Game.from_board(board)
print(game)