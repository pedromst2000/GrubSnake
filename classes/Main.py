import pygame as game
from settings.settings import CELL_NUMBER_X, CELL_NUMBER_Y, CELL_SIZE
from classes.Snake.Snake import Snake
from classes.Item.Item import Item
from gui.Hud.Hud import HUD_Score as Score
from pygame import Vector2


class Main:
    def __init__(
        self,
        eat_sound: game.mixer.Sound,
        poison_sound: game.mixer.Sound,
        game_over_sound: game.mixer.Sound,
        selected_level: str,
    ):
        """
        Initialize the main game class.
        """
        self.snake = Snake()
        self.level = selected_level
        self.apple = Item(self.snake.body, "assets/graphics/items/apple.png")

        # Only medium or hard levels have poison
        self.poison_image = None
        self.poisons: list[Vector2] = []
        if self.level != "easy":
            raw_image = game.image.load(
                "assets/graphics/items/poison.png"
            ).convert_alpha()
            self.poison_image = game.transform.smoothscale(
                raw_image, (CELL_SIZE, CELL_SIZE)
            )
            # Spawn 1 poison initially
            self.poisons = Item.spawn_poisons(self.snake.body, self.apple.pos, [])

        self.eat_sound = eat_sound
        self.poison_sound = poison_sound
        self.game_over_sound = game_over_sound
        self.score_HUD = Score(self.level)

    def update_game(self):
        """
        Update the game state: move the snake, check for collisions and game over.
        """

        self.snake.move()
        self.check_collision_item()
        self.check_fail()

    def draw_elements(self, screen: game.Surface):
        """
        Draw all game elements on the screen.
        """

        self.apple.draw(screen)
        # Draw all poisons
        if self.poison_image:
            for pos in self.poisons:
                screen.blit(self.poison_image, (pos.x * CELL_SIZE, pos.y * CELL_SIZE))
        self.snake.draw_snake(screen)
        self.score_HUD.draw_score(screen, (20, 20))

    def check_collision_item(self):
        """
        Check for collisions between the snake and items (apple and poison).
        """
        head = self.snake.body[0]

        # Apple collision
        if head == self.apple.pos:
            self.eat_sound.play()
            self.snake.add_block()
            self.score_HUD.add_score(1)
            # Move apple to a new valid position
            self.apple.randomize_position(
                self.snake.body, forbidden_positions=self.poisons
            )

            # Spawn new poisons
            if self.poison_image:
                new_poisons = Item.spawn_poisons(
                    self.snake.body, self.apple.pos, self.poisons
                )
                self.poisons.extend(new_poisons)
                # Cap maximum poisons to 9
                if len(self.poisons) > 9:
                    self.poisons = self.poisons[-9:]  # keep only the last 9 poisons

        # Poison collision
        elif self.poison_image and head in self.poisons:
            self.poison_sound.play()
            self.score_HUD.add_score(-1)
            # Remove poison that was eaten
            self.poisons.remove(head)

    def check_fail(self):
        """
        Check for game over conditions: border collision and self-collision.
        """
        head = self.snake.body[0]

        if (  # Border collision
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
        Handle game over state: play sound, reset snake and score, reposition items.
        """
        self.game_over_sound.play()
        self.snake.reset()
        self.score_HUD.reset()
        # Reset apple and poisons
        self.apple.randomize_position(self.snake.body)
        if self.poison_image:
            self.poisons = Item.spawn_poisons(self.snake.body, self.apple.pos, [])
