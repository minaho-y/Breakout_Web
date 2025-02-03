import asyncio
import math
import pygame
import sys
import pygame.event
# import pygame_widgets
from pygame.locals import *
from config import SCREEN, SCREEN_MODE, F_RATE
from result import result_screen
# from pygame_widgets.progressbar import ProgressBar

### 定数
START_LIFE = 3          # ライフの数
TIME_LIMIT = 30         # タイムリミット
BALL_SIZE = 18          # ボールサイズ
P_WIDTH = 100           # パドル幅
P_HEIGHT = 10           # パドル高さ
BLOCK_WIDTH = 50        # ブロック幅
BLOCK_HEIGHT = 25       # ブロック高さ
BLOCK_LOWS = 5          # ブロック縦列の数
BLOCK_COLS = 10         # ブロック横列の数
B_TOP = 50              # ブロック上の余白
BLOCK_OFFSET_X = int((SCREEN.width - (BLOCK_WIDTH * BLOCK_COLS)) / 2)   # ブロック横の余白

E_TIME = 2.5           # ゲーム終了を表示する時間

### 画像のパス
PADDLE_IMAGE_PATH = "paddle_04.png"
BALL_IMAGE_PATH = "ballYellow_02.png"
BLOCK_IMAGE_PATH = "tileBlue_02.png"

