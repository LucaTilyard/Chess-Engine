import chess
import math
import numpy as np
import chess.polyglot
import random
from pathlib import Path
from evaluation_function import evaluate_board, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR


MVV_LVA_VALUES = [0, 1, 3, 3, 5, 9, 1000]


def order_moves(board, moves, tt_best_move=None):
    # Score moves to sort them, improves alpha-beta pruning efficiency.
    # Search in the standard order, checks, captures, promotions, then quiet moves.
    def move_score(move):
        if move == tt_best_move:
            return 10000  # Highest priority for the best move from the transposition table
        score = 0

        # Implement MVV-LVA (Most Valuable Victim - Least Valuable Attacker)

        if board.is_capture(move): # This does not account for en passant, but it is a rare move and thus not worth the complexity to account for it.
            victim_type = board.piece_type_at(move.to_square)
            attacker_type = board.piece_type_at(move.from_square)
            if victim_type and attacker_type:
                score += MVV_LVA_VALUES[victim_type] * 10 - MVV_LVA_VALUES[attacker_type]

        return score

    return sorted(moves, key=move_score, reverse=True)

transposition_table = {}

def minmax(board, depth, alpha, beta, is_maximising, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR): 
    board_hash = board._transposition_key()
    tt_best_move = None

    # Read from cache
    if board_hash in transposition_table:
        tt_entry = transposition_table[board_hash]
        tt_best_move = tt_entry.get('best_move') # Extract the move for ordering
        
        if tt_entry['depth'] >= depth:
            if tt_entry['flag'] == 'EXACT':
                return tt_entry['score']
            elif tt_entry['flag'] == 'LOWERBOUND':
                alpha = max(alpha, tt_entry['score'])
            elif tt_entry['flag'] == 'UPPERBOUND':
                beta = min(beta, tt_entry['score'])
            if alpha >= beta:
                return tt_entry['score']

    if depth == 0 or board.is_game_over(): 
        return evaluate_board(board, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR)

    original_alpha = alpha
    original_beta = beta
    best_move_this_node = None # Track the best move found

    if is_maximising: 
        best_score = -math.inf
        # Pass tt_best_move to the sorter
        for move in order_moves(board, board.generate_pseudo_legal_moves(), tt_best_move):
            board.push(move)

            if board.was_into_check():
                board.pop()
                continue  # Skip illegal moves that put the player into check
            
            score = minmax(board, depth-1, alpha, beta, not is_maximising, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR)
            board.pop()
            
            if score > best_score:
                best_score = score
                best_move_this_node = move # Update best move

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        flag = 'EXACT'
        if best_score <= original_alpha:
            flag = 'UPPERBOUND'
        elif best_score >= beta:
            flag = 'LOWERBOUND'
            
        # Save the best move to the TT
        transposition_table[board_hash] = {'score': best_score, 'depth': depth, 'flag': flag, 'best_move': best_move_this_node}
        return best_score

    else: # Minimising player
        best_score = math.inf 
        for move in order_moves(board, board.generate_pseudo_legal_moves(), tt_best_move):
            board.push(move)

            if board.was_into_check():
                board.pop()
                continue  # Skip illegal moves that put the player into check

            score = minmax(board, depth-1, alpha, beta, not is_maximising, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR)
            board.pop()
            
            if score < best_score:
                best_score = score
                best_move_this_node = move # Update best move

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        flag = 'EXACT'
        if best_score <= alpha:
            flag = 'UPPERBOUND'
        elif best_score >= original_beta:
            flag = 'LOWERBOUND'

        transposition_table[board_hash] = {'score': best_score, 'depth': depth, 'flag': flag, 'best_move': best_move_this_node}
        return best_score

def get_best_move(board, max_depth, is_maximising, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR=PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR):

    # Check if board position is in opening book
    try:
        opening_book = Path(__file__).resolve().with_name("opening-database.bin")
        # opening_book = "/opening-database.bin"
        with chess.polyglot.open_reader(str(opening_book)) as reader:
            entries = list(reader.find_all(board))
            if entries:
                # Pick a move at random from the opening book entries
                chosen_entry = random.choice(entries)
                return chosen_entry.move
                
    except FileNotFoundError:
        print("Opening book file not found. Using minimax instead.")
        # use minimax if board position is not in opening book or if the opening book file is not found
        pass


    # Set first legal move as a fallback
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None # No moves available
    global_best_move = legal_moves[0]

    # Iterative Deepening Loop
    for current_depth in range(1, max_depth + 1):
        best_score = -math.inf if is_maximising else math.inf
        alpha = -math.inf
        beta = math.inf
        
        # Look up the root node in the TT to order moves at depth 1
        board_hash = board._transposition_key()
        tt_best_move = transposition_table.get(board_hash, {}).get('best_move')

        # Order moves using the best move from the previous depth iteration
        ordered_moves = order_moves(board, legal_moves, tt_best_move)

        for move in ordered_moves:
            board.push(move)
            move_score = minmax(board, current_depth - 1, alpha, beta, not is_maximising, PIECE_SQUARE_TENSOR_WEIGHTING_FACTOR)
            board.pop()

            if is_maximising: 
                if move_score > best_score:
                    global_best_move = move 
                    best_score = move_score
                alpha = max(alpha, best_score)

            else: 
                if move_score < best_score:
                    global_best_move = move
                    best_score = move_score
                beta = min(beta, best_score)

    return global_best_move


# IDEAS: 
# - "King boost" - squares surrounding the king are given an boost if covered
# - "Piece coordination" - boost scores if pieces are coordinated, defending each other or attacking together. 
# - Supress king safty and piece coordination in the endgame, as they are less relevant.
# - Have bot target double knight checkmate
# - add itterative deepening to minimax, so it can search deeper if time allows.
# - Implement Ponderinging, so the bot can think on the opponents turn.
# - Deeper book, so the bot can play more opening moves from the book.
# - Threading 
# - truly 100% accurate game in benchmark 
# - PeSTO's Evaluation Function