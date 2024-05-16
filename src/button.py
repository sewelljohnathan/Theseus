"""Button Class."""

from typing import Callable

import pygame

from gamestate import GameState
from text import TextWrapper


class Button:
    """Abstract Button creation."""

    def __init__(
        self,
        text: str,
        x: float,
        y: float,
        w: float,
        h: float,
        func: Callable,
        color1: pygame.Color = (0, 125, 175),
        color2: pygame.Color = (0, 75, 225),
        text_color: pygame.Color = (0, 0, 0),
        font_name: str = "freesansbold.ttf",
        font_size: float = 20,
    ):
        """Initialize the button."""
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.func = func
        self.color1 = color1
        self.color2 = color2
        self.text_color = text_color
        self.font_name = font_name
        self.font_size = font_size
        self.text_wrapper = TextWrapper(
            text,
            (x + 10, y + h / 2 - font_size / 2, w, h),
            font_name,
            font_size,
            text_color,
        )

    def draw(self):
        """Draw the button."""
        game_state = GameState()

        button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
            mouse_x > self.x
            and mouse_x < self.x + self.w
            and mouse_y > self.y
            and mouse_y < self.y + self.h
        ):
            pygame.draw.rect(
                game_state.screen, self.color2, button_rect, border_radius=5
            )
            if pygame.mouse.get_pressed()[0]:
                self.func()
        else:
            pygame.draw.rect(
                game_state.screen, self.color1, button_rect, border_radius=5
            )

        self.text_wrapper.draw()
