"""Driver for Theseus."""

import os

import pygame

from gamestate import GameState
# from scenes.battle_scene import BattleScene
from scenes.pause_screen import PauseHandler
# from scenes.mg_wheel import MGWheel
from scenes.mg_simon import MGSIMON


def main():
    """Driver."""
    pygame.init()
    pygame.font.init()

    game_state = GameState()
    game_state.screen = pygame.display.set_mode((1280, 720))
    game_state.clock = pygame.time.Clock()
    pygame.display.set_caption("THESEUS")

    icon_path = os.path.join(".", "assets", "logo.png")
    icon_image = pygame.image.load(icon_path).convert_alpha()
    pygame.display.set_icon(icon_image)

    game_state.scene = MGSIMON()
    pause_handler = PauseHandler()

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                game_state.key_press = pygame.key.name(event.key)
            if event.type == pygame.KEYUP:
                print(pygame.key.name(event.key))
                game_state.key_press = None

        game_state.scene.run()
        pause_handler.run()
        pygame.display.update()
        game_state.clock.tick(30)


if __name__ == "__main__":
    main()
