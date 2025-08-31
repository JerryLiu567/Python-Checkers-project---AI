import pygame
from checkers.constants import WIDTH, HEIGHT, BLACK, WHITE, GREY

class UI:
    """
    負責管理所有使用者介面(選單、按鈕)的類別。
    """
    def __init__(self, win):
        self.win = win
        self.font = pygame.font.SysFont(None, 50)

    def _draw_text(self, text, color, x, y):
        """通用繪製文字函式"""
        textobj = self.font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        self.win.blit(textobj, textrect)

    def main_menu(self):
        """
        繪製主選單，並根據事件回傳玩家的選擇。
        :return: 'pvp', 'pva' 或 None (如果關閉視窗)
        """
        pvp_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 50)
        pva_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 50)

        self.win.fill(BLACK)
        self._draw_text('Select Game Mode', WHITE, WIDTH//2, HEIGHT//4)

        pygame.draw.rect(self.win, GREY, pvp_button)
        pygame.draw.rect(self.win, GREY, pva_button)
        self._draw_text('Player vs Player', WHITE, pvp_button.centerx, pvp_button.centery)
        self._draw_text('Player vs AI', WHITE, pva_button.centerx, pva_button.centery)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pvp_button.collidepoint(mouse_pos):
                    return 'pvp'
                if pva_button.collidepoint(mouse_pos):
                    return 'pva'
        return None

    def difficulty_menu(self):
        """
        繪製 AI 難度選擇選單，並回傳對應的深度。
        :return: 2, 4, 5 或 None
        """
        easy_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 100, 300, 50)
        medium_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 30, 300, 50)
        hard_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 40, 300, 50)

        self.win.fill(BLACK)
        self._draw_text('Select AI Difficulty', WHITE, WIDTH//2, HEIGHT//4)

        pygame.draw.rect(self.win, GREY, easy_button)
        pygame.draw.rect(self.win, GREY, medium_button)
        pygame.draw.rect(self.win, GREY, hard_button)
        self._draw_text('Easy (Depth 1)', WHITE, easy_button.centerx, easy_button.centery)
        self._draw_text('Medium (Depth 3)', WHITE, medium_button.centerx, medium_button.centery)
        self._draw_text('Hard (Depth 5)', WHITE, hard_button.centerx, hard_button.centery)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy_button.collidepoint(mouse_pos):
                    return 1
                if medium_button.collidepoint(mouse_pos):
                    return 3
                if hard_button.collidepoint(mouse_pos):
                    return 5
        return None

    def game_over_screen(self, winner):
        """
        繪製遊戲結束畫面。
        :param winner: 勝利者的字串 ("WHITE", "RED", "DRAW")
        :return: "restart" 或 "quit"
        """
        restart_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 50)
        
        # 稍微變暗背景來凸顯文字
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0,0,0,128))
        self.win.blit(s, (0,0))

        if winner == "DRAW":
            message = "The game is a DRAW."
        else:
            message = f"{winner} wins!"
        
        self._draw_text(message, WHITE, WIDTH//2, HEIGHT//4)
        
        pygame.draw.rect(self.win, GREY, restart_button)
        self._draw_text('Restart', WHITE, restart_button.centerx, restart_button.centery)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return "restart"
        return None