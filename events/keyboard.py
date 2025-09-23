import pygame as game
import sys
from renderers.sounds import CLICK_BTN_SOUND, SELECT_BTN_SOUND
from gui.Button.Button import Button


def handle_keydown_navigation(
    event: game.event.Event,
    selected_idx: int,
    num_buttons: int,
    buttons: list[Button],
    screens: list[callable] = None,
    SCREEN: game.Surface = None,
) -> int:
    """
    Handles keydown events for menu navigation (up/down arrows and enter/space key).

    Args:
        event (game.event.Event): The keydown event.
        selected_idx (int): The currently selected button index.
        num_buttons (int): The total number of buttons.
        buttons (list[Button]): The list of Button objects.
        screens (list[callable] | None): A list of screen functions corresponding to the buttons.
        SCREEN (game.Surface | None): The main display surface where the screens will be rendered.

    Returns:
        int: The updated selected button index.
    """

    if event.key == game.K_DOWN:
        selected_idx = (
            selected_idx + 1
        ) % num_buttons  # Wrap around and increment index
        SELECT_BTN_SOUND.play()  # Selection sound
    elif event.key == game.K_UP:
        selected_idx = (
            selected_idx - 1
        ) % num_buttons  # Wrap around and decrement index
        SELECT_BTN_SOUND.play()  # Selection sound
    elif event.key in (
        game.K_RETURN,
        game.K_KP_ENTER,
        game.K_SPACE,
    ):  # Enter or Space key
        selected_btn = buttons[selected_idx]  # Get the currently selected button
        if selected_btn.check_for_input(selected=True):  # Confirm selection
            CLICK_BTN_SOUND.play()  # Click sound
            selected_nvl = selected_btn.text_str.lower()  # Update selected level

            if screens and SCREEN is not None:
                if selected_btn.text_str == "PLAY":
                    screens[0](
                        SCREEN
                    )  # Calling the function directly from the list of screens
                if selected_btn.text_str == "INSTRUCTIONS":
                    screens[1](SCREEN)

                elif selected_nvl is not None:
                    if selected_btn.text_str in ["EASY", "MEDIUM", "HARD"]:
                        screens[0](SCREEN, selected_nvl)

                if selected_btn.text_str == "EXIT":
                    game.quit()
                    sys.exit()

    return selected_idx
