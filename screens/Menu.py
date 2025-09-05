import pygame as game, sys
from pathlib import Path
from renderers.background import render_background
from renderers.text import render_text
from renderers.sounds import SOUNDS
from gui.Button.Button import Button


def main_menu_screen(SCREEN: game.Surface) -> None:
    """
    Displays the screen of the main menu of the game.

    Args:
    - SCREEN (game.Surface): The surface to render the text on.

    Returns:
    - None
    """

    BG = render_background(Path("assets/menu/background_menu.png"))

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = game.mouse.get_pos()

        render_text(
            text="BITSNAKE",
            color="#285f25",
            SCREEN=SCREEN,
            type="title",
            effect="shadow",
            offset=(7, 6.7),
        )

        render_text(
            text="BITSNAKE",
            color="#6FC96A",
            SCREEN=SCREEN,
            type="title",
            effect="none",
        )

        SOUNDS["menu"]["music"].play(
            -1
        )  # Play menu music / -1 = loop indefinitely the music

        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()

        game.display.update()
