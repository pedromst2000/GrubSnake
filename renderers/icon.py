import pygame as game
from pathlib import Path


def render_icon(icon_path: str, Image: game.Surface):
    """
    To render the icon in the window.

    :param icon_path: The path to the icon file.
    :param Image: The image surface to render.

    """
    ico_path: Path = Path(icon_path)
    pill_image: game.Surface = Image.open(Path(ico_path)).convert(
        "RGBA"
    )  # convert to alpha channel
    icon: game.Surface = game.image.fromstring(
        pill_image.tobytes(), pill_image.size, "RGBA"
    )
    game.display.set_icon(icon)
