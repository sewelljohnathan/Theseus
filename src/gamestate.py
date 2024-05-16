"""GameState singleton class."""

import pygame

singleton = None


class GameState:
    """GameState class."""

    screen: pygame.Surface

    def __new__(cls):
        """Generate singleton object."""
        global singleton

        if singleton is None:
            singleton = super().__new__(cls)

        return singleton
