import pygame as game
from settings.settings import CELL_NUMBER_X, CELL_NUMBER_Y
from classes.Snake.Snake import Snake
from classes.Item.Item import Item
from classes.Score.Score import Score


class Main:
    def __init__(
        self,
        eat_sound: game.mixer.Sound,
        poison_sound: game.mixer.Sound,
        game_over_sound: game.mixer.Sound,
        font: game.font.Font,
        apple_icon_small: game.Surface,
    ):
        """
        Initialize the main game class.
        """
        self.snake = Snake()
        self.level = "hard"  # hardcoded
        self.apple = Item(self.snake.body, "assets/graphics/items/apple.png")
        self.poison = (
            Item(self.snake.body, "assets/graphics/items/poison.png")
            if self.level == "hard"
            else None
        )
        self.eat_sound = eat_sound
        self.poison_sound = poison_sound
        self.game_over_sound = game_over_sound
        self.font = font
        self.score_HUD = Score(font, apple_icon_small, self.level)

    def update_game(self):
        """
        Update the snake's position and state.
        """
        self.snake.move()
        self.check_collision_item(self.eat_sound, self.poison_sound)
        self.check_fail()

    def draw_elements(self, screen: game.Surface):
        """
        Draw the snake and apple on the given screen.
        """
        self.apple.draw(screen)
        if (
            self.poison
        ):  # will draw the poison item if it exists (only available in hard mode)
            self.poison.draw(screen)
        self.snake.draw_snake(screen)
        self.score_HUD.draw_score(screen, (20, 20))

    def check_collision_item(
        self, eat_sound: game.mixer.Sound, poison_sound: game.mixer.Sound
    ):
        """
        Check for collisions with the apple.
        """

        if self.snake.body[0] == self.apple.pos:
            eat_sound.play()
            self.snake.add_block()
            self.score_HUD.add_score(1)
            self.apple.randomize_position(self.snake.body)
            if self.poison:
                self.poison.randomize_position(self.snake.body)
        elif self.poison and self.snake.body[0] == self.poison.pos:
            poison_sound.play()
            self.score_HUD.add_score(-1)
            self.apple.randomize_position(self.snake.body)
            self.poison.randomize_position(self.snake.body)

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

        # # Collide with poison
        # elif self.poison and head == self.poison.pos:
        #     self.game_over()

    def game_over(self):
        """
        Handle game over state.
        """
        self.game_over_sound.play()
        # self.score_HUD.save_high_score()
        self.snake.reset()
        self.score_HUD.reset()
        self.apple.randomize_position(
            self.snake.body
        )  # Ensure apple is visible and not overlapping after reset
