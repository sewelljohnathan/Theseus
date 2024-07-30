"""Mini Game Wheel Scene class."""

import pygame
import math

from gamestate import GameState
from text import TextWrapper
from scenes.mini_game_scene import MiniGameScene


class MGWheel(MiniGameScene):
    """Wheel Mini Game Scene."""

    def __init__(self):
        """Initialize Wheel Mini Game Scene."""
        screen = GameState().screen
        self.center = (screen.get_width() / 2, screen.get_height() / 2)
        self.wheel = Wheel(self.center, 150, 40)
        self.ball = Ball(self.wheel.center, 20, 20, self.wheel.radius)
        self.timer = Timer(0)
        self.start = False
        self.text_wrapper = TextWrapper(
            '0:00', (self.center[0] - 40, 150), font_size=40,
            color=pygame.Color(255, 255, 255),
        )

    def run(self):
        """Update and draw the Wheel Mini Game scene."""
        game_state = GameState()
        game_state.screen.fill((100, 0, 255))

        if self.ball.clicked:
            self.start = True

        time = game_state.clock.get_time() / 1000.0
        if self.start:
            self.ball.move(time)
            self.timer.add_time(time * 1000)

        self.text_wrapper = TextWrapper(
            self.timer.display(), (self.center[0] - 40, 150), font_size=40,
            color=pygame.Color(255, 255, 255),
        )

        self.wheel.draw()
        self.ball.draw()
        self.text_wrapper.draw()


class Wheel():
    """Class representing a wheel in the mini game."""

    def __init__(self,
                 center: tuple[float, float],
                 radius: float,
                 width: float,
                 color: pygame.Color = (125, 125, 175),
                 ):
        """Initialize the wheel."""
        self.color = color
        self.center = center
        self.radius = radius
        self.width = width

    def draw(self):
        """Draw the wheel."""
        game_state = GameState()
        pygame.draw.circle(game_state.screen, self.color, self.center,
                           self.radius, self.width)


class Ball():
    """Class representing a ball in the mini game."""

    def __init__(self,
                 offset: tuple[float, float],
                 radius: float,
                 size: float,
                 ring: float,
                 color1: pygame.Color = (150, 0, 150),
                 color2: pygame.Color = (125, 0, 125),
                 clicked: bool = False,
                 pos: float = -.5 * math.pi,
                 vel: float = 1,
                 acel: float = .2,
                 max_vel: float = 2 * math.pi,
                 ):
        """Initialize the ball."""
        self.color1 = color1
        self.color2 = color2
        self.center = offset
        self.ring = ring
        self.radius = radius
        self.size = size
        self.clicked = clicked
        self.pos = pos
        self.vel = vel
        self.acel = acel
        self.max_vel = max_vel

        self.time = 0
        self.cur_sec = 0
        self.prev_sec = self.cur_sec
        self.update_pos(self.pos, self.pos)

    def draw(self):
        """Draw the ball."""
        game_state = GameState()
        self.time += game_state.clock.get_time() / 1000
        self.cur_sec = math.floor(self.time)

        x = self.center[0] + (self.ring - self.radius) * math.cos(self.pos_x)
        y = self.center[1] + ((self.ring - self.radius) * math.sin(self.pos_y))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.is_mouse_over(mouse_x, mouse_y, x, y):
            pygame.draw.circle(game_state.screen, self.color2,
                               (x, y), self.size)
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
        else:
            pygame.draw.circle(game_state.screen, self.color1,
                               (x, y), self.size)

    def move(self, time: float):
        """Update the ball physics."""
        # self.vel += self.acel * time
        # self.vel = self.max_vel if self.vel > self.max_vel else self.vel
        self.vel = min(self.vel + self.acel * time, self.max_vel)
        self.pos += (self.vel * time)
        self.update_pos(self.pos, self.pos)

    def update_pos(self, pos_x: float, pos_y: float):
        """Update the position of the ball."""
        self.pos_x = pos_x
        self.pos_y = pos_y

    def is_mouse_over(self, mouse_x: float, mouse_y: float,
                      x: float, y: float) -> bool:
        """Check if the mouse is over the ball."""
        return (
            x - self.radius < mouse_x < x + self.radius and
            y - self.radius < mouse_y < y + self.radius
        )


class Timer():
    """Abstract Stop watch Creation."""

    def __init__(self, time: int):
        """Initialize the timer."""
        self.time = time

    def add_time(self, time: int):
        """Update the time on the timer."""
        self.time += int(time)

    def display(self):
        """Display the time in 00:00 format."""

        # splits the time in milliseconds, into seconds and milliseconds
        sec = self.time // 1000
        mil = int(self.time % 1000 / 10)

        return f'{sec:02d}:{mil:02d}'
