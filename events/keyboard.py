import pygame as game
import sys
from renderers.sounds import SOUNDS
from gui.Button.Button import Button


def handle_keydown_navigation(
    event: game.event.Event,
    selected_idx: int,
    num_buttons: int,
    buttons: list[Button],
    screens: list[callable] = None,
    SCREEN: game.Surface = None,
    selected_nvl: str = None,
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
        selected_nvl (str | None): The selected level (e.g., "easy", "medium", "hard").

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

            if screens and SCREEN is not None:
                if selected_btn.text_str == "PLAY":
                    screens[0](
                        SCREEN
                    )  # Calling the function directly from the list of screens
                if selected_btn.text_str == "INSTRUCTIONS":
                    screens[1](SCREEN)

                elif selected_nvl is not None:
                    if selected_btn.text_str in ["EASY", "MEDIUM", "HARD"]:
                        # screens[0](SCREEN, selected_btn.text_str.lower())
                        print(f"Selected level: {selected_nvl}")  # For testing purposes
                if selected_btn.text_str == "EXIT":
                    SOUNDS["menu"]["music"].stop()
                    game.quit()
                    sys.exit()

    return selected_idx
