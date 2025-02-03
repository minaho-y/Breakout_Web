from enum import Enum, auto
import pygame
import asyncio
import sys
from config import SCREEN, SCREEN_MODE, F_RATE
from title import title_screen
from game import game_screen
from result import result_screen

current_state = SCREEN_MODE.TITLE  # 初期状態はタイトル画面
############################
### メイン関数
############################
async def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption('ブロック崩し')

    clock = pygame.time.Clock()

    # 現在の画面を記録（変更を検知するため）
    previous_state = None 

    global current_state
    running = True

    while running:
        clock.tick(F_RATE)
        await asyncio.sleep(0)    #引数は0で固定

        # 画面が切り替わったら再描画
        if current_state != previous_state:
            if current_state == SCREEN_MODE.TITLE:
                await title_screen(screen)
            elif current_state == SCREEN_MODE.GAME:
                await game_screen(screen)
            elif current_state == SCREEN_MODE.RESULT:
                await result_screen(screen)
        previous_state = current_state
        
        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:
                running = False
            # キーイベント
            if event.type == pygame.KEYDOWN:
                print(f"Current state: {current_state}")
                # Escキーが押されたら終了
                if event.key == pygame.K_ESCAPE:
                    running = False
                # タイトル画面 -> ゲーム画面
                if current_state == SCREEN_MODE.TITLE and event.key == pygame.K_RETURN:
                    current_state = SCREEN_MODE.GAME
                # ゲーム画面 -> リザルト画面
                # if current_state == SCREEN_MODE.GAME:
                #     current_state = SCREEN_MODE.RESULT
        
        pygame.display.flip()  # 画面更新
    # 終了処理
    pygame.quit()
    sys.exit()

# if __name__ == "__main__":
asyncio.run(main())