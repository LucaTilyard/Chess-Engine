import time
import chess
import chess.pgn
from minimax import get_best_move 
from datetime import datetime
from evaluation_function import PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR
import os

depth = 6

total_time = 0
positions_evaluated = 0

total_time_2 = 0
positions_evaluated_2 = 0

total_time_3 = 0
positions_evaluated_3 = 0
accuracy = 0

# Write in specs string any information about the configuration of the engine to be stored with the results in the benchmarks results. 

specs_string = "Using A/B Pruning, MVV-LVA, Transposition Table, caceing and PST evaluation function"

# Amature game played between two humans < 1000 ELO 
with open("example-games/example-amature.pgn") as pgn:
    game = chess.pgn.read_game(pgn)

    while game is not None:
        board = game.board()
        
        for move in game.mainline_moves():
            
            is_white_turn = (board.turn == chess.WHITE)
            
            start_time = time.perf_counter()
            best_move = get_best_move(board, depth, is_maximising=is_white_turn)
            end_time = time.perf_counter()
            
            move_time = end_time - start_time
            total_time += move_time
            positions_evaluated += 1
            
            board.push(move)

        # Read the next game in the file
        game = chess.pgn.read_game(pgn)

print(f"\n--- Benchmark Complete ---")
print(f"Evaluated {positions_evaluated} positions.")
print(f"Total time: {total_time:.2f} seconds.")
if positions_evaluated > 0:
    print(f"Average time per move: {total_time / positions_evaluated:.2f} seconds.")


# Repeat process with long grand master game played between two humans > 2500 ELO
with open("example-games/MCvHN.pgn") as pgn:
    game = chess.pgn.read_game(pgn)

    while game is not None:
        board = game.board()
        
        for move in game.mainline_moves():
            
            is_white_turn = (board.turn == chess.WHITE)
            
            start_time = time.perf_counter()
            best_move = get_best_move(board, depth, is_maximising=is_white_turn)
            end_time = time.perf_counter()
            
            move_time = end_time - start_time
            total_time_2 += move_time
            positions_evaluated_2 += 1
            
            board.push(move)

        # Read the next game in the file
        game = chess.pgn.read_game(pgn)

print(f"\n--- Benchmark Complete ---")
print(f"Evaluated {positions_evaluated_2} positions.")
print(f"Total time: {total_time_2:.2f} seconds.")
if positions_evaluated_2 > 0:
    print(f"Average time per move: {total_time_2 / positions_evaluated_2:.2f} seconds.")

# reasonably accuracy game played between two humans > 2500 ELO, where the engine is expected to play the exact moves of the game. The engine should be able to play the exact moves of the game with 100% accuracy, and the time taken for each move should be recorded. The total time taken for the game should also be recorded.
# This game shoudl also record accuracy of moves

with open("example-games/MCvS.pgn") as pgn:
    game = chess.pgn.read_game(pgn)

    while game is not None:
        board = game.board()
        
        for move in game.mainline_moves():
            
            is_white_turn = (board.turn == chess.WHITE)
            
            start_time = time.perf_counter()
            best_move = get_best_move(board, depth, is_maximising=is_white_turn)
            end_time = time.perf_counter()
            
            move_time = end_time - start_time
            total_time_3 += move_time
            positions_evaluated_3 += 1
            
            if best_move == move:
                accuracy += 1
            
            board.push(move)

        # Read the next game in the file
        game = chess.pgn.read_game(pgn)

print(f"\n--- Benchmark Complete ---")
print("compiling report...")
# Benchmark Report: 
# Create a txt file and put in results for both games, including total time, average time per move, and number of positions evaluated.
if not os.path.exists("benchmarks"):
    os.makedirs("benchmarks")

with open(f"benchmarks/benchmark_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w") as f:
    f.write("--- Benchmark Results ---\n\n")

    f.write("Configuration:\n")
    f.write(f"Depth: {depth}\n")
    f.write(f"Piece-Square Tensor Weighting Factor: {PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR}\n")
    f.write(specs_string + "\n\n")
    f.write("\n ------------------------- \n\n")

    f.write("Amateur Game (<1000 ELO):\n")
    f.write(f"Evaluated {positions_evaluated} positions.\n")
    f.write(f"Total time: {total_time:.2f} seconds.\n")
    if positions_evaluated > 0:
        f.write(f"Average time per move: {total_time / positions_evaluated:.2f} seconds.\n")

    f.write("\n ------------------------- \n")
    
    f.write("\nGrandmaster Game (>2500 ELO):\n")
    f.write(f"Evaluated {positions_evaluated_2} positions.\n")
    f.write(f"Total time: {total_time_2:.2f} seconds.\n")
    if positions_evaluated_2 > 0:
        f.write(f"Average time per move: {total_time_2 / positions_evaluated_2:.2f} seconds.\n")

    f.write("\n ------------------------- \n")


    f.write("\nHigh Accuracy Game (>2500 ELO):\n")
    f.write(f"Evaluated {positions_evaluated_3} positions.\n")
    f.write(f"Total time: {total_time_3:.2f} seconds.\n")
    if positions_evaluated_3 > 0:
        f.write(f"Average time per move: {total_time_3 / positions_evaluated_3:.2f} seconds.\n")
        f.write(f"Accuracy: {accuracy / positions_evaluated_3 * 100:.2f}%\n")

print("Benchmark report generated successfully.")