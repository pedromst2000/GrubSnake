import pygame as game
from pathlib import Path

def render_icon(icon_path: str, Image: game.Surface) -> None:
   """
   To render the icon in the window.

   Parameters:
       Path (game.Path): The path to the icon file.
       Image (game.Surface): The image surface to render.
   
   Returns:
       None
   """
   ico_path = Path(icon_path)
   pill_image = Image.open(Path(ico_path)).convert("RGBA")  # convert to alpha channel
   icon = game.image.fromstring(pill_image.tobytes(), pill_image.size, "RGBA")
   game.display.set_icon(icon)
