import pygame as game
from pygame import Vector2
import random
from settings.settings import CELL_SIZE, CELL_NUMBER_X, CELL_NUMBER_Y


class Item:
    """
    Class representing an item in the game, such as an apple or poison.
    """

    def __init__(self, snake_body: list[Vector2], image_path: str):
        """
        Initialize an item (like apple) at a valid position.

        :param snake_body: List of Vector2 positions occupied by the snake.
        :param image_path: Path to the item's image file.
        """
        raw_image: game.Surface = game.image.load(image_path).convert_alpha()
        self.image: game.Surface = game.transform.smoothscale(
            raw_image, (CELL_SIZE, CELL_SIZE)
        )
        self.pos: Vector2 = Vector2(0, 0)
        self.randomize_position(snake_body)

    def draw(self, screen: game.Surface):
        """
        Draw the item on the screen.

        :param screen: The game surface to draw the item on.
        """
        rect: game.Rect = game.Rect(
            int(self.pos.x * CELL_SIZE),
            int(self.pos.y * CELL_SIZE),
            CELL_SIZE,
            CELL_SIZE,
        )
        screen.blit(self.image, rect)

    def randomize_position(self, snake_body: list[Vector2], forbidden_positions=None):
        """
        Place item randomly, avoiding snake and forbidden positions.

        :param snake_body: List of Vector2 positions occupied by the snake.
        :param forbidden_positions: List of Vector2 positions to avoid.
        """
        if forbidden_positions is None:
            forbidden_positions: list[Vector2] = []

        while True:
            x: int = random.randint(0, CELL_NUMBER_X - 1)
            y: int = random.randint(0, CELL_NUMBER_Y - 1)
            candidate: Vector2 = Vector2(x, y)
            if candidate not in snake_body and candidate not in forbidden_positions:
                self.pos: Vector2 = candidate
                break

    def spawn_poisons(
        snake_body: list[Vector2], apple_pos: Vector2, level: str
    ) -> list[Vector2]:
        """
        Spawn poisons at valid positions avoiding snake and apple.

        :param snake_body: List of Vector2 positions occupied by the snake.
        :param apple_pos: Vector2 position of the apple.
        :param level: Current game level ("medium" or "hard").
        Returns:
          list[Vector2]: List of Vector2 positions for poisons.
        """
        if level not in ["medium", "hard"]:
            return []

        forbidden: set[tuple[int, int]] = {
            (int(seg.x), int(seg.y)) for seg in snake_body
        }
        forbidden.add((int(apple_pos.x), int(apple_pos.y)))

        if level == "medium":
            count: int = random.randint(8, 18)
        else:  # hard
            count: int = random.randint(5, 10)

        available: list[tuple[int, int]] = [
            (x, y)
            for x in range(CELL_NUMBER_X)
            for y in range(CELL_NUMBER_Y)
            if (x, y) not in forbidden
        ]

        chosen: list[tuple[int, int]] = random.sample(
            available, min(count, len(available))
        )
        poisons: list[Vector2] = [Vector2(x, y) for x, y in chosen]

        return poisons
