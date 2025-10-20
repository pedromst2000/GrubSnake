import pygame as game
from pygame import Vector2
from settings.settings import CELL_NUMBER_X, CELL_NUMBER_Y, CELL_SIZE
from classes.Snake.Snake import Snake
from classes.Item.Item import Item
from classes.Obstacle.Obstacle import Obstacle
from gui.Hud.Hud import HUD_Score as Score


class Main:
    """
    Main game class to manage game state, updates, and rendering of elements.
    """

    def __init__(
        self,
        eat_sound: game.mixer.Sound,
        poison_sound: game.mixer.Sound,
        game_over_sound: game.mixer.Sound,
        selected_level: str,
    ):
        """
        Initialize the main game with sounds and selected level settings.
        
        :param eat_sound: Sound to play when the snake eats an apple.
        :param poison_sound: Sound to play when the snake eats poison.
        :param game_over_sound: Sound to play on game over.
        :param selected_level: The selected difficulty level ('easy', 'medium', 'hard').
        """

        self.snake: Snake = Snake()
        self.level: str = selected_level
        self.apple: Item = Item(self.snake.body, "assets/graphics/items/apple.png")
        self.obstacles: list[Obstacle] = [] if self.level == "hard" else None

        # Only medium or hard levels have poison
        self.poison_image: game.Surface | None = None
        self.poisons: list[Item] = []
        if self.level != "easy":
            raw_image: game.Surface = game.image.load(
                "assets/graphics/items/poison.png"
            ).convert_alpha()
            self.poison_image: game.Surface = game.transform.scale(
                raw_image, (CELL_SIZE, CELL_SIZE)
            )

            # Spawn random poisons initially
            self.poisons: list[Item] = Item.spawn_poisons(
                self.snake.body, self.apple.pos, self.level
            )

        self.eat_sound: game.mixer.Sound = eat_sound
        self.poison_sound: game.mixer.Sound = poison_sound
        self.game_over_sound: game.mixer.Sound = game_over_sound
        self.score_HUD: Score = Score(self.level)
        self.obstacle_spawn_interval: int = 50  # ~1.5s at 60fps
        self._obstacle_spawn_timer: int = 0  # internal timer for obstacle spawning

        # Movement speed (grid cells per MOVE_EVENT) for obstacles
        self.obstacle_speed: float = 0.50
        self.obstacle_width: int = 2
        self.obstacle_height: int = 2
        self.obstacle_gap: int = 6  # min gap between obstacles in a row

    def update_game(self):
        """
        Update the game state: move the snake, check for collisions and game over.
        """
        self.snake.move_growth()
        self.check_collision_item()
        self.check_fail()

        if self.level == "hard" and self.obstacles is not None:
            self.update_obstacles()

    def update_obstacles(self):
        """
        Spawn and move obstacles for hard level.
        """

        # Move existing obstacles down
        for obstacle in self.obstacles[:]:
            obstacle.move(speed=self.obstacle_speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)

        # Timer-based spawn: spawn rows periodically, only if top area is free
        self._obstacle_spawn_timer += 1
        if self._obstacle_spawn_timer < self.obstacle_spawn_interval:
            return

        # Reset timer
        self._obstacle_spawn_timer: int = 0

        top_occupied: bool = any(
            int(ob.y) < (self.obstacle_height + 1) for ob in self.obstacles
        )
        if top_occupied:
            return  # Don't spawn new obstacles if top is occupied

        # Spawn a new deterministic row with uniform spacing
        Obstacle.spawn_obstacle_row(
            self=self,
            obstacle_width=self.obstacle_width,
            obstacle_height=self.obstacle_height,
            gap=self.obstacle_gap,
        )

    def draw_elements(self, screen: game.Surface):
        """
        Draw all game elements on the screen.

        :param screen: The game screen surface to draw on.
        """
        self.apple.draw(screen)

        # Draw all poisons
        if self.poison_image:
            for pos in self.poisons:
                screen.blit(self.poison_image, (pos.x * CELL_SIZE, pos.y * CELL_SIZE))

        self.snake.draw_snake(screen)
        self.score_HUD.draw_score(screen, (20, 20))

        if self.obstacles:  # draw obstacles if any
            for obstacle in self.obstacles:
                obstacle.draw(screen)

    def check_collision_item(self):
        """
        Check for collisions between the snake and items (apple and poison).
        """
        head: Vector2 = self.snake.body[0]

        # Apple collision
        if head == self.apple.pos:
            self.eat_sound.play()
            self.snake.add_block()
            self.score_HUD.add_score(1)

            self.apple.randomize_position(
                self.snake.body, forbidden_positions=self.poisons
            )

            if self.poison_image:
                self.poisons: list[Vector2] = Item.spawn_poisons(
                    self.snake.body, self.apple.pos, self.level
                )
            return

        # Poison collision
        if self.poison_image and head in self.poisons:
            self.poison_sound.play()
            self.score_HUD.add_score(-1)
            self.poisons.remove(head)

    def check_fail(self):
        """
        Check for game over conditions: border collision, self-collision, obstacle collision.
        """
        head: Vector2 = self.snake.body[0]

        # Border collision
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

        # Obstacle collision
        if self.level == "hard" and self.obstacles is not None:
            for obstacle in self.obstacles:
                obstacle_cells: set[tuple[int, int]] = {
                    (int(c.x), int(c.y)) for c in obstacle.get_cells()
                }
                for segment in self.snake.body:
                    seg: tuple[int, int] = (int(segment.x), int(segment.y))
                    if seg in obstacle_cells:
                        self.game_over()
                        return

    def game_over(self):
        """
        Handle game over: play sound, reset snake, score, obstacles, and respawn items.
        """
        self.game_over_sound.play()
        self.snake.reset()
        self.score_HUD.reset()
        self.obstacles: list[Obstacle] = (
            [] if self.level == "hard" else None
        )  # reset obstacles

        self.apple.randomize_position(self.snake.body)  # respawn apple
        if self.poison_image:  # respawn poisons
            self.poisons: list[Item] = Item.spawn_poisons(
                self.snake.body, self.apple.pos, self.level
            )
