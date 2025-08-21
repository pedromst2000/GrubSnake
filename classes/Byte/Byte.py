import pygame as game
from pygame import Vector2
import random
from utils.settings import CELL_SIZE, CELL_NUMBER_X, CELL_NUMBER_Y


class Byte:
    def __init__(self, snake_body: list[Vector2]):
        """
        Initialize the Byte object with its position and image.
        """
        self.image = game.image.load("assets/graphics/byte.png").convert_alpha()
        self.pos = Vector2(0, 0)
        self.randomize_position(snake_body)  # Randomize the initial position of the Byte

    def draw_byte(self, screen: game.Surface):
        """
        Draw the Byte object on the given surface.
        """
        byte_rect = game.Rect(
            int(self.pos.x * CELL_SIZE),
            int(self.pos.y * CELL_SIZE),
            CELL_SIZE,
            CELL_SIZE
        )
        screen.blit(self.image, byte_rect)

    def randomize_position(self, snake_body: list[Vector2]):
        """
        Randomize the position of the Byte object inside map bounds
        """
        while True:
            x = random.randint(0, CELL_NUMBER_X - 1)
            y = random.randint(0, CELL_NUMBER_Y - 1)
            candidate_pos = Vector2(x, y)
            
            if candidate_pos not in snake_body:
                self.pos = candidate_pos # Set the position to the new candidate position
                return # Exit the loop if the position is valid
