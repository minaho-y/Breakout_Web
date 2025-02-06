from enum import Enum, auto
import pygame
import asyncio
import sys
from config import SCREEN, SCREEN_MODE, F_RATE
from title import title_screen
from game import game_screen
from result import result_screen

############################
### メイン関数
############################
async def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption('ブロック崩し')

    clock = pygame.time.Clock()

    running = True

    current_state = SCREEN_MODE.TITLE  # 初期状態はタイトル画面

    while running:
        clock.tick(F_RATE)
        await asyncio.sleep(0)    #引数は0で固定

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

        # 画面遷移
        if current_state == SCREEN_MODE.TITLE:
            current_state = await title_screen(screen)
        elif current_state == SCREEN_MODE.GAME:
            current_state = await game_screen(screen)
        elif current_state == SCREEN_MODE.RESULT:
            current_state = await result_screen(screen)

        pygame.display.flip()  # 画面更新
        
    # 終了処理
    sys.exit()
    pygame.quit()

# if __name__ == "__main__":
asyncio.run(main())