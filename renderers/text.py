import pygame as game
from renderers.font import render_font


def render_text(
    text: str,
    color: str,
    SCREEN: game.Surface = None,
    type: str = "title",
    effect: str = "none",
    offset: tuple = (0, 0),
    return_surface: bool = False,
) -> game.Surface | None:
    """
    Renders a label text on the screen or returns the surface if requested.


    :param text: The text to render.
    :param color: The color of the text.
    :param SCREEN: The surface to render the text on (ignored if return_surface=True).
    :param type: "title", "input", "label".
    :param effect: "none" or "shadow".
    :param offset: Shadow offset for "title".
    :param return_surface: If True, return a text Surface instead of blitting (default False).
    Returns:
        game.Surface: The rendered text surface if return_surface is True, else None.
    """

    font_size: int = 60 if type == "title" else 20 if type == "input" else 13
    FONT: game.Font = render_font(size=font_size)

    # Always render a surface
    text_surface: game.Surface = FONT.render(text, True, color)

    if return_surface:
        return text_surface

    if SCREEN is None:
        raise ValueError("SCREEN must be provided if return_surface=False")

    if type == "title":
        if effect == "shadow":
            shadow_surface: game.Surface = FONT.render(text, True, color)
            shadow_rect: game.Rect = shadow_surface.get_rect(
                center=(
                    SCREEN.get_width() // 2 + offset[0],
                    75 + offset[1],
                )
            )
            SCREEN.blit(shadow_surface, shadow_rect)

        text_rect: game.Rect = text_surface.get_rect(
            center=(SCREEN.get_width() // 2, 75)
        )
        SCREEN.blit(text_surface, text_rect)
    else:
        # For inputs/labels just blit centered near top
        text_rect: game.Rect = text_surface.get_rect(
            center=(SCREEN.get_width() // 2, 75)
        )
        SCREEN.blit(text_surface, text_rect)
