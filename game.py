import asyncio
import math
import pygame
import sys
import pygame.event
from pygame.locals import *
from config import SCREEN, SCREEN_MODE, F_RATE, TIME_LIMIT, P_WIDTH, P_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_LOWS, BLOCK_COLS, B_TOP, BALL_SIZE
# from pygame_widgets.progressbar import ProgressBar

### 定数
DATA_AREA = 50          # データ表示のエリア
BLOCK_OFFSET_X = int((SCREEN.width - (BLOCK_WIDTH * BLOCK_COLS)) / 2)   # ブロック横の余白
E_TIME = 2.5           # ゲーム終了を表示する時間

result_time = TIME_LIMIT
result_score = 0

### 画像のパス
PADDLE_IMAGE_PATH = "paddle_04.png"
BALL_IMAGE_PATH = "ballYellow_02.png"
BLOCK_IMAGE_PATH = "tileBlue_02.png"
HEART_IMAGE_PATH = "suit_hearts.png"
PRESS_SPACE_PATH = "press_space.png"

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
    def __init__(self, filename, paddle, blocks, speed, angle_left, angle_right, score, time):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        self.dx = self.dy =  0      # ボールの速度
        self.paddle = paddle        # パドルへの参照
        self.blocks = blocks        # ブロックグループへの参照
        self.score = score          # スコアへの参照
        self.time = time
        self.update = self.start    # ゲーム開始状態に更新
        self.speed = speed
        self.angle_left = angle_left    # パドルへの反射方向
        self.angle_right = angle_right
        # ボールの初期位置（パドルの上）
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top

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
        if self.rect.top <  DATA_AREA + SCREEN.top:      # 上側
            self.rect.top = DATA_AREA + SCREEN.top 
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
            self.time.add_time(-10)

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
    def __init__(self, screen):
        self.score = 0
        self.draw(screen)

    def draw(self, screen):
        font = pygame.font.Font(None, 40)
        self.text_str = 'SCORE : ' + str(self.score)
        self.text = font.render(self.text_str, True, (255, 255, 250))
        self.text_w, self.str_y = font.size(self.text_str)
        (self.x, self.y) = (10, 10)
        screen.blit(self.text, (self.x, self.y))

    def add_score(self, x):
        if x < 0:
            self.score = max(0, self.score+x)
        else:
            self.score += x

############################
### ゲームオーバー or ゲームクリアを表示
############################
async def show_game_result(screen, is_clear):
    ### CLEAR or OVERを表示
    font = pygame.font.Font(None, 90)
    if is_clear:
        text_str = "GAME CLEAR"
    else: 
        text_str = "GAME OVER"
        
    text = font.render(text_str, True, (63,255,63))
    font_width, font_height = font.size(text_str)
    screen.blit(text, (SCREEN.centerx-font_width/2, SCREEN.centery-font_height/2))
    pygame.display.update()
    await asyncio.sleep(E_TIME)

############################
### 時間クラス
############################
class Time:
    def __init__(self):
        self.sysfont = pygame.font.SysFont(None, 40)
        (self.x, self.y) = (580, 10)
        self.elapsed_time = 0
        self.left_time = TIME_LIMIT
    
    def calc_left_time(self):
        self.left_time = max(0, int(TIME_LIMIT - self.elapsed_time))

    def show_left_time(self, screen):
        self.calc_left_time()
        img = self.sysfont.render('TIME LEFT : ' + str(self.left_time), True, (255, 255, 250))
        screen.blit(img, (self.x, self.y))

    def add_time(self, x):
        self.elapsed_time -= x

############################
### メイン関数 
############################
async def game_screen(screen):
    global result_score
    global result_time
    running = True
    clear_delay = 0  # フレーム遅延用のカウンター

    # クロックオブジェクトの作成
    clock = pygame.time.Clock()
    previous_ticks = None
    ball_started = False    # ボールが発射されたか

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

    # ブロックの作成
    for y in range(0, BLOCK_LOWS):
        for x in range(0, BLOCK_COLS):
            Block(BLOCK_IMAGE_PATH, x, y)

    # スコアを画面に表示
    score = Score(screen)

    # 制限時間を画面に表示
    time = Time()

    ball = Ball(BALL_IMAGE_PATH, paddle, blocks, 5, 135, 45, score, time) 

    pygame.display.update()  # 画面更新

    while running:
        events = pygame.event.get()
        clock.tick(F_RATE)

        screen.fill((20, 20, 20))
        pygame.draw.rect(screen, (50,40,200), (0, 0, SCREEN.width, 45))
        group.draw(screen)

        # イベント処理
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # ボール停止時
                elif event.key == pygame.K_SPACE and ball_started == False:
                    ball_started = True
                    previous_ticks = pygame.time.get_ticks()
                    ball.start()

        if ball_started:
            group.update()
            # 現在のフレームの経過時間を計算して累積する
            current_ticks = pygame.time.get_ticks()
            time.elapsed_time += (current_ticks - previous_ticks) / 1000  # 秒単位で加算
            previous_ticks = current_ticks  # 現在のフレームを次回の前フレームとして更新

        else:   # 停止状態
            paddle.update()
            ball.update()

            # "PRESS SPACE" 表示
            image = pygame.image.load(PRESS_SPACE_PATH).convert_alpha()
            image = pygame.transform.scale(image, (int(image.get_width()), int(image.get_height() * 0.8)))
            rect = image.get_rect(center=(SCREEN.width / 2, SCREEN.height / 2))
            screen.blit(image, rect.topleft)
        
        score.draw(screen)

        time.show_left_time(screen)

        pygame.display.update()  # 画面更新

        ## クリア（残ブロックなし）
        if len(blocks) == 0:
            if clear_delay == 0:
                clear_delay = 1  # 次のフレームに備える
            elif clear_delay == 1:
                running = False
                is_clear = 1
                result_time = time.left_time
                result_score = score.score
                await show_game_result(screen, is_clear)
                return SCREEN_MODE.RESULT
        
        ### ゲームオーバー
        elif time.left_time <= 0:
            is_clear = 0
            result_time = time.left_time   
            result_score = score.score
            await show_game_result(screen, is_clear)
            running = False
            return SCREEN_MODE.RESULT