from copy import deepcopy
import pygame
from checkers.constants import RED, WHITE, YELLOW

def minmax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float("-inf")
        best_move = None
        # --- 修改部分：讓 AI 遵守遇子必吃規則 ---
        for move_board in get_all_moves(position, WHITE, game):
            evaluation = minmax(move_board, depth-1, False ,game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move_board

        return maxEval, best_move

    else:
        minEval = float("inf")
        best_move = None
        # --- 修改部分：讓 AI 遵守遇子必吃規則 ---
        for move_board in get_all_moves(position, RED, game):
            evaluation = minmax(move_board, depth-1, True ,game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move_board

        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board, color, game):
    moves = []
    
    # --- 核心修改 ---
    # 直接呼叫 board 的方法，取得所有遵守「遇子必吃」規則的移動
    # all_valid_moves 的格式為: { piece_object: { (row, col): [skipped] } }
    all_valid_moves = board.get_all_player_moves(color)

    # 遍歷所有有合法移動的棋子
    for piece, valid_moves in all_valid_moves.items():
        # 遍歷該棋子的所有合法移動
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves