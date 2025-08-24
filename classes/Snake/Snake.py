from pygame.math import Vector2  # For the draw of the snake with vectors
import pygame as game
from utils.settings import CELL_SIZE


class Snake:
    """
    Handles drawing (head/body/tail sprites), movement, direction, growth, reset.
     Body positions are on the grid (Vector2 of cell coordinates).
    """

    def __init__(self):
        """
        Initialize the snake's position and body.

        Vector2: The position of the snake's head.
        """
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = Vector2(1, 0)
        self.new_block = False  # To manage the growth of the snake

        def load_sprite(path: str) -> game.Surface:
            img = game.image.load(path).convert_alpha()
            return game.transform.smoothscale(img, (CELL_SIZE, CELL_SIZE))

        # Loading sprites of the Snake
        self.head_up = load_sprite("assets/graphics/head_up.png")
        self.head_down = load_sprite("assets/graphics/head_down.png")
        self.head_left = load_sprite("assets/graphics/head_left.png")
        self.head_right = load_sprite("assets/graphics/head_right.png")

        self.tail_up = load_sprite("assets/graphics/tail_up.png")
        self.tail_down = load_sprite("assets/graphics/tail_down.png")
        self.tail_left = load_sprite("assets/graphics/tail_left.png")
        self.tail_right = load_sprite("assets/graphics/tail_right.png")

        self.body_vertical = load_sprite("assets/graphics/body_vertical.png")
        self.body_horizontal = load_sprite("assets/graphics/body_horizontal.png")
        self.body_tr = load_sprite("assets/graphics/body_top_right.png")
        self.body_tl = load_sprite("assets/graphics/body_top_left.png")
        self.body_br = load_sprite("assets/graphics/body_bottom_right.png")
        self.body_bl = load_sprite("assets/graphics/body_bottom_left.png")

    def draw_snake(self, screen: game.Surface):
        """
        Method class for drawing the snake.
        """
        self.update_head_graphics()
        self.update_body_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            rect = game.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:  # head
                screen.blit(self.head_graphics, rect)
            elif index == len(self.body) - 1:  # tail
                screen.blit(self.tail_graphics, rect)
            else:  # body segment
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

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

    def update_head_graphics(self):
        """
        Update the graphics for the snake's head based on its direction.
        """
        relation = self.body[0] - self.body[1]
        if relation == Vector2(1, 0):
            self.head_graphics = self.head_right
        elif relation == Vector2(-1, 0):
            self.head_graphics = self.head_left
        elif relation == Vector2(0, 1):
            self.head_graphics = self.head_down
        else:  # Vector2(0, -1)
            self.head_graphics = self.head_up

    def update_body_graphics(self):
        """
        Update the graphics for the snake's body based on its segments.
        """
        relation = self.body[-1] - self.body[-2]
        if relation == Vector2(1, 0):
            self.tail_graphics = self.tail_right
        elif relation == Vector2(-1, 0):
            self.tail_graphics = self.tail_left
        elif relation == Vector2(0, 1):
            self.tail_graphics = self.tail_down
        else:  # Vector2(0, -1)
            self.tail_graphics = self.tail_up

    def move(self):
        """
        Method class for moving the snake.
        """
        if not self.new_block:  # If the snake is not growing
            body_copy = self.body[:-1]  # Copy the body except the last block
        else:  # If the snake is growing
            body_copy = self.body[:]  # Copy the entire body
            self.new_block = False  # Reset the growth flag

        new_head = self.body[0] + self.direction
        body_copy.insert(0, new_head)
        self.body = body_copy

    def add_block(self):
        """
        Method class for adding a block to the snake. (Grow of the Snake)
        """
        self.new_block = True  # Set the flag to indicate the snake should grow

    def reset(self):
        """
        Method class for resetting the snake to its initial state.
        """
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = game.Vector2(1, 0)
        self.new_block = False
