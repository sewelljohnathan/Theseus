"""Driver for Theseus."""

import os

import pygame

from gamestate import GameState
from scenes.battle_scene import BattleScene


def main():
    """Driver."""
    pygame.init()
    pygame.font.init()

    game_state = GameState()
    game_state.screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("THESEUS")

    icon_path = os.path.join(".", "assets", "logo.png")
    icon_image = pygame.image.load(icon_path).convert_alpha()
    pygame.display.set_icon(icon_image)

    game_state.scene = BattleScene()

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()

        game_state.scene.run()
        pygame.display.update()


if __name__ == "__main__":
    main()
