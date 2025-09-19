import pygame as game
from pathlib import Path


def render_background(path: str) -> game.Surface:
    """
    Renders the background for the screen, covering it fully while preserving aspect ratio.
    (Similar to CSS background-size: cover)

    Args:
        path (str): The file path to the background image.

    Returns:
        game.Surface: The scaled and cropped background image surface.
    """
    window_size = game.display.get_surface().get_size()
    screen_width, screen_height = window_size

    # Load original background
    background = game.image.load(Path(path)).convert()
    bg_width, bg_height = background.get_size()

    # Calculate scale factor (use max to cover screen fully)
    scale_factor = max(screen_width / bg_width, screen_height / bg_height)

    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)

    # Scale background
    background = game.transform.scale(background, (new_width, new_height))

    # Crop/center to fit screen
    x_offset = (new_width - screen_width) // 2
    y_offset = (new_height - screen_height) // 2
    final_surface = background.subsurface(
        (x_offset, y_offset, screen_width, screen_height)
    )

    return final_surface
