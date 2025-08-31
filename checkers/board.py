import pygame
from checkers.constants import (BOARD_COLOR_DARK, BOARD_COLOR_LIGHT, ROWS, COLS, SQUARE_SIZE, 
                                PIECE_COLOR_A, PIECE_COLOR_B)
from checkers.piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.moves_since_last_capture_or_king = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BOARD_COLOR_DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BOARD_COLOR_LIGHT, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        # This method is now only called internally by Game._move, which handles the main logic
        # self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        # piece.move(row, col)
        pass # The logic is now in Game._move to handle move_event return

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, PIECE_COLOR_B))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, PIECE_COLOR_A))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win, selected_piece=None):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    is_selected = (piece == selected_piece)
                    piece.draw(win, is_selected)

    def remove(self, pieces):
        for piece in pieces:
            if self.board[piece.row][piece.col] != 0:
                if piece.color == PIECE_COLOR_A:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
                self.board[piece.row][piece.col] = 0
        
        self.moves_since_last_capture_or_king = 0
    
    def winner(self):
        if self.red_left <= 0:
            return PIECE_COLOR_B
        elif self.white_left <= 0:
            return PIECE_COLOR_A
        
        if self.moves_since_last_capture_or_king >= 50:
            return "DRAW"
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == PIECE_COLOR_A or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == PIECE_COLOR_B or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def get_all_player_moves(self, color):
        all_moves_for_player = {}
        capture_moves_exist = False

        for piece in self.get_all_pieces(color):
            valid_moves = self.get_valid_moves(piece)
            if not valid_moves:
                continue
            
            for move, skipped in valid_moves.items():
                if skipped:
                    capture_moves_exist = True
                    break
            
            all_moves_for_player[piece] = valid_moves

        if capture_moves_exist:
            final_moves = {}
            for piece, moves in all_moves_for_player.items():
                capture_only = {move: skipped for move, skipped in moves.items() if skipped}
                if capture_only:
                    final_moves[piece] = capture_only
            return final_moves
        
        else:
            return all_moves_for_player

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves