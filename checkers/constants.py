import pygame

# --- 核心尺寸與格線 ---
WIDTH = 800
HEIGHT = 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# --- 新色彩主題 ---
# 棋盤顏色 (米白與灰綠)
BOARD_COLOR_LIGHT = (238, 238, 210)
BOARD_COLOR_DARK = (118, 150, 86)

# 棋子顏色 (玩家A: 紅色, 玩家B/AI: 藍色)
PIECE_COLOR_A = (200, 20, 20)
PIECE_COLOR_B = (0, 100, 200)

# UI 提示顏色
VALID_MOVE_COLOR = (100, 255, 100, 150) # 半透明亮綠色
SELECTED_PIECE_COLOR = (0, 255, 0)
FORCED_CAPTURE_COLOR = (255, 255, 0)

# 文字與按鈕顏色
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (128, 128, 128)
BUTTON_HOVER_COLOR = (158, 158, 158)
BACKGROUND_COLOR = (49, 46, 43)

# --- 圖像資源 ---
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

# --- UI 常數 ---
MENU_FONT_SIZE = 60
INFO_FONT_SIZE = 30
BUTTON_WIDTH = 320
BUTTON_HEIGHT = 65