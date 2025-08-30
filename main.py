import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
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
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Checkers')
        self.clock = pygame.time.Clock()
        self.ui = UI(self.win)
        self.game = None
        self.game_mode = None
        self.ai_depth = 0
        self.running = True
        self.state = "main_menu" # 初始狀態為主選單

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

    def _handle_in_game(self):
        """處理遊戲進行中的邏輯"""
        # 1. 檢查遊戲是否結束
        winner = self.game.winner()
        if winner is not None:
            self.state = "game_over"
            return

        # 2. 處理 AI 回合
        if self.game_mode == 'pva' and self.game.turn == WHITE:
            value, new_board = alphabeta(self.game.get_board(), self.ai_depth, float('-inf'), float('inf'), True, self.game)
            if new_board:
                 self.game.ai_move(new_board)

        # 3. 處理玩家事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 確保不是 AI 回合才處理點擊
                if not (self.game_mode == 'pva' and self.game.turn == WHITE):
                    pos = pygame.mouse.get_pos()
                    row, col = self._get_row_col_from_mouse(pos)
                    self.game.select(row, col)
        
        # 4. 更新畫面
        self.game.update()

    def _handle_game_over(self):
        """處理遊戲結束邏輯"""
        winner = self.game.winner()
        choice = self.ui.game_over_screen(winner)
        if choice == "quit":
            self.running = False
        elif choice == "restart":
            self.state = "main_menu" # 回到主選單

def main():
    """程式主入口"""
    app = Application()
    app.run()

if __name__ == '__main__':
    main()