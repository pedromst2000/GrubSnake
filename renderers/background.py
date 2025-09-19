import pygame as game
from pathlib import Path
from settings.settings import SCREEN_WIDTH, SCREEN_HEIGHT


def render_background(path: str) -> game.Surface:
    """
    Renders the background for the main menu.
    Renders the background for the screen.

    Args:
        path (str): The file path to the background image.

    Returns:
        game.Surface: The scaled background image surface.

    """
    background = game.image.load(Path(path)).convert()
    background = game.transform.scale(
        background, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )  # to adjust the window size

    return background
