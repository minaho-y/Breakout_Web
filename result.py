import pygame
from config import SCREEN_MODE, SCREEN

async def result_screen(screen, score, left_time):
    screen.fill((20, 20, 20))

    # RESULT
    font = pygame.font.SysFont(None, 100)
    img = font.render('RESULT', True, (255, 50, 50))
    text_rect = img.get_rect(center=(SCREEN.width // 2, SCREEN.height // 4))
    screen.blit(img, text_rect)

    # Brock Score
    font_b = pygame.font.SysFont(None, 50)
    img_b = font_b.render(f'Block Score : {score}', True, (255, 255, 250))
    text_b_rect = img_b.get_rect(center=(SCREEN.width // 2, 300))
    screen.blit(img_b, text_b_rect)

    # Time Remaining
    font_t = pygame.font.SysFont(None, 50)
    img_t = font_t.render(f'Time Remaining : {left_time}', True, (255, 255, 250))
    text_t_rect = img_t.get_rect(center=(SCREEN.width // 2, 370))
    screen.blit(img_t, text_t_rect)

    pygame.display.update()