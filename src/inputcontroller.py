# Scrapped idea for an input controller to be iterated on
# or used as basis of what to avoid

"""

import pygame
from collections import deque
from gamestate import GameState


class InputController:
    \"""Singleton class to handle keyboard input events.\"""

    _instance = None

    def __new__(cls):
        \"""Ensure only one instance of the class exists.\"""
        if cls._instance is None:
            cls._instance = super(InputController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        \"""Initialize input controller.\"""
        if not hasattr(self, 'initialized'):  # Ensures __init__ runs only once
            self.game_state = GameState()
            self.key_states = {}
            self.key_times = {}
            self.input_buffer = deque()
            self.buffer_time = 0.0
            self.current_time = pygame.time.get_ticks() / 1000.0
            self.double_press_threshold = 0.3  # seconds
            self.long_press_threshold = 0.5  # seconds
            self.input_delay = 0.05  # seconds
            self.actions = ''
            self.pressed = False
            self.held = False
            self.initialized = True

    def key_down(self, key: str):
        \"""Handle key down event.\"""
        if key not in self.key_states or self.key_states[key] == 'released':
            self.key_states[key] = 'pressed'
            self.key_times[key] = self.current_time
            self.input_buffer.append((key, 'pressed', self.current_time))
        elif self.key_states[key] == 'pressed':
            if (self.current_time - self.key_times[key]
               <= self.double_press_threshold):
                self.key_states[key] = 'double_pressed'

    def key_up(self, key: str):
        \"""Handle key up event.\"""
        if key in self.key_states and self.key_states[key] == 'pressed':
            duration = self.current_time - self.key_times[key]
            if duration >= self.long_press_threshold:
                self.key_states[key] = 'long_released'
            else:
                self.key_states[key] = 'short_released'
            self.input_buffer.append((key, 'released', self.current_time))
        else:
            self.key_states[key] = 'released'

    def process(self):
        \"""Process input events from the buffer.\"""
        self.increment_time()

        while (self.input_buffer and self.current_time - self.buffer_time
               >= self.input_delay):
            key, action, event_time = self.input_buffer.popleft()
            self.buffer_time = self.current_time
            self.handle_action(key, action)

    def handle_action(self, key, action):
        \"""Handle buffered key actions.\"""
        if action == 'pressed':
            self.pressed = True
            self.actions = self.map_key_to_action(key)
        elif action == 'released':
            self.pressed = False
            self.held = False
            self.actions = ''

    def map_key_to_action(self, key):
        \"""Map key to corresponding action.\"""
        match key:
            case 'left': return 'left'
            case 'right': return 'right'
            case 'up': return 'up'
            case 'down': return 'down'
            case 'escape': return 'escape'
            case _: return ''

    def increment_time(self):
        \"""Update the current time based on game state.\"""
        self.current_time += pygame.time.get_ticks() / 1000.0

    def get_press(self, press_type):
        \"""Get the current action based on press type.\"""
        if self.pressed:
            if press_type == 's' and not self.held:
                self.held = True
                return self.actions
            if press_type == 'h':
                self.held = True
                return self.actions
        return ''

"""
