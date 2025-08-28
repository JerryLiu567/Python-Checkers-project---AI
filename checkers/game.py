import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, YELLOW
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self._draw_forced_capture_indicators() # 繪製黃色提示圈
        self.draw_valid_moves(self.valid_moves) # 只在選擇棋子後繪製藍色點
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        # --- 新增變數，儲存當前回合所有合法移動 ---
        self.turn_valid_moves = self.board.get_all_player_moves(self.turn)

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        # 如果已經選擇了棋子，就嘗試移動
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.valid_moves = {} # 取消選擇後，清除藍點
                self.select(row, col) # 重新執行 select，嘗試選擇新棋子
        
        piece = self.board.get_piece(row, col)
        
        # --- 修改後的選擇邏輯 ---
        # 檢查點擊的棋子是否在當前回合有合法移動的棋子列表中
        if piece != 0 and piece in self.turn_valid_moves:
            self.selected = piece
            # 取得這個棋子的移動，並存起來以便繪製藍點
            self.valid_moves = self.turn_valid_moves[piece]
            return True
            
        return False

    def _move(self, row, col):
        # 檢查目標位置是否在目前選中棋子的合法移動中
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        # moves 的格式為: { (row, col): [skipped] }
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    # --- 新增方法：繪製黃色提示圈 ---
    def _draw_forced_capture_indicators(self):
        """
        如果存在必須吃子的棋子，用黃色圈標示出來。
        """
        # self.turn_valid_moves 的格式是 {piece: moves}
        # 我們只需要 piece 物件
        pieces_with_moves = self.turn_valid_moves.keys()
        
        # 檢查這些移動是否是「吃子」移動
        is_capture_turn = False
        for moves in self.turn_valid_moves.values():
            for skipped in moves.values():
                if skipped:
                    is_capture_turn = True
                    break
            if is_capture_turn:
                break
        
        # 如果是必須吃子的回合，才畫黃圈
        if is_capture_turn:
            for piece in pieces_with_moves:
                radius = SQUARE_SIZE//2 - 5
                # 在棋子外圍畫一個黃色的圓圈
                pygame.draw.circle(self.win, YELLOW, (piece.x, piece.y), radius, 3)


    def change_turn(self):
        self.selected = None
        self.valid_moves = {} # 換邊時清除藍點
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        
        # 為新回合計算所有合法的移動
        self.turn_valid_moves = self.board.get_all_player_moves(self.turn)

    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.change_turn()