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

    def __init__(self, image_path: str, width: int, height: int, x: int | None = None):
        """
        :param image_path: Path to the obstacle image.
        :param width: How many cells wide the obstacle is.
        :param height: How many cells high the obstacle is.
        :param x: optional fixed X column to spawn at (grid coordinate).
        """
        # Clamp width and height to at least 1
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

    def draw(self, screen: game.Surface):
        """
        Draw the obstacle at its grid-aligned position (rounded y).

        :param screen: Pygame surface to draw on.

        """
        pixel_y: int = int(self.y) * CELL_SIZE
        if pixel_y + (self.height * CELL_SIZE) >= 0 and pixel_y < SCREEN_HEIGHT:
            screen.blit(self.image, (self.x * CELL_SIZE, pixel_y))

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

    def spawn_obstacle_row(self, obstacle_width: int, obstacle_height: int, count: int):
        """
        Spawn `count` obstacles distributed evenly across the top row.

        :param obstacle_width: Width of each obstacle in grid cells.
        :param obstacle_height: Height of each obstacle in grid cells.
        :param count: Number of obstacles to spawn in the row (will be clamped to fit).
        """
        width: int = max(1, int(obstacle_width))
        total_slots: int = CELL_NUMBER_X

        # Use a layout width that cannot exceed the grid to avoid negative spacing.
        layout_width: int = min(width, total_slots)

        # Maximum number of obstacles that can fit given the obstacle width.
        max_count: int = max(1, total_slots // layout_width)

        # Clamp requested count to a sensible range.
        count: int = max(1, min(int(count), max_count))

        total_occupied: int = count * layout_width
        leftover: int = total_slots - total_occupied
        gaps: int = count + 1  # slots before/between/after obstacles

        base_gap: int = leftover // gaps if gaps > 0 else 0
        extra: int = leftover % gaps if gaps > 0 else 0

        current_x: int = 0
        for i in range(count):
            # gap before this obstacle
            gap_size = base_gap + (1 if extra > 0 else 0)
            if extra > 0:
                extra -= 1
            current_x += gap_size

            # instantiate obstacle at column current_x
            ob: Obstacle = Obstacle(
                "assets/graphics/items/trap.png",
                width=width,
                height=obstacle_height,
                x=current_x,
            )
            self.obstacles.append(ob)

            # move past this obstacle for next iteration
            current_x += layout_width

    def is_off_screen(self) -> bool:
        """
        Return whether the obstacle has moved past the bottom edge of the screen.
        An obstacle is considered off-screen if its top edge has reached or exceeded SCREEN_HEIGHT.

        Returns:
            bool: True if the obstacle is off the bottom of the screen, False otherwise.
        """

        return self.y * CELL_SIZE >= SCREEN_HEIGHT
