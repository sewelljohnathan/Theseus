"""Driver for Theseus."""

import os

import pygame

from button import Button
from text import draw_text

OFF_WHITE = (200, 200, 200)


def battle(screen: pygame.Surface):
    """Draw the battle scene."""
    screen.fill((100, 0, 255))

    battle_window = pygame.Rect(30, 30, 1220, 450)
    pygame.draw.rect(screen, OFF_WHITE, battle_window)

    options_window = pygame.Rect(30, 500, 1220, 200)
    pygame.draw.rect(screen, OFF_WHITE, options_window)

    Button(
        "1) Attack", 40, 510, 150, 30, lambda: draw_text(screen, "Attacking!", 500, 300)
    ).draw(screen)

    Button(
        "2) Defend", 40, 550, 150, 30, lambda: draw_text(screen, "Defending!", 500, 300)
    ).draw(screen)
    Button(
        "3) RUN", 40, 590, 150, 30, lambda: draw_text(screen, "Running!", 500, 300)
    ).draw(screen)


def main():
    """Driver."""
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("THESEUS")

    icon_path = os.path.join(".", "assets", "logo.png")
    icon_image = pygame.image.load(icon_path).convert_alpha()
    pygame.display.set_icon(icon_image)

    is_running = True

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()

        battle(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
