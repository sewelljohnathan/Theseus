"""Battle Scene class."""

import pygame

from button import Button
from scenes.scene import Scene
from text import TextWrapper


class BattleScene(Scene):
    """Battle Scene."""

    def __init__(self, screen):
        """Initialize Battle scene."""
        self.attack_button = Button(
            "1) Attack",
            40,
            510,
            150,
            30,
            lambda: TextWrapper("Attacking!", (500, 300, 100, 100)).draw(screen),
        )
        self.defend_button = Button(
            "2) Defend",
            40,
            550,
            150,
            30,
            lambda: TextWrapper("Defending!", (500, 300, 100, 100)).draw(screen),
        )
        self.run_button = Button(
            "3) RUN",
            40,
            590,
            150,
            30,
            lambda: TextWrapper("Running!", (500, 300, 100, 100)).draw(screen),
        )

    def run(self, screen):
        """Draw the battle scene."""
        screen.fill((100, 0, 255))

        battle_window = pygame.Rect(30, 30, 1220, 450)
        pygame.draw.rect(screen, (200, 200, 200), battle_window)

        options_window = pygame.Rect(30, 500, 1220, 200)
        pygame.draw.rect(screen, (200, 200, 200), options_window)

        self.attack_button.draw(screen)
        self.defend_button.draw(screen)
        self.run_button.draw(screen)
