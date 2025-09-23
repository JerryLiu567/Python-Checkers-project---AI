import pygame
from checkers.constants import (PIECE_COLOR_A, PIECE_COLOR_B, VALID_MOVE_COLOR, SQUARE_SIZE, FORCED_CAPTURE_COLOR, 
                                ROWS, COLS)
from checkers.board import Board

class Game:
    def __init__(self, win, game_mode):
        self.win = win
        self.game_mode = game_mode
        self._init()
    
    def update(self):
        self.board.draw(self.win, self.selected)
        self.draw_valid_moves(self.valid_moves)
        self._draw_forced_capture_indicators()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = PIECE_COLOR_A
        self.valid_moves = {}
        self.turn_valid_moves = self.board.get_all_player_moves(self.turn)

    def winner(self):
        board_winner = self.board.winner()
        if board_winner is not None:
            return board_winner

        if not self.turn_valid_moves:
            return PIECE_COLOR_B if self.turn == PIECE_COLOR_A else PIECE_COLOR_A
        
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
            return result
        
        piece = self.board.get_piece(row, col)
        
        if piece != 0 and piece in self.turn_valid_moves:
            self.selected = piece
            self.valid_moves = self.turn_valid_moves[piece]
            return "selected"
            
        return None

    # (在 Game class 中)
    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            moved_piece = self.selected
            
            # 1. 執行實體移動
            self.board.board[moved_piece.row][moved_piece.col], self.board.board[row][col] = self.board.board[row][col], self.board.board[moved_piece.row][moved_piece.col]
            moved_piece.move(row, col)

            skipped = self.valid_moves.get((row, col))
            
            # 2. 檢查是否升王
            promoted_to_king = False
            if row == ROWS - 1 or row == 0:
                if not moved_piece.king:
                    moved_piece.make_king()
                    promoted_to_king = True
                    if moved_piece.color == PIECE_COLOR_B:
                        self.board.white_kings += 1
                    else:
                        self.board.red_kings += 1
            
            # --- 核心修改：依照優先級決定事件類型 ---
            move_event = None
            if promoted_to_king:
                move_event = "king"      # 最高優先級
            elif skipped:
                move_event = "capture"   # 第二優先級
            else:
                move_event = "move"      # 最低優先級

            # 3. 根據事件更新和局計數器
            if move_event in ["capture", "king"]:
                self.board.moves_since_last_capture_or_king = 0
            else:
                self.board.moves_since_last_capture_or_king += 1

            # 4. 處理吃子和連吃邏輯
            if skipped:
                self.board.remove(skipped)
                new_piece = self.board.get_piece(row, col)
                new_moves = self.board.get_valid_moves(new_piece)
                capture_moves = {m: s for m, s in new_moves.items() if s}

                if capture_moves: # 如果可以連吃
                    self.selected = new_piece
                    self.valid_moves = capture_moves
                    self.turn_valid_moves = {new_piece: capture_moves}
                    return move_event # 回傳本次事件，但不交換回合
            
            # 5. 如果不能連吃或不是吃子，正常交換回合
            self.change_turn()
            return move_event

        return None # 無效移動

    def draw_valid_moves(self, moves):
        if moves:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(VALID_MOVE_COLOR)
            for move in moves:
                row, col = move
                self.win.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def _draw_forced_capture_indicators(self):
        if self.game_mode == 'pva' and self.turn == PIECE_COLOR_B:
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
                pygame.draw.circle(self.win, FORCED_CAPTURE_COLOR, (piece.x, piece.y), radius, 3)

    def change_turn(self):
        self.selected = None
        self.valid_moves = {}
        if self.turn == PIECE_COLOR_A:
            self.turn = PIECE_COLOR_B
        else:
            self.turn = PIECE_COLOR_A
        
        self.turn_valid_moves = self.board.get_all_player_moves(self.turn)

    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.change_turn()