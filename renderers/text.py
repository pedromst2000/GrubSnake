import pygame as game
from renderers.font import render_font


def render_text(
    text: str,
    color: str,
    SCREEN: game.Surface,
    type: str = "title",
    effect: str = "none",
    offset: tuple = (0, 0),
) -> None:
    """
    Renders a label text on the screen for title or other types with optional effects.

    Args:
        size (int): The size of the font.
        text (str): The text to render.
        color (str): The color of the text.
        SCREEN (game.Surface): The surface to render the text on.
        type (str): The type of label to render. Default is "title". options: "title", "input", "label".
        effect (str): The effect to apply to the label. Default is "none". options: "none", "shadow".
        offset (tuple): The (x, y) offset to apply to the label position. Default is (0, 0).

    Returns:
        None
    """

    FONT = render_font(size=60 if type == "title" else 24)

    if type == "title":
        if effect == "shadow":
            SHADOW_OFFSET = (offset[0], offset[1])
            SHADOW_TEXT = FONT.render(text, True, color)
            SHADOW_RECT = SHADOW_TEXT.get_rect(
                center=(
                    SCREEN.get_width() // 2 + SHADOW_OFFSET[0],
                    75 + SHADOW_OFFSET[1],
                )
            )
            SCREEN.blit(SHADOW_TEXT, SHADOW_RECT)
        # ELSE
        MENU_TEXT = FONT.render(text, True, color)
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN.get_width() // 2, 75))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
