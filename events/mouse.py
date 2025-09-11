import pygame as game
import sys
from renderers.sounds import SOUNDS
from gui.Button.Button import Button


def handle_mouse_navigation(
    event: game.event.Event,
    selected_idx: int,
    buttons: list[Button],
    screens: list[callable],
    mouse_pos: tuple[int, int] = None,
) -> None:
    """
    Handles mouse click events for menu navigation.

    Args:
        event (game.event.Event): The mouse button down event.
        selected_idx (int): The currently selected button index.
        buttons (list[Button]): The list of Button objects.
        screens (list[callable]): A list of screen functions corresponding to the buttons.
        mouse_pos (tuple[int, int], optional): The current mouse position. Defaults to None.

    Returns:
        None
    """
    SOUNDS["menu"]["click"].play()  # Click sound
    for idx, button in enumerate(buttons):
        if button.check_for_input(position=mouse_pos, selected=False):
            selected_idx = idx
            if button.text_str == "PLAY":
                screens[0]()  # Calling the function directly from the list of screens
            elif button.text_str == "INSTRUCTIONS":
                screens[1]()
            elif button.text_str == "EXIT":
                SOUNDS["menu"]["music"].stop()
                game.quit()
                sys.exit()
