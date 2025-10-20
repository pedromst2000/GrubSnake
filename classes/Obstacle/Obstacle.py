import math
import pygame as game
import random
from settings.settings import CELL_NUMBER_X, CELL_SIZE, SCREEN_HEIGHT


class Obstacle:
    """
    Class to manage obstacles in the game.
    Supports multi-cell obstacles (width x height).
    Optional `x` param to specify column; if None, chooses randomly.
    """

    def __init__(
        self, image_path: str, width: int = 2, height: int = 2, x: int | None = None
    ):
        """
        :param image_path: Path to the obstacle image.
        :param width: How many cells wide the obstacle is (defaults to 2).
        :param height: How many cells high the obstacle is (defaults to 2).
        :param x: optional fixed X column to spawn at (grid coordinate).
        """
        # ensure at least 1 and keep width/height as ints
        self.width: int = max(1, int(width))
        self.height: int = max(1, int(height))

        raw_img: game.Surface = game.image.load(image_path).convert_alpha()
        self.image: game.Surface = game.transform.scale(
            raw_img, (CELL_SIZE * self.width, CELL_SIZE * self.height)
        )

        # Choose random X if not specified or out of bounds
        if x is None:
            self.x: int = random.randint(0, max(0, CELL_NUMBER_X - self.width))
        else:
            # clamp to valid range
            self.x: int = max(0, min(x, max(0, CELL_NUMBER_X - self.width)))

        # Start just above the visible screen so the row enters smoothly
        self.y: int = -self.height
        self.pos: game.math.Vector2 = game.math.Vector2(self.x, self.y)

    def move(self, speed: float):
        """
        Move the obstacle down by fractional grid units (speed in grid cells per update).

        :param speed: Speed in grid cells per update (can be fractional).
        """
        self.y += speed
        self.pos: game.math.Vector2 = game.math.Vector2(self.x, self.y)

    def get_cells(self) -> list[game.math.Vector2]:
        """
        Return all grid cells occupied by this obstacle as Vector2s
        using integer (grid) coordinates (floor of y).

        Returns:
            list[game.math.Vector2]: List of grid cells occupied by the obstacle.
        """
        base_y: int = int(math.floor(self.y))  # base y grid coordinate
        cells: list[game.math.Vector2] = []
        for dx in range(self.width):
            for dy in range(self.height):
                cells.append(game.math.Vector2(self.x + dx, base_y + dy))
        return cells

    def spawn_obstacle_row(self, obstacle_width: int, obstacle_height: int, gap: int):
        """
        Spawn a row of obstacles at the top of the screen.

        :param obstacle_width: Width of each obstacle in grid cells.
        :param obstacle_height: Height of each obstacle in grid cells.
        :param gap: Minimum gap between obstacles in grid cells.

        """
        width: int = max(1, int(obstacle_width))
        gap: int = max(0, int(gap))

        step: int = width + gap
        if step <= 0:
            step: int = width + 1

        # Compute centered start offset so obstacles are centered across entire grid
        total_slots: int = CELL_NUMBER_X
        # number of full placements that fit
        placements: int = total_slots // step
        # try to place as many as fit; if there's leftover columns, center them
        used_columns: int = (
            placements * step - gap
        )  # last obstacle doesn't need trailing gap
        leftover: int = total_slots - used_columns
        start_offset: int = leftover // 2  # integer center offset

        x: int = start_offset
        spawned: int = 0
        while x + width <= CELL_NUMBER_X:
            # instantiate obstacle at column x
            ob: Obstacle = Obstacle(
                "assets/graphics/items/trap.png",
                width=width,
                height=obstacle_height,
                x=x,
            )
            self.obstacles.append(ob)
            spawned += 1
            x += step

    def is_off_screen(self) -> bool:
        """
        Return whether the obstacle has moved past the bottom edge of the screen.
        Determines if the obstacle's bottom (self.y + self.height), scaled by CELL_SIZE,
        has reached or exceeded SCREEN_HEIGHT.

        Returns:
            bool: True if the obstacle is off the bottom of the screen, False otherwise.
        """

        return (self.y + self.height) * CELL_SIZE >= SCREEN_HEIGHT

    def draw(self, screen: game.Surface):
        """
        Draw the obstacle at its grid-aligned position (rounded y).

        :param screen: Pygame surface to draw on.

        """
        pixel_y: int = int(self.y) * CELL_SIZE
        if pixel_y + (self.height * CELL_SIZE) >= 0 and pixel_y < SCREEN_HEIGHT:
            screen.blit(self.image, (self.x * CELL_SIZE, pixel_y))
