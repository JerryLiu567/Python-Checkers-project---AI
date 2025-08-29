import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK, GREY
from checkers.game import Game
from minmax.algorithm import minmax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    run_menu = True
    font = pygame.font.SysFont(None, 50)
    
    pvp_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 50)
    pva_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 50)

    while run_menu:
        WIN.fill(BLACK)
        draw_text('Select Game Mode', font, WHITE, WIN, WIDTH//2, HEIGHT//4)

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
    pygame.font.init()
    game_mode = main_menu()

    if game_mode is None:
        run = False
    else:
        game = Game(WIN, game_mode)

    while run:
        clock.tick(FPS)

        # --- 修改部分：處理遊戲結束後的延遲 ---
        game_result = game.winner()
        if game_result is not None:
            if game_result == "DRAW":
                print("The game is a DRAW.")
            else:
                print(f"{game_result} wins!")
            pygame.time.delay(3000) # 遊戲結束後停留3秒
            run = False
            continue # 結束此次迴圈，避免繼續執行

        if game_mode == 'pva' and game.turn == WHITE:
            pygame.time.delay(500)
            value, new_board = minmax(game.get_board(), 3, WHITE, game)
            if new_board:
                 game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not (game_mode == 'pva' and game.turn == WHITE):
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        if 'game' in locals():
            game.update()
    
    pygame.quit()

main()