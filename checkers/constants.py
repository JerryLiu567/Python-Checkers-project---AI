import pygame

WIDTH = 800
HEIGHT = 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

RED =(255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREY = (128,128,128)

# --- 新增顏色 ---
YELLOW = (255, 255, 0) # 用於標示需要吃子的棋

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'),(44,25))
