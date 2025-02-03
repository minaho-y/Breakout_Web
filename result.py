import pygame
from config import SCREEN_MODE, SCREEN
# from game import Score

async def result_screen(screen):
    screen.fill((0, 0, 0))
    # global current_state
    font = pygame.font.SysFont(None, 30)
    img = font.render('RESULT', True, (255, 255, 250))
    text_rect = img.get_rect(center=(SCREEN.width // 2, SCREEN.height // 2))
    screen.blit(img, text_rect)
    pygame.display.update()