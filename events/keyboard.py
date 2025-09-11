import pygame as game
import sys
from renderers.sounds import SOUNDS
from gui.Button.Button import Button


def handle_keydown_navigation(
    event: game.event.Event,
    selected_idx: int,
    num_buttons: int,
    buttons: list[Button],
    screens: list[callable],
) -> int:
    """
    Handles keydown events for menu navigation (up/down arrows and enter/space key).

    Args:
        event (game.event.Event): The keydown event.
        selected_idx (int): The currently selected button index.
        num_buttons (int): The total number of buttons.
        buttons (list[Button]): The list of Button objects.
        screens (list[callable]): A list of screen functions corresponding to the buttons.

    Returns:
        int: The updated selected button index.
    """
    if event.key == game.K_DOWN:
        selected_idx = (
            selected_idx + 1
        ) % num_buttons  # Wrap around and increment index
        SOUNDS["menu"]["select"].play()  # Selection sound
    elif event.key == game.K_UP:
        selected_idx = (
            selected_idx - 1
        ) % num_buttons  # Wrap around and decrement index
        SOUNDS["menu"]["select"].play()  # Selection sound
    elif event.key in (
        game.K_RETURN,
        game.K_KP_ENTER,
        game.K_SPACE,
    ):  # Enter or Space key
        selected_btn = buttons[selected_idx]  # Get the currently selected button
        if selected_btn.check_for_input(selected=True):  # Confirm selection
            SOUNDS["menu"]["click"].play()  # Click sound
            if selected_btn.text_str == "PLAY":
                screens[0]()  # Calling the function directly from the list of screens
            elif selected_btn.text_str == "INSTRUCTIONS":
                screens[1]()
            elif selected_btn.text_str == "EXIT":
                SOUNDS["menu"]["music"].stop()
                game.quit()
                sys.exit()
    return selected_idx
