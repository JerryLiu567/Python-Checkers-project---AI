import pygame
import random
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, PIECE_COLOR_A, PIECE_COLOR_B
from checkers.game import Game
from minmax.algorithm import alphabeta
from ui import UI

FPS = 60

class Application:
    """
    應用程式總管類別，負責管理主迴圈、遊戲狀態與各個元件。
    """
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Checkers')
        self.clock = pygame.time.Clock()
        self.ui = UI(self.win)
        self.game = None
        self.game_mode = None
        self.ai_depth = 0
        self.running = True
        self.state = "main_menu"
        self.game_over_sound_played = False

        try:
            self.move_sound = pygame.mixer.Sound('assets/sounds/move.wav')
            self.capture_sound = pygame.mixer.Sound('assets/sounds/capture.wav')
            self.king_sound = pygame.mixer.Sound('assets/sounds/king.wav')
            self.win_sound = pygame.mixer.Sound('assets/sounds/win.wav')
            self.draw_sound = pygame.mixer.Sound('assets/sounds/draw.wav')
        except pygame.error as e:
            print(f"Warning: Sound file not found - {e}")
            self.move_sound = self.capture_sound = self.king_sound = self.win_sound = self.draw_sound = None

    def _get_row_col_from_mouse(self, pos):
        """將滑鼠座標轉換為棋盤行列"""
        x, y = pos
        return y // SQUARE_SIZE, x // SQUARE_SIZE

    def run(self):
        """應用程式主迴圈"""
        while self.running:
            self.clock.tick(FPS)

            if self.state == "main_menu":
                self._handle_main_menu()
            elif self.state == "difficulty_menu":
                self._handle_difficulty_menu()
            elif self.state == "in_game":
                self._handle_in_game()
            elif self.state == "game_over":
                self._handle_game_over()
        
        pygame.quit()

    def _play_sound(self, sound_event):
        """根據傳入的事件字串，播放對應的音效"""
        if sound_event == "move" and self.move_sound:
            self.move_sound.play()
        elif sound_event == "capture" and self.capture_sound:
            self.capture_sound.play()
        elif sound_event == "king" and self.king_sound:
            self.king_sound.play()

    def _handle_main_menu(self):
        """處理主選單邏輯"""
        choice = self.ui.main_menu()
        if choice == "quit":
            self.running = False
        elif choice == 'pvp':
            self.game_mode = 'pvp'
            self.game = Game(self.win, self.game_mode)
            self.state = "in_game"
        elif choice == 'pva':
            self.game_mode = 'pva'
            self.state = "difficulty_menu"

    def _handle_difficulty_menu(self):
        """處理難度選擇邏輯"""
        choice = self.ui.difficulty_menu()
        if choice == "quit":
            self.running = False
        elif isinstance(choice, int):
            self.ai_depth = choice
            self.game = Game(self.win, self.game_mode)
            self.state = "in_game"

    # (在 Application class 中)
    def _handle_in_game(self):
        """處理遊戲進行中的邏輯"""
        winner = self.game.winner()
        if winner is not None:
            self.state = "game_over"
            return

        # 處理 AI 回合
        if self.game_mode == 'pva' and self.game.turn == PIECE_COLOR_B:
            # --- 新增：在 AI 計算前延遲 500 毫秒 (0.5秒) ---
            pygame.time.delay(500) 

            old_piece_count = self.game.board.red_left + self.game.board.white_left
            value, new_board = alphabeta(self.game.get_board(), self.ai_depth, float('-inf'), float('inf'), True, self.game)
            if new_board:
                 self.game.ai_move(new_board)
                 new_piece_count = self.game.board.red_left + self.game.board.white_left
                 if new_piece_count < old_piece_count:
                     self._play_sound("capture")
                 else:
                     self._play_sound("move")

        # 處理玩家事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not (self.game_mode == 'pva' and self.game.turn == PIECE_COLOR_B):
                    pos = pygame.mouse.get_pos()
                    row, col = self._get_row_col_from_mouse(pos)
                    move_event = self.game.select(row, col)
                    if move_event:
                        self._play_sound(move_event)
        
        self.game.update()
        self.ui.draw_game_info(self.game)
        pygame.display.update()

    def _handle_game_over(self):
        """處理遊戲結束邏輯"""
        winner = self.game.winner()
        
        if not self.game_over_sound_played:
            if winner == "DRAW" and self.draw_sound:
                self.draw_sound.play()
            elif self.win_sound:
                self.win_sound.play()
            self.game_over_sound_played = True

        choice = self.ui.game_over_screen(winner)
        if choice == "quit":
            self.running = False
        elif choice == "restart":
            self.game_over_sound_played = False
            self.state = "main_menu"

def main():
    """程式主入口"""
    app = Application()
    app.run()

if __name__ == '__main__':
    main()