"""Driver for Theseus."""

import os

import pygame

from scenes import BattleScene


def main():
    """Driver."""
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("THESEUS")

    icon_path = os.path.join(".", "assets", "logo.png")
    icon_image = pygame.image.load(icon_path).convert_alpha()
    pygame.display.set_icon(icon_image)

    battle = BattleScene(screen)

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()
        battle.run(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
