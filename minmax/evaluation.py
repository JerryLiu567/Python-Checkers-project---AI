from checkers.constants import PIECE_COLOR_B, PIECE_COLOR_A, ROWS

def evaluate_board(board):
    """
    評估一個棋盤狀態的分數。
    分數 > 0 表示對藍方(AI)有利。
    分數 < 0 表示對紅方(玩家)有利。
    """
    king_weight = 2
    
    score = (board.white_left - board.red_left) + \
            (board.white_kings * (king_weight - 1) - board.red_kings * (king_weight - 1))

    for row_index, row_content in enumerate(board.board):
        for piece in row_content:
            if piece == 0:
                continue

            if piece.color == PIECE_COLOR_B:
                if not piece.king:
                    score += piece.row * 0.1
                if not piece.king and row_index <= 1:
                    score += 0.05
            
            elif piece.color == PIECE_COLOR_A:
                if not piece.king:
                    score -= (ROWS - 1 - piece.row) * 0.1
                if not piece.king and row_index >= ROWS - 2:
                    score -= 0.05
    
    return score