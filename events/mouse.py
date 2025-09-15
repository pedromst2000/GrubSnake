import pygame as game
import sys
from renderers.sounds import SOUNDS
from gui.Button.Button import Button


def handle_mouse_navigation(
    event: game.event.Event,
    selected_idx: int,
    buttons: list[Button],
    screens: list[callable] | None = None,
    mouse_pos: tuple[int, int] = None,
    SCREEN: game.Surface = None,
) -> int:
    """
    Handles mouse click events for menu navigation.

    Args:
        event (game.event.Event): The mouse button down event.
        selected_idx (int): The currently selected button index.
        buttons (list[Button]): The list of Button objects.
        screens (list[callable] | None, optional): A list of screen functions corresponding to the buttons. Defaults to None.
        mouse_pos (tuple[int, int], optional): The current mouse position. Defaults to None.
        SCREEN (game.Surface, optional): The main display surface where the screens will be rendered. Defaults to None.
    Returns:
        int: The updated selected button index.
    """
    SOUNDS["menu"]["click"].play()  # Click sound
    for idx, button in enumerate(
        buttons
    ):  # Iterate through buttons to check each button it´s being clicked or selected
        if button.check_for_input(position=mouse_pos):
            selected_idx = idx
            selected_nvl = button.text_str.lower()  # Update selected level

            if screens and SCREEN is not None:  # Only proceed if screens are provided
                if button.text_str == "PLAY":
                    screens[0](SCREEN)  # Calling the function directly from the list of screens
                elif button.text_str == "INSTRUCTIONS":
                    screens[1](SCREEN)
                elif button.text_str in ["EASY", "MEDIUM", "HARD"]:
                    # screens[0](SCREEN, selected_nvl)  # Call the screen function with selected level
                    print(f"Selected level: {selected_nvl}")  # For testing purposes
                elif button.text_str == "EXIT":
                    SOUNDS["menu"]["music"].stop()
                    game.quit()
                    sys.exit()

    return selected_idx
