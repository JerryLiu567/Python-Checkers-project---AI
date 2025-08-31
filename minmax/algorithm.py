import random
from copy import deepcopy
import pygame
from checkers.constants import PIECE_COLOR_A, PIECE_COLOR_B
from .evaluation import evaluate_board

def alphabeta(position, depth, alpha, beta, max_player, game):
    if depth == 0 or position.winner() is not None:
        return evaluate_board(position), position
    
    if max_player:
        maxEval = float('-inf')
        best_moves = [] 
        
        for move_board in get_all_moves(position, PIECE_COLOR_B, game):
            evaluation = alphabeta(move_board, depth - 1, alpha, beta, False, game)[0]
            
            if evaluation > maxEval:
                maxEval = evaluation
                best_moves = [move_board]
            elif evaluation == maxEval:
                best_moves.append(move_board)

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        
        return maxEval, random.choice(best_moves) if best_moves else (maxEval, None)

    else:
        minEval = float('inf')
        best_move = None
        for move_board in get_all_moves(position, PIECE_COLOR_A, game):
            evaluation = alphabeta(move_board, depth - 1, alpha, beta, True, game)[0]
            
            if evaluation < minEval:
                minEval = evaluation
                best_move = move_board

            beta = min(beta, evaluation)
            if beta <= alpha:
                break

        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    # This is a helper for the old get_all_moves, can be removed if get_all_moves is self-contained
    # For now, let's assume it's still needed by a version of get_all_moves
    if piece is not None:
        board.board[piece.row][piece.col], board.board[move[0]][move[1]] = board.board[move[0]][move[1]], board.board[piece.row][piece.col]
        piece.move(move[0], move[1])

        if skip:
            board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = []
    
    all_valid_moves = board.get_all_player_moves(color)

    for piece, valid_moves in all_valid_moves.items():
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            
            # Direct manipulation for simulation
            new_board = temp_board
            sim_piece = new_board.get_piece(temp_piece.row, temp_piece.col)
            
            new_board.board[sim_piece.row][sim_piece.col], new_board.board[move[0]][move[1]] = new_board.board[move[0]][move[1]], new_board.board[sim_piece.row][sim_piece.col]
            sim_piece.move(move[0], move[1])

            if skip:
                # Need to handle 'skipped' pieces correctly in the copied board
                skipped_in_new_board = [new_board.get_piece(p.row, p.col) for p in skip]
                new_board.remove(skipped_in_new_board)

            moves.append(new_board)

    return moves