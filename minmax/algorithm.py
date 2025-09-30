import random
from copy import deepcopy
import pygame
from checkers.constants import PIECE_COLOR_A, PIECE_COLOR_B, ROWS, COLS
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

# (在 minmax/algorithm.py 中)
def get_all_moves(board, color, game):
    """
    產生指定顏色方所有合法的下一步棋盤狀態列表。
    這個函式現在包含了完整的模擬邏輯，包括升王。
    """
    moves = []
    
    # 取得所有合法的移動 (已包含遇子必吃規則)
    all_valid_moves = board.get_all_player_moves(color)

    for piece, valid_moves in all_valid_moves.items():
        for move, skip in valid_moves.items():
            # 為每一次可能的移動建立一個棋盤副本
            temp_board = deepcopy(board)
            # 在副本上取得對應的棋子
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            
            # 執行模擬移動（移除多餘的 game 參數）
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)

    return moves

# --- 我們將模擬邏輯重新封裝回 simulate_move 函式，並補上升王檢查 ---
def simulate_move(piece, move, board, skip):
    """
    在給定的棋盤上模擬一次移動，並回傳移動後的新棋盤。
    這個函式現在包含了升王檢查，專供 AI 使用。
    """
    # 在棋盤上移動棋子
    board.board[piece.row][piece.col], board.board[move[0]][move[1]] = board.board[move[0]][move[1]], board.board[piece.row][piece.col]
    piece.move(move[0], move[1])

    # --- 核心修正：在模擬中加入升王邏輯 ---
    row, col = move
    # 檢查是否到達底線
    if row == ROWS - 1 or row == 0:
        if not piece.king:
            piece.make_king()
            # 更新對應顏色的國王數量
            if piece.color == PIECE_COLOR_B:
                board.white_kings += 1
            else:
                board.red_kings += 1
    
    # 如果這次移動是吃子
    if skip:
        # 在新棋盤中找到被吃的棋子並移除
        skipped_in_new_board = [board.get_piece(p.row, p.col) for p in skip]
        board.remove(skipped_in_new_board)

    return board