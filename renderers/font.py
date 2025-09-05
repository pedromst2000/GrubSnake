import pygame as game


def render_font(size: int) -> game.font.Font:
    """
    Render a font object from a file path and size.

    Parameters:
    - size (int): The size of the font. Default is 24.

    Returns:
    - game.font.Font: The rendered font object.
    """

    return game.font.Font("assets/font/PressStart2P_font.ttf", size)
