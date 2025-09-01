import pygame as game
from pygame import Vector2
import random
from utils.settings.settings import CELL_SIZE, CELL_NUMBER_X, CELL_NUMBER_Y


class Item:
    def __init__(self, snake_body: list[Vector2], image_path: str):
        """
        Item to represent a collectible or obstacle in the game.
        - snake_body: list of snake segments to avoid when spawning
        - image_path: path to the image file for this item
        """
        raw_image = game.image.load(image_path).convert_alpha()
        self.image = game.transform.smoothscale(raw_image, (CELL_SIZE, CELL_SIZE))
        self.pos = Vector2(0, 0)
        self.randomize_position(snake_body)

    def draw(self, screen: game.Surface):
        """
        Draw the item on the screen.
        """
        item_rect = game.Rect(
            int(self.pos.x * CELL_SIZE),
            int(self.pos.y * CELL_SIZE),
            CELL_SIZE,
            CELL_SIZE,
        )
        screen.blit(self.image, item_rect)

    def randomize_position(self, snake_body: list[Vector2]):
        """
        Randomize position inside map bounds, avoiding snake body.
        """
        while True:
            x = random.randint(0, CELL_NUMBER_X - 1)
            y = random.randint(0, CELL_NUMBER_Y - 1)
            candidate_pos = Vector2(x, y)

            if candidate_pos not in snake_body:
                self.pos = candidate_pos
                return
