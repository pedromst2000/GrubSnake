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

        # Loading sprites of the Snake
        self.head_up = game.image.load("assets/graphics/head_up.png").convert_alpha()
        self.head_down = game.image.load(
            "assets/graphics/head_down.png"
        ).convert_alpha()
        self.head_left = game.image.load(
            "assets/graphics/head_left.png"
        ).convert_alpha()
        self.head_right = game.image.load(
            "assets/graphics/head_right.png"
        ).convert_alpha()

        self.tail_up = game.image.load("assets/graphics/tail_up.png").convert_alpha()
        self.tail_down = game.image.load(
            "assets/graphics/tail_down.png"
        ).convert_alpha()
        self.tail_left = game.image.load(
            "assets/graphics/tail_left.png"
        ).convert_alpha()
        self.tail_right = game.image.load(
            "assets/graphics/tail_right.png"
        ).convert_alpha()

        self.body_vertical = game.image.load(
            "assets/graphics/body_vertical.png"
        ).convert_alpha()
        self.body_horizontal = game.image.load(
            "assets/graphics/body_horizontal.png"
        ).convert_alpha()
        self.body_tr = game.image.load(
            "assets/graphics/body_top_right.png"
        ).convert_alpha()
        self.body_tl = game.image.load(
            "assets/graphics/body_top_left.png"
        ).convert_alpha()
        self.body_br = game.image.load(
            "assets/graphics/body_bottom_right.png"
        ).convert_alpha()
        self.body_bl = game.image.load(
            "assets/graphics/body_bottom_left.png"
        ).convert_alpha()

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

            # if index == 0:  # head of the snake
            #     head_rel = self.body[1] - game.Vector2(self.body[0])
            #     if head_rel == game.Vector2(1, 0):
            #         screen.blit(self.head_left, rect)
            #     elif head_rel == game.Vector2(-1, 0):
            #         screen.blit(self.head_right, rect)
            #     elif head_rel == game.Vector2(0, 1):
            #         screen.blit(self.head_up, rect)
            #     elif head_rel == game.Vector2(0, -1):
            #         screen.blit(self.head_down, rect)

            # elif index == len(self.body) - 1:  # tail of the snake
            #     tail_rel = self.body[-2] - game.Vector2(self.body[-1])
            #     if tail_rel == game.Vector2(1, 0):
            #         screen.blit(self.tail_left, rect)
            #     elif tail_rel == game.Vector2(-1, 0):
            #         screen.blit(self.tail_right, rect)
            #     elif tail_rel == game.Vector2(0, 1):
            #         screen.blit(self.tail_up, rect)
            #     elif tail_rel == game.Vector2(0, -1):
            #         screen.blit(self.tail_down, rect)

            # else:  # body of the snake
            #     prev_block = game.Vector2(self.body[index + 1]) - game.Vector2(block)
            #     next_block = game.Vector2(self.body[index - 1]) - game.Vector2(block)
            #     if prev_block.x == next_block.x:  # vertical body
            #         screen.blit(self.body_vertical, rect)
            #     elif prev_block.y == next_block.y:  # horizontal body
            #         screen.blit(self.body_horizontal, rect)
            #     else:  # corners of the snake
            #         if (prev_block.x == -1 and next_block.y == -1) or (
            #             next_block.x == -1 and prev_block.y == -1
            #         ):
            #             screen.blit(self.body_tl, rect)
            #         elif (prev_block.x == -1 and next_block.y == 1) or (
            #             next_block.x == -1 and prev_block.y == 1
            #         ):
            #             screen.blit(self.body_bl, rect)
            #         elif (prev_block.x == 1 and next_block.y == -1) or (
            #             next_block.x == 1 and prev_block.y == -1
            #         ):
            #             screen.blit(self.body_tr, rect)
            #         elif (prev_block.x == 1 and next_block.y == 1) or (
            #             next_block.x == 1 and prev_block.y == 1
            #         ):
            #             screen.blit(self.body_br, rect)

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

        # head_relation = self.body[1] - self.body[0]
        # if head_relation == Vector2(1, 0):
        #     self.head_graphics = self.head_right
        # elif head_relation == Vector2(-1, 0):
        #     self.head_graphics = self.head_left
        # elif head_relation == Vector2(0, 1):
        #     self.head_graphics = self.head_down
        # elif head_relation == Vector2(0, -1):
        #     self.head_graphics = self.head_up

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
      
        # tail_relation = self.body[-2] - self.body[-1]
        # if tail_relation == Vector2(1, 0):
        #     self.tail_graphics = self.tail_left
        # elif tail_relation == Vector2(-1, 0):
        #     self.tail_graphics = self.tail_right
        # elif tail_relation == Vector2(0, 1):
        #     self.tail_graphics = self.tail_down
        # elif tail_relation == Vector2(0, -1):
        #     self.tail_graphics = self.tail_up

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
        Method class for adding a block to the snake.
        """
        self.new_block = True  # Set the flag to indicate the snake should grow

    def reset(self):
        """
        Method class for resetting the snake to its initial state.
        """
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = game.Vector2(1, 0)
        self.new_block = False
