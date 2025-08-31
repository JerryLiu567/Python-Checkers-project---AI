import pygame
from checkers.constants import (WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR,
                               MENU_FONT_SIZE, INFO_FONT_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT,
                               PIECE_COLOR_A, PIECE_COLOR_B)

class UI:
    """
    負責管理所有使用者介面(選單、按鈕)的類別。
    """
    def __init__(self, win):
        self.win = win
        self.menu_font = pygame.font.SysFont(None, MENU_FONT_SIZE)
        self.info_font = pygame.font.SysFont(None, INFO_FONT_SIZE)

    def _draw_text(self, text, font, color, x, y):
        """通用繪製文字函式"""
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        self.win.blit(textobj, textrect)

    def _draw_menu_background(self, title):
        """繪製統一的選單背景和標題"""
        self.win.fill(BACKGROUND_COLOR)
        self._draw_text(title, self.menu_font, TEXT_COLOR, WIDTH//2, HEIGHT//4)

    def main_menu(self):
        pvp_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - 80, BUTTON_WIDTH, BUTTON_HEIGHT)
        pva_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 10, BUTTON_WIDTH, BUTTON_HEIGHT)

        self._draw_menu_background('Checkers AI')
        
        run_menu_loop = True
        while run_menu_loop:
            mouse_pos = pygame.mouse.get_pos()

            button_color = BUTTON_HOVER_COLOR if pvp_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.win, button_color, pvp_button)
            
            button_color = BUTTON_HOVER_COLOR if pva_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.win, button_color, pva_button)

            self._draw_text('Player vs Player', self.menu_font, TEXT_COLOR, pvp_button.centerx, pvp_button.centery)
            self._draw_text('Player vs AI', self.menu_font, TEXT_COLOR, pva_button.centerx, pva_button.centery)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pvp_button.collidepoint(event.pos): return 'pvp'
                    if pva_button.collidepoint(event.pos): return 'pva'
        return None

    def difficulty_menu(self):
        easy_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - 110, BUTTON_WIDTH, BUTTON_HEIGHT)
        medium_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - 25, BUTTON_WIDTH, BUTTON_HEIGHT)
        hard_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 60, BUTTON_WIDTH, BUTTON_HEIGHT)

        self._draw_menu_background('Select AI Difficulty')

        run_menu_loop = True
        while run_menu_loop:
            mouse_pos = pygame.mouse.get_pos()

            button_color = BUTTON_HOVER_COLOR if easy_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.win, button_color, easy_button)
            button_color = BUTTON_HOVER_COLOR if medium_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.win, button_color, medium_button)
            button_color = BUTTON_HOVER_COLOR if hard_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.win, button_color, hard_button)
            
            self._draw_text('Easy (Depth 2)', self.menu_font, TEXT_COLOR, easy_button.centerx, easy_button.centery)
            self._draw_text('Medium (Depth 4)', self.menu_font, TEXT_COLOR, medium_button.centerx, medium_button.centery)
            self._draw_text('Hard (Depth 5)', self.menu_font, TEXT_COLOR, hard_button.centerx, hard_button.centery)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos): return 2
                    if medium_button.collidepoint(event.pos): return 4
                    if hard_button.collidepoint(event.pos): return 5
        return None

    def game_over_screen(self, winner):
        restart_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0,0,0,128))
        self.win.blit(s, (0,0))

        if winner == "DRAW":
            message = "The game is a DRAW."
        else:
            winner_name = "Red Player" if winner == PIECE_COLOR_A else "Blue Player"
            message = f"{winner_name} wins!"
        
        self._draw_text(message, self.menu_font, TEXT_COLOR, WIDTH//2, HEIGHT//4)

        run_menu_loop = True
        while run_menu_loop:
            mouse_pos = pygame.mouse.get_pos()

            button_color = BUTTON_HOVER_COLOR if restart_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.win, button_color, restart_button)
            self._draw_text('Restart', self.menu_font, TEXT_COLOR, restart_button.centerx, restart_button.centery)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        return "restart"
        return None

    def draw_game_info(self, game):
        """繪製遊戲中的即時資訊，如回合、剩餘棋子等"""
        red_info = f"Red Pieces: {game.board.red_left}"
        self._draw_text(red_info, self.info_font, PIECE_COLOR_A, 100, 25)

        white_info = f"Blue Pieces: {game.board.white_left}"
        self._draw_text(white_info, self.info_font, PIECE_COLOR_B, WIDTH - 100, 25)

        turn_text = "RED's Turn" if game.turn == PIECE_COLOR_A else "BLUE's Turn"
        turn_color = PIECE_COLOR_A if game.turn == PIECE_COLOR_A else PIECE_COLOR_B
        self._draw_text(turn_text, self.info_font, turn_color, WIDTH // 2, 25)

        draw_counter_text = f"Draw Counter: {game.board.moves_since_last_capture_or_king} / 50"
        self._draw_text(draw_counter_text, self.info_font, TEXT_COLOR, WIDTH // 2, HEIGHT - 25)