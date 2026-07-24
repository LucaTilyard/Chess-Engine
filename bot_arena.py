from minimax import get_best_move
import chess
import chess.pgn

class Bot:
    def __init__(self, depth, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=1, points = 0):
        self.depth = depth
        self.PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR = PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR
        self.BOARD_VISION_WEIGHT = BOARD_VISION_WEIGHT
        self.points = points

    def make_move(self, board, is_maximising):
        best_move = get_best_move(board, self.depth, is_maximising, self.PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR, self.BOARD_VISION_WEIGHT)
        return best_move

# 20 bot round robin tournament, 1 point for a win, 0.5 for a draw, 0 for a loss. Each bot plays each other bot once as white and once as black. The bot with the most points at the end of the tournament wins.

def chess_match(white, black): 
    board = chess.Board()
    print(f"Match between {white.__class__.__name__} (White) and {black.__class__.__name__} (Black)")
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            best_move = white.make_move(board, True) 
        else:
            best_move = black.make_move(board, False)

        board.push(best_move)
    if board.result() == "1-0":
        white.points += 1
    elif board.result() == "0-1":
        black.points += 1
    else:
        white.points += 0.5
        black.points += 0.5

    print("PNG of the game:")
    game = chess.pgn.Game.from_board(board)
    print(game)

def display_tournament_table(bots):
    # Order bots by points
    bots.sort(key=lambda x: x.points, reverse=True)

    # Print the tournament table, bot name | points | weighted PST factor | weighted board vision factor
    print("Tournament Table:")
    print("Bot Name | Points | Weighted PST Factor | Weighted Board Vision Factor")
    for bot in bots:
        print(f"{bot.__class__.__name__} | {bot.points} | {bot.PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR} | {bot.BOARD_VISION_WEIGHT}") 

    return 1

bot1 = Bot(depth=3, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.2)
bot2 = Bot(depth=3, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.25)
bot3 = Bot(depth=3, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.15)
bot4 = Bot(depth=3, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.3)
bot5 = Bot(depth=3, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.7)
bot6 = Bot(depth=3, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.3)
bot7 = Bot(depth=4, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.4)
bot8 = Bot(depth=4, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.6)
bot9 = Bot(depth=4, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.7)
bot10 = Bot(depth=4, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=1, BOARD_VISION_WEIGHT=0.9)

compeating_bots = [bot1, bot2, bot3, bot4]

for bot in compeating_bots:
    bot.points = 0

for i in range(len(compeating_bots)):
    # "Home" games (White)
    for j in range(i + 1, len(compeating_bots)):
        chess_match(compeating_bots[i], compeating_bots[j])

    # "Away" games (Black)
    for j in range(i + 1, len(compeating_bots)):
        chess_match(compeating_bots[j], compeating_bots[i])

display_tournament_table(compeating_bots)



