import pygame
# import sys
from config import SCREEN, SCREEN_MODE, F_RATE
# from game import game_screen

PLAY_BUTTON_PATH = "PlayButton.png"

############################
### Play Button クラス
############################
class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(PLAY_BUTTON_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*0.8, self.image.get_height()*0.8))
        self.rect = self.image.get_rect()
        self.rect.centery = SCREEN.bottom - 120
        self.rect.centerx = SCREEN.width / 2

    def draw(self, screen):
        screen.blit(self.image, self.rect)

async def title_screen(screen):
    # screen = pygame.display.set_mode(SCREEN.size)
    running = True
    playButton = PlayButton()
    clock = pygame.time.Clock()

    while running:
        events = pygame.event.get()
        clock.tick(F_RATE)

        for event in events:
            if event.type == pygame.QUIT:
                print("TITLE SCREEN: QUIT")  # ← デバッグログ追加
                running = False
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("TITLE SCREEN: ESC")  # ← デバッグログ追加
                    running = False
                    return None
                if event.key == pygame.K_RETURN:
                    print("TITLE SCREEN: Enter -> GAME SCREEN")
                    running = False
                    return SCREEN_MODE.GAME
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.rect.collidepoint(event.pos):
                    print("TITLE SCREEN: Mouse Click -> GAME SCREEN") 
                    running = False
                    print("DEBUG: Exiting title_screen with SCREEN_MODE.GAME")  # 追加
                    return SCREEN_MODE.GAME

        screen.fill((20, 20, 20))
        # global current_state

        # Break Out
        font = pygame.font.SysFont(None, 100)
        img = font.render('BREAK OUT', True, (255, 255, 250))
        text_rect = img.get_rect(center=(SCREEN.width // 2, SCREEN.height // 2))
        screen.blit(img, text_rect)

        playButton.draw(screen)

        pygame.display.update()
