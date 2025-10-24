from pygame.math import Vector2  # For the draw of the snake with vectors
import pygame as game
from settings.settings import CELL_SIZE
from settings.settings import CELL_NUMBER_X, CELL_NUMBER_Y
from globals.states.score import apples_eaten as score_state


class Snake:
    """
    Handles drawing (head/body/tail sprites), movement, direction, growth, reset.
     Body positions are on the grid (`Vector2` of cell coordinates).
    """

    def __init__(self):
        """
        Initialize the snake's position and body.
        """
        # Calculate center position based on settings
        center_x: int = CELL_NUMBER_X // 2
        center_y: int = CELL_NUMBER_Y // 2
        self.body: list[Vector2] = [
            Vector2(center_x, center_y),
            Vector2(center_x - 1, center_y),
            Vector2(center_x - 2, center_y),
        ]  # body of the snake, starting with 3 segments in the center
        self.direction: Vector2 = Vector2(1, 0)  # the snake starts moving right
        self.new_block: bool = False  # To manage the growth of the snake

        def load_sprite(path: str) -> game.Surface:
            """
            Load and scale a sprite from the given path.

            :param path: The file path to the sprite image.

            Returns:
               game.Surface: The loaded and scaled sprite image.
            """
            img: game.Surface = game.image.load(path).convert_alpha()
            return game.transform.smoothscale(img, (CELL_SIZE, CELL_SIZE))

        # Loading sprites of the Snake
        self.head_up: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/head_up.png"
        )
        self.head_down: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/head_down.png"
        )
        self.head_left: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/head_left.png"
        )
        self.head_right: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/head_right.png"
        )

        self.tail_up: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/tail_up.png"
        )
        self.tail_down: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/tail_down.png"
        )
        self.tail_left: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/tail_left.png"
        )
        self.tail_right: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/tail_right.png"
        )

        self.body_vertical: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/body_vertical.png"
        )
        self.body_horizontal: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/body_horizontal.png"
        )
        self.body_tr: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/body_top_right.png"
        )
        self.body_tl: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/body_top_left.png"
        )
        self.body_br: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/body_bottom_right.png"
        )
        self.body_bl: game.Surface = load_sprite(
            "assets/graphics/snake_sprites/body_bottom_left.png"
        )

    def update_head_graphics(self):
        """
        Update the graphics for the snake's head based on its direction.
        """
        relation: Vector2 = self.body[0] - self.body[1]
        if relation == Vector2(1, 0):
            self.head_graphics: game.Surface = self.head_right  # Right
        elif relation == Vector2(-1, 0):
            self.head_graphics: game.Surface = self.head_left  # Left
        elif relation == Vector2(0, 1):
            self.head_graphics: game.Surface = self.head_down  # Down
        else:  # Vector2(0, -1)
            self.head_graphics: game.Surface = self.head_up  # Up

    def update_body_graphics(self):
        """
        Update the graphics for the snake's body based on its segments.
        """
        relation: Vector2 = self.body[-1] - self.body[-2]
        if relation == Vector2(1, 0):
            self.tail_graphics: game.Surface = self.tail_right
        elif relation == Vector2(-1, 0):
            self.tail_graphics: game.Surface = self.tail_left
        elif relation == Vector2(0, 1):
            self.tail_graphics: game.Surface = self.tail_down
        else:  # Vector2(0, -1)
            self.tail_graphics: game.Surface = self.tail_up

    def draw_snake(self, screen: game.Surface):
        """
        Method class for drawing the snake on the screen.

        :param screen: The game screen where the snake will be drawn.
        """
        self.update_head_graphics()
        self.update_body_graphics()

        for index, block in enumerate(self.body):
            x_pos: int = int(block.x * CELL_SIZE)
            y_pos: int = int(block.y * CELL_SIZE)
            rect: game.Rect = game.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:  # head
                screen.blit(self.head_graphics, rect)
            elif index == len(self.body) - 1:  # tail
                screen.blit(self.tail_graphics, rect)
            else:  # body segment
                prev_block: Vector2 = self.body[index + 1] - block
                next_block: Vector2 = self.body[index - 1] - block

                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, rect)
                else:
                    # corners
                    if (prev_block.x == -1 and next_block.y == -1) or (
                        next_block.x == -1 and prev_block.y == -1
                    ):
                        screen.blit(self.body_tl, rect)
                    elif (prev_block.x == -1 and next_block.y == 1) or (
                        next_block.x == -1 and prev_block.y == 1
                    ):
                        screen.blit(self.body_bl, rect)
                    elif (prev_block.x == 1 and next_block.y == -1) or (
                        next_block.x == 1 and prev_block.y == -1
                    ):
                        screen.blit(self.body_tr, rect)
                    elif (prev_block.x == 1 and next_block.y == 1) or (
                        next_block.x == 1 and prev_block.y == 1
                    ):
                        screen.blit(self.body_br, rect)

    def move_growth(self):
        """
        Method class for moving the snake in the current direction. Handles growth if needed.
        """
        if not self.new_block:  # If the snake is not growing
            body_copy: list[Vector2] = self.body[
                :-1
            ]  # Copy the body except the last block
        else:  # If the snake is growing
            body_copy: list[Vector2] = self.body[:]  # Copy the entire body
            self.new_block: bool = False  # Reset the growth flag

        new_head: Vector2 = self.body[0] + self.direction  # Calculate new head position
        body_copy.insert(0, new_head)  # Insert new head into the body
        self.body: list[Vector2] = body_copy  # Update the snake's body

    def grow(self):
        """
        Method class for adding a block to the snake. (Grow of the Snake)
        """
        self.new_block: bool = True  # Set the flag to indicate the snake should grow

    def reset(self):
        """
        Method class for resetting the snake to its initial state.
        """
        center_x: int = CELL_NUMBER_X // 2
        center_y: int = CELL_NUMBER_Y // 2
        self.body: list[Vector2] = [
            Vector2(center_x, center_y),
            Vector2(center_x - 1, center_y),
            Vector2(center_x - 2, center_y),
        ]  # Reset to initial 3 segments in the center
        self.direction: Vector2 = Vector2(1, 0)  # Reset direction to right
        self.new_block: bool = False  # Reset growth flag
