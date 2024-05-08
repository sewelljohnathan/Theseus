"""Button Class."""

import pygame

from text import draw_text


class Button:
    """Abstract Button creation."""

    def __init__(
        self,
        text,
        x,
        y,
        w,
        h,
        func,
        color1=(0, 125, 175),
        color2=(0, 75, 225),
        text_color=(0, 0, 0),
        font_name="freesansbold.ttf",
        font_size=20,
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

    def draw(self, screen: pygame.Surface):
        """Draw the button."""
        button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
            mouse_x > self.x
            and mouse_x < self.x + self.w
            and mouse_y > self.y
            and mouse_y < self.y + self.h
        ):
            pygame.draw.rect(screen, self.color2, button_rect, border_radius=5)
            if pygame.mouse.get_pressed()[0]:
                self.func()
        else:
            pygame.draw.rect(screen, self.color1, button_rect, border_radius=5)

        draw_text(
            screen,
            self.text,
            self.x + 10,
            self.y + self.h / 2 - self.font_size / 2,
            self.w,
            self.h,
            self.text_color,
            self.font_name,
            self.font_size,
        )
