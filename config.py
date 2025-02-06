from enum import Enum, auto
import pygame

### 画面定義(X軸,Y軸,横,縦)
SCREEN = pygame.Rect(0, 0, 800, 600) # 画面サイズ

### 定数
F_RATE = 60             # フレームレート

TIME_LIMIT = 90         # タイムリミット
START_LIFE = 3          # ライフの数
P_WIDTH = 100           # パドル幅
P_HEIGHT = 10           # パドル高さ
BLOCK_WIDTH = 80        # ブロック幅
BLOCK_HEIGHT = 35       # ブロック高さ
BLOCK_LOWS = 4          # ブロック縦列の数
BLOCK_COLS = 6          # ブロック横列の数
B_TOP = 110             # ブロック上の余白
BALL_SIZE = 20          # ボールサイズ

### グローバル変数
left_time = TIME_LIMIT
result_score = 0

############################
### 画面モードクラス
############################
class SCREEN_MODE(Enum):
    TITLE = auto()
    GAME = auto()
    RESULT = auto()