from PIL import Image
import pygame as game
from settings.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from renderers.icon import render_icon
from screens.Menu import main_menu_screen

game.init()
SCREEN = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game.display.set_caption("GRUBSNAKE")
render_icon(icon_path="assets/Icon.ico", Image=Image)


main_menu_screen(SCREEN)
