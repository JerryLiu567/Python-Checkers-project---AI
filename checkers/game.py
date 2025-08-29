import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, YELLOW
from checkers.board import Board

class Game:
    def __init__(self, win, game_mode):
        self.win = win
        self.game_mode = game_mode
        self._init()
    
    def update(self):
        self.board.draw(self.win)
        self._draw_forced_capture_indicators()
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.turn_valid_moves = self.board.get_all_player_moves(self.turn)

    def winner(self):
        # --- 修改部分：整合所有勝利/和局條件 ---
        
        # 1. 檢查 board 物件的條件 (吃完棋子 or 50步和局)
        board_winner = self.board.winner()
        if board_winner is not None:
            return board_winner

        # 2. 檢查當前回合的玩家是否無路可走
        if not self.turn_valid_moves:
            # 如果輪到紅方但沒路走，白方贏
            if self.turn == RED:
                return "WHITE"
            # 如果輪到白方但沒路走，紅方贏
            else:
                return "RED"
        
        return None

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.valid_moves = {}
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        
        if piece != 0 and piece in self.turn_valid_moves:
            self.selected = piece
            self.valid_moves = self.turn_valid_moves[piece]
            return True
            
        return False

    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            moved_piece = self.selected
            
            # 這裡不呼叫 board.move，因為吃子後可能不會增加計數器
            # 在下面根據情況處理
            self.board.board[moved_piece.row][moved_piece.col], self.board.board[row][col] = self.board.board[row][col], self.board.board[moved_piece.row][moved_piece.col]
            moved_piece.move(row, col)

            skipped = self.valid_moves.get((row, col))
            
            promoted_to_king = False
            if row == ROWS - 1 or row == 0:
                if not moved_piece.king:
                    moved_piece.make_king()
                    promoted_to_king = True
                    if moved_piece.color == WHITE:
                        self.board.white_kings += 1
                    else:
                        self.board.red_kings += 1
            
            if skipped:
                self.board.remove(skipped) # remove 內部會重置計數器
                
                new_piece = self.board.get_piece(row, col)
                
                new_moves = self.board.get_valid_moves(new_piece)
                capture_moves = {m: s for m, s in new_moves.items() if s}

                if capture_moves:
                    self.selected = new_piece
                    self.valid_moves = capture_moves
                    self.turn_valid_moves = {new_piece: capture_moves}
                    return True
            
            # --- 修改部分：只有在非吃子移動時才更新計數器 ---
            if not skipped:
                if promoted_to_king:
                    self.board.moves_since_last_capture_or_king = 0
                else:
                    self.board.moves_since_last_capture_or_king += 1
                
            self.change_turn()
            return True

        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def _draw_forced_capture_indicators(self):
        if self.game_mode == 'pva' and self.turn == WHITE:
            return

        pieces_with_moves = self.turn_valid_moves.keys()
        
        is_capture_turn = False
        for moves in self.turn_valid_moves.values():
            for skipped in moves.values():
                if skipped:
                    is_capture_turn = True
                    break
            if is_capture_turn:
                break
        
        if is_capture_turn:
            for piece in pieces_with_moves:
                radius = SQUARE_SIZE//2 - 5
                pygame.draw.circle(self.win, YELLOW, (piece.x, piece.y), radius, 3)

    def change_turn(self):
        self.selected = None
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        
        self.turn_valid_moves = self.board.get_all_player_moves(self.turn)

    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.change_turn()