############################
### パドルクラス
############################
class Paddle(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (P_WIDTH, P_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN.bottom - 20   # パドルのy座標
        self.rect.left = SCREEN.width / 2 - self.rect.width / 2
        
    def update(self):
        # パドルの移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        self.rect.clamp_ip(SCREEN)      # ゲーム画面内のみで移動

############################
### ボールクラス
############################
class Ball(pygame.sprite.Sprite):
    def __init__(self, filename, paddle, blocks, speed, angle_left, angle_right, score, life):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        self.dx = self.dy =  0      # ボールの速度
        self.paddle = paddle        # パドルへの参照
        self.blocks = blocks        # ブロックグループへの参照
        self.score = score          # スコアへの参照
        self.life = life            # ライフへの参照
        self.update = self.start    # ゲーム開始状態に更新
        self.speed = speed
        self.angle_left = angle_left    # パドルへの反射方向
        self.angle_right = angle_right

    def start(self):
        # ボールの初期位置（パドルの上）
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top

        # スペースキーでボール射出
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.dx = 0
            self.dy = -self.speed
            self.update = self.move

    # ボールの挙動
    def move(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

        # 壁との反射
        if self.rect.left < SCREEN.left:    # 左側
            self.rect.left = SCREEN.left
            self.dx = -self.dx
        if self.rect.right > SCREEN.right:  # 右側
            self.rect.right = SCREEN.right
            self.dx = -self.dx
        if self.rect.top < SCREEN.top:      # 上側
            self.rect.top = SCREEN.top
            self.dy = -self.dy

        # パドルとの反射(左端:135度方向, 右端:45度方向, それ以外:線形補間)
        if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
            (x1, y1) = (self.paddle.rect.left - self.rect.width, self.angle_left)
            (x2, y2) = (self.paddle.rect.right, self.angle_right)
            x = self.rect.left      # ボールが当たった位置
            y = (float(y2-y1)/(x2-x1)) * (x-x1) + y1    # 線形補間
            angle = math.radians(y)
            self.dx = self.speed * math.cos(angle)
            self.dy = -self.speed * math.sin(angle)

        # ボールを落とした場合
        if self.rect.top > SCREEN.bottom:
            self.update = self.start    # ボールを初期状態に
            self.life.add_life(-1)      # ライフを1減らす
            if self.score.get_score() < 50:
                self.score.set_score(0)     # スコアを0点に
            else: self.score.add_score(-50)

        # ボールと衝突したブロックリストを取得
        blocks_collided = pygame.sprite.spritecollide(self, self.blocks, True)
        if blocks_collided:
            self.score.add_score(10)
            oldrect = self.rect
            for block in blocks_collided:
                # ボールが左からブロックへ衝突
                if oldrect.left < block.rect.left and oldrect.right < block.rect.right:
                    self.rect.right = block.rect.left
                    self.dx = -self.dx

                # ボールが右からブロックへ衝突
                if oldrect.left > block.rect.left and oldrect.right > block.rect.right:
                    self.rect.left = block.rect.right
                    self.dx = -self.dx

                # ボールが上からブロックへ衝突
                if oldrect.top < block.rect.top and oldrect.bottom < block.rect.bottom:
                    self.rect.bottom = block.rect.top
                    self.dy = -self.dy

                # ボールが下からブロックへ衝突
                if oldrect.top > block.rect.top and oldrect.bottom > block.rect.bottom:
                    self.rect.top = block.rect.bottom
                    self.dy = -self.dy

############################
### ブロッククラス
############################
class Block(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = BLOCK_OFFSET_X + x * self.rect.width
        self.rect.top = y * self.rect.height + B_TOP

    # 残りのブロック数を取得
    def get_blocks(self):
        return len(self.blocks)

############################
### スコアクラス
############################
class Score:
    def __init__(self, x, y):
        self.score = 0
        self.sysfont = pygame.font.SysFont(None, 30)
        (self.x, self.y) = (x, y)

    def draw(self, screen):
        img = self.sysfont.render('SCORE : ' + str(self.score), True, (255, 255, 250))
        screen.blit(img, (self.x, self.y))

    def add_score(self, x):
        self.score += x

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score
    
############################
### ライフクラス
############################
class Life:
    def __init__(self, x, y):
        self.life = START_LIFE
        self.sysfont = pygame.font.SysFont(None, 30)
        (self.x, self.y) = (x, y)

    def draw(self, screen):
        img = self.sysfont.render('LIFE : ' + str(self.life), True, (255, 255, 250))
        screen.blit(img, (self.x, self.y))

    # def set_life(self, x):
    #     self.life = x

    def add_life(self, x):
        self.life += x

    def get_life(self):
        return self.life
 
############################
### クリアを表示し，画面遷移 
############################
async def show_game_clear(screen):
    ### GAME CLEARを表示
    font = pygame.font.Font(None, 60)
    text_str = "GAME CLEAR"
    text = font.render(text_str, True, (63,255,63))
    font_width, font_height = font.size(text_str)
    screen.blit(text, (SCREEN.centerx-font_width/2, SCREEN.centery-font_height/2))
    pygame.display.update()
    ### CLEAR画面時間
    await asyncio.sleep(E_TIME)
    await result_screen(screen)

############################
### ゲームオーバーを表示し，画面遷移 
############################
async def show_game_over(screen):
    ### GAME OVERを表示
    font = pygame.font.Font(None, 60)
    text_str = "GAME OVER"
    text = font.render(text_str, True, (63,255,63))
    font_width, font_height = font.size(text_str)
    screen.blit(text, (SCREEN.centerx-font_width/2, SCREEN.centery-font_height/2))
    pygame.display.update()
    await asyncio.sleep(E_TIME)
    await result_screen(screen)

############################
### 時間クラス
############################
class Time:
    def __init__(self, now_time, x, y):
        self.now_time = now_time
        self.sysfont = pygame.font.SysFont(None, 30)
        (self.x, self.y) = (x, y)

    def calc_elapsed_time(self, now, start):
        self.elapsed_time = (now - start) / 1000
        return self.elapsed_time

    def show_rest_time(self, screen):
        self.rest_time = (int) (TIME_LIMIT - self.elapsed_time)
        img = self.sysfont.render('TIME LEFT : ' + str(self.rest_time), True, (255, 255, 250))
        screen.blit(img, (self.x, self.y))

############################
### メイン関数 
############################
async def game_screen(screen):

    # クロックオブジェクトの作成
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    running = True

    # progressBar = ProgressBar(screen, 50, 50, SCREEN.centerx-50, 5, lambda: 1 - (pygame.time.get_ticks() - start_ticks) / 10, curved=True)

    # 描画用のスプライトグループ
    group = pygame.sprite.RenderUpdates()

    # 衝突判定用のスプライトグループ
    blocks = pygame.sprite.Group()

    # スプライトグループに追加
    Paddle.containers = group
    Ball.containers = group
    Block.containers = group, blocks

    paddle = Paddle(PADDLE_IMAGE_PATH)

    # ブロックの作成 (14 x 10)
    for y in range(0, BLOCK_LOWS):
        for x in range(0, BLOCK_COLS):
            Block(BLOCK_IMAGE_PATH, x, y)

    # スコアを画面に表示
    score = Score(10, 10)

    # ライフを画面に表示
    life = Life(710, 10)

    # 制限時間を画面に表示
    time = Time(TIME_LIMIT, 500, 10)

    pygame.display.update()  # **画面更新**

    global current_state

    Ball(BALL_IMAGE_PATH, paddle, blocks, 5, 135, 45, score, life)

    while running:
        events = pygame.event.get()
        clock.tick(F_RATE)
        elapsed_time = time.calc_elapsed_time(pygame.time.get_ticks(), start_ticks)

        ## 残ブロックなし
        if len(blocks) == 0:
            await show_game_clear(screen)
            return
        
        ### ゲームオーバー
        if life.get_life() < 1 or elapsed_time > TIME_LIMIT:
            await show_game_over(screen)
            running = False
            return

        # イベント処理
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # 全てのスプライトグループを更新
        group.update()
        screen.fill((0, 0, 0))  # 画面クリア
        # 全てのスプライトグループを描画
        group.draw(screen)
        # スコアを描画
        score.draw(screen)
        # スコアを描画
        life.draw(screen)
        # 残り時間を描画
        time.show_rest_time(screen)

        pygame.display.update()  # 画面更新