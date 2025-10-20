import pygame as game
import sys
from pathlib import Path
from classes.Main import Main
from settings.settings import LEVELS, MOVE_EVENT
from renderers.sounds import (
    MENU_MUSIC_SOUND,
    EAT_APPLE_SOUND,
    EAT_POISON_SOUND,
    GAME_OVER_SOUND,
)
from renderers.background import render_background
from events.keyboard import handle_keydown_snake_movement
from animations.fading import fade_in


def gameplay_screen(SCREEN: game.Surface, chosen_level: str):
    """
    Renders the gameplay screen for the selected difficulty level.

    :param SCREEN: The main game surface where elements are drawn.
    :param chosen_level: The difficulty level chosen by the player.
    """
    BG: game.Surface = render_background(Path("assets/backgrounds/game_bg.png"))
    MENU_MUSIC_SOUND.stop()

    main_game: Main = Main(
        eat_sound=EAT_APPLE_SOUND,
        poison_sound=EAT_POISON_SOUND,
        game_over_sound=GAME_OVER_SOUND,
        selected_level=chosen_level,
    )

    def render_fade_in():
        SCREEN.blit(BG, (0, 0))
        main_game.draw_elements(SCREEN)

    clock: game.time.Clock = game.time.Clock()  # Control the frame rate

    fade_in(SCREEN, render_fade_in, duration=1550)

    game.time.set_timer(MOVE_EVENT, LEVELS[chosen_level]["move_interval"])

    while True:
        SCREEN.blit(BG, (0, 0))  # Clear screen each frame

        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()
            if event.type == game.KEYDOWN:
                handle_keydown_snake_movement(event, main_game=main_game)
            elif event.type == MOVE_EVENT:  #  Snake movement event
                main_game.update_game()

        main_game.draw_elements(SCREEN)
        game.display.update()
        clock.tick(60)
