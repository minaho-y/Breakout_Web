import pygame
from config import SCREEN_MODE, SCREEN, F_RATE
import game
# from title import title_screen

HOME_BUTTON_PATH = "HomeButton.png"

############################
### Home Button クラス
############################
class HomeButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(HOME_BUTTON_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*0.8, self.image.get_height()*0.8))
        self.rect = self.image.get_rect()
        self.rect.centery = SCREEN.bottom - 120
        self.rect.centerx = SCREEN.width / 2

    def draw(self, screen):
        screen.blit(self.image, self.rect)

async def result_screen(screen):
    running = True
    homeButton = HomeButton()
    clock = pygame.time.Clock()

    # time = Time()
    # score = Score(screen)


    while running:
        events = pygame.event.get()
        clock.tick(F_RATE)
        # イベント処理
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_h:
                    running = False
                    # await title_screen(screen)
                    return SCREEN_MODE.TITLE
            if event.type == pygame.MOUSEBUTTONDOWN:

                if homeButton.rect.collidepoint(event.pos):
                    running = False
                    # await title_screen(screen)
                    return SCREEN_MODE.TITLE

        screen.fill((20, 20, 20))

        # RESULT
        font = pygame.font.SysFont(None, 100)
        img = font.render('RESULT', True, (255, 50, 50))
        text_rect = img.get_rect(center=(SCREEN.width // 2, SCREEN.height // 4))
        screen.blit(img, text_rect)

        # Brock Score
        # global result_score
        font_b = pygame.font.SysFont(None, 50)
        img_b = font_b.render(f'Block Score : {game.result_score}', True, (255, 255, 250))
        text_b_rect = img_b.get_rect(center=(SCREEN.width // 2, 300))
        screen.blit(img_b, text_b_rect)

        # Time Remaining
        # global left_time
        font_t = pygame.font.SysFont(None, 50)
        img_t = font_t.render(f'Time Left : {game.result_time}', True, (255, 255, 250))
        text_t_rect = img_t.get_rect(center=(SCREEN.width // 2, 370))
        screen.blit(img_t, text_t_rect)

        homeButton.draw(screen)

        pygame.display.update()