from enum import Enum, auto
import pygame
import asyncio
import sys
from game import game_screen

### 定数
F_RATE = 60             # フレームレート

### 画面定義(X軸,Y軸,横,縦)
SCREEN  = pygame.Rect(0, 0, 800, 600) # 画面サイズ

############################
### 画面モードクラス
############################
class SCREEN_MODE(Enum):
    TITLE = auto()
    GAME = auto()
    RESULT = auto()

current_state = SCREEN_MODE.TITLE  # 初期状態はタイトル画面
############################
### メイン関数
############################
async def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption('ブロック崩し')

    clock = pygame.time.Clock()

    global current_state
    running = True

    while(running):
        clock.tick(F_RATE)
        await asyncio.sleep(0)    #引数は0で固定
        screen.fill((0, 0, 0))

        # 画面の切り替え
        if current_state == SCREEN_MODE.TITLE:
            title_screen(screen)
        elif current_state == SCREEN_MODE.GAME:
            game_screen(screen)
        elif current_state == SCREEN_MODE.RESULT:
            result_screen(screen)

        # 画面更新
        pygame.display.update()

        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:
                running = False
            # キーイベント
            if event.type == pygame.KEYDOWN:
                # Escキーが押されたら終了
                if event.key == pygame.K_ESCAPE:
                    running = False

    # 終了処理
    pygame.quit()
    sys.exit()

# if __name__ == "__main__":
asyncio.run(main())