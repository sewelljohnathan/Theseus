"""Battle Scene class."""

import pygame

from button import Button
from gamestate import GameState
from scenes.scene import Scene
from text import TextWrapper


class BattleScene(Scene):
    """Battle Scene."""

    def __init__(self):
        """Initialize Battle scene."""
        self.attack_button = Button(
            "1) Attack",
            40,
            510,
            150,
            30,
            TextWrapper("Attacking!", (500, 300, 100, 100)).draw,
        )
        self.defend_button = Button(
            "2) Defend",
            40,
            550,
            150,
            30,
            TextWrapper("Defending!", (500, 300, 100, 100)).draw,
        )
        self.run_button = Button(
            "3) RUN",
            40,
            590,
            150,
            30,
            TextWrapper("Running!", (500, 300, 100, 100)).draw,
        )

    def run(self):
        """Draw the battle scene."""
        game_state = GameState()

        game_state.screen.fill((100, 0, 255))

        battle_window = pygame.Rect(30, 30, 1220, 450)
        pygame.draw.rect(game_state.screen, (200, 200, 200), battle_window)

        options_window = pygame.Rect(30, 500, 1220, 200)
        pygame.draw.rect(game_state.screen, (200, 200, 200), options_window)

        self.attack_button.draw()
        self.defend_button.draw()
        self.run_button.draw()
