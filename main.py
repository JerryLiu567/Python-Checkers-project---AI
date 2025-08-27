import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK, BLUE, GREY #新增部分：為了讓字體顏色能被辨識，從 constants 引入 GREY
from checkers.game import Game
from minmax.algorithm import minmax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# --- 新增部分：用於顯示文字的函式 ---
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# --- 新增部分：主選單函式 ---
def main_menu():
    """
    顯示主選單，讓玩家選擇遊戲模式。
    返回 'pva' (玩家 vs AI) 或 'pvp' (玩家 vs 玩家)。
    如果玩家關閉視窗，則返回 None。
    """
    run_menu = True
    font = pygame.font.SysFont(None, 50)
    
    # 建立按鈕的矩形區域以便偵測點擊
    pvp_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 50)
    pva_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 50)

    while run_menu:
        WIN.fill(BLACK)
        draw_text('Select Game Mode', font, WHITE, WIN, WIDTH//2, HEIGHT//4)

        # 繪製按鈕
        pygame.draw.rect(WIN, GREY, pvp_button)
        pygame.draw.rect(WIN, GREY, pva_button)
        draw_text('Player vs Player', font, WHITE, WIN, pvp_button.centerx, pvp_button.centery)
        draw_text('Player vs AI', font, WHITE, WIN, pva_button.centerx, pva_button.centery)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pvp_button.collidepoint(mouse_pos):
                    return 'pvp'
                if pva_button.collidepoint(mouse_pos):
                    return 'pva'
    
    return None

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    
    # --- 修改部分：先進入主選單 ---
    # 初始化 pygame.font
    pygame.font.init()
    game_mode = main_menu()

    # 如果玩家在選單就關閉視窗，則結束遊戲
    if game_mode is None:
        run = False
    else:
        game = Game(WIN)

    while run:
        clock.tick(FPS)

        # --- 修改部分：根據遊戲模式決定 AI 是否行動 ---
        # 只有在 '玩家 vs AI' 模式且輪到白色方時，AI 才會動作
        if game_mode == 'pva' and game.turn == WHITE:
            value, new_board = minmax(game.get_board(), 3, WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(f"{game.winner()} wins!")
            # 可以在這裡加入一個延遲或 "再玩一場" 的選項
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        # 只有在 game 物件成功建立後才更新
        if 'game' in locals():
            game.update()
    
    pygame.quit()




main()
