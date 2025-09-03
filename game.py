from PIL import Image
import pygame as game, sys
from pathlib import Path
from settings.settings import (
    CELL_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MOVE_EVENT,
)
from settings.settings import LEVELS
from settings.icon import render_icon
from classes.Main import Main


def main():

    game.init()
    screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game.display.set_caption("BitSnake")

    background_grass = game.image.load(Path("assets/background_game.png")).convert()
    background_grass = game.transform.scale(
        background_grass, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )  # to adjust the window size

    render_icon(icon_path="assets/Icon.ico", Image=Image)

    # Load assets
    eat_sound = game.mixer.Sound(Path("assets/sounds/eating_byte.wav"))
    poison_sound = game.mixer.Sound(Path("assets/sounds/eating_poison.wav"))
    game_over_sound = game.mixer.Sound(Path("assets/sounds/game_over.wav"))
    move_sound = game.mixer.Sound(Path("assets/sounds/snake_rustling.wav"))

    poison_sound.set_volume(0.6)
    game_over_sound.set_volume(0.6)
    move_sound.set_volume(0.50)

    # HUD SCORE - TO BE REFACTORED WITH A CALLBACK FUNCTION
    font = game.font.SysFont("Consolas", 18, bold=True)
    byte_icon_small = game.image.load(
        Path("assets/graphics/items/byte.png")
    ).convert_alpha()
    # Scaling to Fit
    if byte_icon_small.get_width() != CELL_SIZE:
        byte_icon_small = game.transform.smoothscale(byte_icon_small, (18, 18))

    # Game loop
    main_game = Main(
        eat_sound, poison_sound, game_over_sound, font, byte_icon_small
    )  # Initialize the main game class
    game.time.set_timer(
        MOVE_EVENT, LEVELS[main_game.level]["move_interval"]
    )  # Set the timer for snake movement
    clock = game.time.Clock()  # Create a clock object to manage the frame rate

    # TODO - INSERT THE MAIN MENU LOGIC HERE
    running = True
    while running:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()
            if event.type == game.KEYDOWN:
                if (
                    event.key in (game.K_UP, game.K_w)
                    and main_game.snake.direction.y != 1
                ):
                    main_game.snake.direction = game.Vector2(0, -1)
                    move_sound.play()
                if (
                    event.key in (game.K_DOWN, game.K_s)
                    and main_game.snake.direction.y != -1
                ):
                    main_game.snake.direction = game.Vector2(0, 1)
                move_sound.play()
                if (
                    event.key in (game.K_LEFT, game.K_a)
                    and main_game.snake.direction.x != -1
                ):
                    main_game.snake.direction = game.Vector2(-1, 0)
                    move_sound.play()
                if (
                    event.key in (game.K_RIGHT, game.K_d)
                    and main_game.snake.direction.x != 1
                ):
                    main_game.snake.direction = game.Vector2(1, 0)
                    move_sound.play()

        screen.blit(background_grass, (0, 0))
        main_game.update_game()
        main_game.draw_elements(screen)

        game.display.flip()  # Update the display
        clock.tick(LEVELS[main_game.level]["fps"])

    game.quit()  # Quit the game
    sys.exit()  # Exit the program


if __name__ == "__main__":
    main()
