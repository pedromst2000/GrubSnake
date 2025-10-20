import pygame as game


def render_font(size: int) -> game.font.Font:
    """
    Render a font object from a file path and size.

    :param size: Size of the font.

    Returns:
        game.font.Font: The rendered font object.
    """

    return game.font.Font("assets/font/PressStart2P_font.ttf", size)
