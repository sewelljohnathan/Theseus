"""Wrapper for printed text to the screen."""

import time

import pygame


class TextWrapper:
    """Wrapper class for text."""

    def __init__(
        self,
        text: str,
        rect: tuple[int, int, int, int],
        font_name: str = "freesansbold.ttf",
        font_size: int = 20,
        color: tuple[int, int, int] = (0, 0, 0),
    ):
        """Initialize TextWrapper."""
        self.text = text
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(font_name, font_size)
        self.font_height = self.font.size("Tg")[1]
        self.color = color

    def draw(self, screen: pygame.Surface):
        """Draw text."""
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.rect)


class DynamicTextWrapper(TextWrapper):
    """Wrapper class for dynamic text."""

    def __init__(
        self,
        text: str,
        rect: tuple[int, int, int, int],
        font_name: str = "freesansbold.ttf",
        font_size: int = 20,
        color: tuple[int, int, int] = (0, 0, 0),
        display_speed: float = 50,
        display_delay: float = 0,
    ):
        """Initialize DynamicTextWrapper."""
        super().__init__(text, rect, font_name, font_size, color)
        self.display_speed = display_speed
        self.display_delay = display_delay

        self.display_start = None

    def draw(self, screen: pygame.Surface, debug=False):
        """
        Draw dynamic text with wrapping.

        Modified from https://www.pygame.org/wiki/TextWrap
        """
        # Draw debug background
        if debug:
            debug_surface = pygame.Surface((self.rect.width, self.rect.height))
            debug_surface.set_alpha(200)
            debug_surface.fill((255, 255, 255))
            screen.blit(debug_surface, (self.rect.x, self.rect.y))

        if self.display_start is None:
            self.display_start = time.time()

        # Get the time delta from when the text should begin to render
        time_delta = time.time() - self.display_start - self.display_delay
        if time_delta < 0:
            return

        # Get the number of characters to display
        characters_to_blit = int(time_delta * self.display_speed)
        characters_to_blit = min(characters_to_blit, len(self.text))

        y = self.rect.top
        lineSpacing = -2

        text = self.text
        characters_blitted = 0
        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + self.font_height > self.rect.bottom:
                break

            # determine maximum width of line
            while self.font.size(text[:i])[0] < self.rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # Correct if the line is more than should be blitted
            if characters_blitted + i > characters_to_blit:
                i = characters_to_blit - characters_blitted

            # render the line and blit it to the surface
            image = self.font.render(text[:i], True, self.color)
            screen.blit(image, (self.rect.left, y))
            y += self.font_height + lineSpacing

            # remove the text we just blitted
            text = text[i:]
            characters_blitted += i
