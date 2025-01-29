import pygame
# import sys
from config import SCREEN, SCREEN_MODE

async def title_screen(screen):
    # screen = pygame.display.set_mode(SCREEN.size)
    screen.fill((0, 0, 0))
    global current_state
    font = pygame.font.SysFont(None, 30)
    img = font.render('TITLE', True, (255, 255, 250))
    text_rect = img.get_rect(center=(SCREEN.width // 2, SCREEN.height // 2))
    screen.blit(img, text_rect)

    pygame.display.update()
