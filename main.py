import sys
import random
import chess
from minimax import get_best_move

def main():
    board = chess.Board()
    # Infinite loop to read commands from the GUI/Bridge
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            continue
            
        tokens = line.split()
        command = tokens[0]
        
        if command == "uci":
            print("id name LucaChessBot", flush=True)
            print("id author Luca Tilyard", flush=True)

            print("uciok", flush=True)
            
        elif command == "isready":
            print("readyok", flush=True)

        elif command == "setoption":
            # Silently accept any configuration options the GUI sends
            pass
            
        elif command == "position":
            # Handle standard starting position
            if "startpos" in tokens:
                board.reset()
                if "moves" in tokens:
                    moves_index = tokens.index("moves")
                    for move in tokens[moves_index + 1:]:
                        board.push_uci(move)
                        
            # Handle custom starting positions (FEN)
            elif "fen" in tokens:
                fen_start = tokens.index("fen") + 1
                if "moves" in tokens:
                    moves_index = tokens.index("moves")
                    fen = " ".join(tokens[fen_start:moves_index])
                    board.set_fen(fen)
                    for move in tokens[moves_index + 1:]:
                        board.push_uci(move)
                else:
                    fen = " ".join(tokens[fen_start:])
                    board.set_fen(fen)

        elif command == "go":
            # This is where your engine's logic goes. 
            # For now, it just picks a random legal move.
            legal_moves = list(board.legal_moves)
            if legal_moves:
                if board.turn == chess.WHITE:
                    best_move = get_best_move(board, 6, True)
                else:
                    best_move = get_best_move(board, 6, False)

                print(f"bestmove {best_move.uci()}", flush=True)
            else:
                # Fallback if the game is already over
                print("bestmove 0000", flush=True)
                
        elif command == "quit":
            break

if __name__ == "__main__":
    main()