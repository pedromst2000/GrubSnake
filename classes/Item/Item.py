import pygame as game
from pygame import Vector2
import random
from settings.settings import CELL_SIZE, CELL_NUMBER_X, CELL_NUMBER_Y


class Item:
    def __init__(self, snake_body: list[Vector2], image_path: str):
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

    def randomize_position(self, snake_body: list[Vector2], forbidden_positions=None):
        """
        Randomize the position of the item, avoiding the snake's body and any forbidden positions.
        """
        if forbidden_positions is None:
            forbidden_positions = []

        while True:
            x = random.randint(0, CELL_NUMBER_X - 1)
            y = random.randint(0, CELL_NUMBER_Y - 1)
            candidate_pos = Vector2(x, y)
            if (
                candidate_pos not in snake_body
                and candidate_pos not in forbidden_positions
            ):
                self.pos = candidate_pos
                break

    def spawn_poisons(
        snake_body: list[Vector2], apple_pos: Vector2, existing_poisons: list[Vector2]
    ):
        """
        Spawn 1–9 poisons on the map at random positions, avoiding snake, apple, and other poisons.
        """
        poisons = []
        forbidden_positions = snake_body + [apple_pos] + existing_poisons
        num_poisons = random.randint(1, 9)
        attempts = 0
        max_attempts = num_poisons * 10

        while len(poisons) < num_poisons and attempts < max_attempts:
            x = random.randint(0, CELL_NUMBER_X - 1)
            y = random.randint(0, CELL_NUMBER_Y - 1)
            candidate_pos = Vector2(x, y)
            if (
                candidate_pos not in forbidden_positions
                and candidate_pos not in poisons
            ):
                poisons.append(candidate_pos)
            attempts += 1

        print(f"Spawned {len(poisons)} poisons.")
        return poisons
