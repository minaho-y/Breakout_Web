from enum import Enum, auto
import pygame

### 画面定義(X軸,Y軸,横,縦)
SCREEN = pygame.Rect(0, 0, 800, 600) # 画面サイズ

### 定数
F_RATE = 60             # フレームレート

############################
### 画面モードクラス
############################
class SCREEN_MODE(Enum):
    TITLE = auto()
    GAME = auto()
    RESULT = auto()