"""Text."""

import pygame


def draw_text(
    screen,
    text,
    x,
    y,
    w=100,
    h=100,
    text_color=(0, 0, 0),
    font_name="freesansbold.ttf",
    font_size=20,
):
    """Draw text to the screen."""
    font = pygame.font.Font(font_name, font_size)
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (x, y, w, h))
