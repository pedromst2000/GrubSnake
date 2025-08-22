import pygame as game
from utils.settings import CELL_NUMBER_X, CELL_NUMBER_Y
from classes.Snake.Snake import Snake
from classes.Byte.Byte import Byte


class Main:
    def __init__(
        self,
        eat_sound: game.mixer.Sound,
        game_over_sound: game.mixer.Sound,
        move_sound: game.mixer.Sound,
        score: int,
    ):
        """
        Initialize the main game class.
        """
        self.snake = Snake()
        self.byte = Byte(self.snake.body)
        self.eat_sound = eat_sound
        self.game_over_sound = game_over_sound
        self.move_sound = move_sound
        self.score = score

    def update_game(self):
        """
        Update the snake's position and state.
        """
        self.snake.move()
        self.check_collision_byte(self.eat_sound)
        self.check_fail()

    def draw_elements(self, screen: game.Surface):
        """
        Draw the snake and byte on the given screen.
        """
        self.byte.draw_byte(screen)
        self.snake.draw_snake(screen)

    def check_collision_byte(self, eat_sound: game.mixer.Sound):
        """
        Check for collisions with the byte.
        """

        if self.snake.body[0] == self.byte.pos:
            eat_sound.play()
            self.snake.add_block()
            self.byte.randomize_position(self.snake.body)
            self.score += 1
            print(f"Score: {self.score}")

    def check_fail(self):
        """
        Check for collisions with the walls or self.
        """

        head = self.snake.body[0]

        # Border collision (allowing last cell as valid)
        if (
            head.x < 0
            or head.x >= CELL_NUMBER_X
            or head.y < 0
            or head.y >= CELL_NUMBER_Y
        ):
            self.game_over()
            return

        # Self collision
        if head in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        """
        Handle game over state.
        """
        self.game_over_sound.play()
        self.snake.reset()
        self.byte.randomize_position(
            self.snake.body
        )  # Ensure byte is visible and not overlapping after reset
        self.score = 0
        print("Game Over! Your score was:", self.score)
