from copy import deepcopy
import pygame
from checkers.constants import RED, WHITE
from minmax.evaluation import evaluate_board

def alphabeta(position, depth, alpha, beta, max_player, game):
    if depth == 0 or position.winner() != None:
        return evaluate_board(position), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move_board in get_all_moves(position, WHITE, game):
            evaluation = alphabeta(move_board, depth - 1, alpha, beta, False, game)[0]
            
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move_board
            
            alpha = max(alpha, evaluation)
            
            if beta <= alpha:
                break
                
        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None
        for move_board in get_all_moves(position, RED, game):
            evaluation = alphabeta(move_board, depth - 1, alpha, beta, True, game)[0]
            
            if evaluation < minEval:
                minEval = evaluation
                best_move = move_board

            beta = min(beta, evaluation)

            if beta <= alpha:
                break

        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
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
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves