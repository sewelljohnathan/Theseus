"""PauseScreen and related classes to manage pause state and display menus."""

import pygame
from dataclasses import dataclass
from typing import Callable

from scenes.scene import Scene
from gamestate import GameState
from text import TextWrapper
from button import Button


class PauseHandler:
    """Class to manage the pause state of the game."""

    def __init__(self):
        """Initialize PauseHandler with an unpaused state."""
        self.is_paused = False

    def run(self):
        """Update the pause state based on user input."""
        game_state = GameState()

        # Toggle pause state when 'escape' key is pressed
        if not self.is_paused and game_state.key_press == 'escape':
            self.is_paused = True
            game_state.scene = PauseScreen(game_state.scene, "Pause", self)

    def unpause(self):
        """Reset the paused state."""
        self.is_paused = False


@dataclass
class Element:
    """Dataclass to assist in creating drawable structures."""
    type: str
    text: str
    action: str = None


class MenuScreen(Scene):
    """Base class for screens in the pause menu."""

    def __init__(self, prev_scene: Scene, title: str):
        """Initialize the screen with the previous scene."""
        self.prev_scene = prev_scene
        self.create_title(title)
        self.to_draw = [self.title]

    def run(self):
        """Update the screen data."""
        pass

    def draw(self):
        """Draw the screen data."""
        pass

    def get_func(self, func: str) -> Callable:
        """Get a function in the menu by its name."""
        return lambda *args: None  # Default implementation

    def create_title(self, title: str):
        """Create a title for the menu screen."""
        game_state = GameState()
        x, y = game_state.screen.get_size()
        self.title = TextWrapper(title, (x / 2 - 100, 100, 200, 50),
                                 font_size=40)

    def create_in_order(
            self,
            init_pos: tuple[int, int],
            size: tuple[int, int],
            offset: tuple[int, int],
            *elements: Element,
            align: str = 'center',
    ) -> list:
        """Return a list of drawable objects created
        \nin order based on the given parameters."""

        objects = []
        alignment = {
            'center': size[0] / 2,
            'left': size[0],
            'right': 0
        }.get(align, size[0] / 2)

        for i, element in enumerate(elements):
            x = init_pos[0] + (i * offset[0]) - alignment
            y = init_pos[1] + (i * offset[1]) - size[1] / 2
            if element.type == "button":
                objects.append(Button(
                    element.text,
                    x, y, size[0], size[1], self.get_func(element.action),
                    pygame.Color(120, 120, 120), pygame.Color(150, 150, 150)
                    ))
            elif element.type == "label":
                objects.append(TextWrapper(
                    element.text, (x, y, size[0], size[1]),
                    font_size=(element.action if element.action
                               is not None else 20)
                        ))
        return objects


class PauseScreen(MenuScreen):
    """Class to display the pause screen with necessary components."""

    def __init__(self, prev_scene: Scene, title: str,
                 pause_handler: PauseHandler):
        """Initialize the PauseScreen with the previous scene and a
        pause handler."""
        super().__init__(prev_scene, title)
        self.pause_handler = pause_handler
        game_state = GameState()
        x, y = game_state.screen.get_size()

        self.to_draw += self.create_in_order(
            (x/2, 200), (200, 50), (0, 100),
            Element('button', 'Resume', 'unpause'),
            Element('button', 'Controls', 'goto_controls')
        )

    def run(self):
        """Update the pause screen."""
        self.draw()

    def draw(self):
        """Draw the pause screen."""
        game_state = GameState()
        game_state.screen.fill((80, 80, 80))
        for obj in self.to_draw:
            obj.draw()

    def unpause(self):
        """Unpauses the game and return to the original scene."""
        self.pause_handler.unpause()
        game_state = GameState()
        game_state.scene = self.prev_scene

    def goto_controls(self):
        """Changes scene to the controls screen"""
        game_state = GameState()
        game_state.scene = ControlsScreen(self, "Controls")

    def get_func(self, func: str) -> Callable:
        """Get a function in the pause menu by its name."""
        return {
            'unpause': self.unpause,
            'goto_controls': self.goto_controls,
        }.get(func, lambda *args: None)


class ControlsScreen(MenuScreen):
    """Class to display the controls menu."""

    def __init__(self, scene: Scene, title: str):
        """Initialize the ControlsScreen with the previous scene."""
        super().__init__(scene, title)

        game_state = GameState()
        x, y = game_state.screen.get_size()

        # Create labels representing actions
        self.to_draw += self.create_in_order(
            (x/2 - 215, 215), (200, 50), (0, 75),
            Element('label', 'Up', 25),
            Element('label', 'Left', 25),
            Element('label', 'Down', 25),
            Element('label', 'Right', 25),
        )
        # Create buttons to match each action label
        self.to_draw += self.create_in_order(
            (x/2 - 125, 200), (200, 50), (250, 0),
            Element('button', 'W', 'None'),
            Element('button', 'Up Arrow', 'None'),
        )
        self.to_draw += self.create_in_order(
            (x/2 - 125, 275), (200, 50), (250, 0),
            Element('button', 'A', 'None'),
            Element('button', 'Left Arrow', 'None'),
        )
        self.to_draw += self.create_in_order(
            (x/2 - 125, 350), (200, 50), (250, 0),
            Element('button', 'S', 'None'),
            Element('button', 'Down Arrow', 'None'),
        )
        self.to_draw += self.create_in_order(
            (x/2 - 125, 425), (200, 50), (250, 0),
            Element('button', 'D', 'None'),
            Element('button', 'Right Arrow', 'None'),
        )
        # Create button to return to previous screen
        self.to_draw += self.create_in_order(
            (x/2, 600), (200, 50), (0, 0),
            Element('button', 'Back', 'return_to_pause_screen')
        )

    def run(self):
        """Update the controls menu."""
        self.draw()

    def draw(self):
        """Draw the controls menu."""
        game_state = GameState()
        game_state.screen.fill((80, 80, 80))
        for obj in self.to_draw:
            obj.draw()

    def return_to_pause_screen(self):
        """Changes scene back to the pause menu"""
        game_state = GameState()
        game_state.scene = self.prev_scene

    def get_func(self, func: str) -> Callable:
        """Get a function in the controls menu by its name."""
        return {
            'return_to_pause_screen': self.return_to_pause_screen,
        }.get(func, lambda *args: None)
