"""Mini Game Wheel Scene class."""

import pygame

from gamestate import GameState
from text import TextWrapper
from scenes.mini_game_scene import MiniGameScene


class MGSIMON(MiniGameScene):
    """Simon Says Mini Game Scene."""

    def __init__(self):
        """Initialize Simon Says Mini Game Scene."""
        screen = GameState().screen
        self.center = (screen.get_width() / 2, screen.get_height() / 2)
        self.text_wrapper = TextWrapper(
                '0', (self.center[0]-20, self.center[1] / 2),
                font_size=40, color=pygame.Color(255, 255, 255),
        )

        self.arrow = Arrow('right')

    def run(self):
        """Draw the Simon Says Mini Game scene."""
        game_state = GameState()
        game_state.screen.fill((100, 0, 255))

        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.text_wrapper = TextWrapper(
                game_state.key_press,  # f'{mouse_x:02d},{mouse_y:02d}',
                (self.center[0] - 40, self.center[1] / 2),
                font_size=40, color=pygame.Color(255, 255, 255),
        )
        """
        if (game_state.key_press in self.arrow.directions):
            self.arrow.change_dir(game_state.key_press)

        self.arrow.draw(self.center)
        self.text_wrapper.draw()


class Arrow():
    """Abstract Arrow Creation."""

    def __init__(self,
                 dir: str,
                 size: int = 4,
                 color1: pygame.Color = (150, 0, 150),
                 color2: pygame.Color = (125, 0, 125),
                 ):
        """Initialize the arrow."""
        self.dir = dir
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.directions = {"right": 0,
                           "down": 90,
                           "left": 180,
                           "up": 270,
                           "d": 0,
                           "s": 90,
                           "a": 180,
                           "w": 270}
        self.change_dir(self.dir)

    def draw(self,
             pos: tuple[float, float]):
        """Draw the arrow."""
        game_state = GameState()

        points = [tuple(b + (self.size * a) for a, b in zip(t, pos))
                  for t in self.grid]
        pygame.draw.polygon(game_state.screen, self.color1, points)

    def rotate_grid_clcws(self, rot: int):
        """Rotate the grid."""
        match rot:
            case 90:
                self.grid = [tuple(row[::-1]) for row in self.grid]
            case 180:
                self.grid = [tuple(-x for x in row) for row in self.grid]
            case 270:
                self.grid = [tuple(row[::-1]) for row in self.grid[::-1]]
                self.grid = [tuple(-x for x in row) for row in self.grid]

    def change_dir(self, dir):
        """Change the direction of the arrow."""
        self.dir = dir
        points = [(0, 4), (8, 4), (8, 0), (15, 7),
                  (15, 8), (8, 15), (8, 11), (0, 11),]

        self.grid = [tuple(a - b for a, b in zip(t, (8, 8))) for t in points]
        self.rotate_grid_clcws(self.directions[self.dir])
