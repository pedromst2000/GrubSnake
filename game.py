from PIL import Image
import pygame as game, sys
from pathlib import Path
from utils.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from classes.Main import Main


def main():

    game.init()
    screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game.display.set_caption("BitSnake")
    clock = game.time.Clock()  # Create a clock object to manage the frame rate

    background_grass = game.image.load(Path("assets/background.png")).convert()
    background_grass = game.transform.scale(
        background_grass, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )  # to adjust the window size

    # Icon Setting
    ico_path = Path("assets/Icon.ico")
    pill_image = Image.open(Path(ico_path)).convert("RGBA")  # convert to alpha channel
    icon = game.image.fromstring(pill_image.tobytes(), pill_image.size, "RGBA")
    game.display.set_icon(icon)

    # Load assets
    eat_sound = game.mixer.Sound(Path("assets/sounds/eating_byte.wav"))
    game_over_sound = game.mixer.Sound(Path("assets/sounds/game_over.wav"))
    move_sound = game.mixer.Sound(Path("assets/sounds/snake_rustling.wav"))

    # Game loop
    main_game = Main()  # Initialize the main game class
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
                    and main_game.snake.direction.x != 1
                ):
                    main_game.snake.direction = game.Vector2(-1, 0)
                    move_sound.play()
                if (
                    event.key in (game.K_RIGHT, game.K_d)
                    and main_game.snake.direction.x != -1
                ):
                    main_game.snake.direction = game.Vector2(1, 0)
                    move_sound.play()

        screen.blit(
            background_grass, (0, 0)
        )  # Fill the screen with the background image
        game.display.flip()  # Flip the display buffers - buffers are now displayed on the screen

        main_game.update_snake()
        main_game.draw_snake(screen)
        game.display.update()
        clock.tick(FPS)

    game.quit()  # Quit the game
    sys.exit()  # Exit the program


if __name__ == "__main__":
    main()
