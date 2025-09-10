import pygame as game
from gui.Button.Button import Button


def render_buttons(
    buttons: list[Button],
    screen: game.Surface,
    menu_mouse_pos: tuple[int, int],
    selected_idx: int,
    hovering_sound: game.mixer.Sound = None,
) -> None:
    """
    Renders a list of buttons on the screen with hover + keyboard selection.

    Args:
        buttons (list[Button]): List of Button objects to render.
        screen (game.Surface): The surface to draw the buttons on.
        menu_mouse_pos (tuple[int, int]): Current mouse position.
        selected_idx (int): Index of the currently selected button (keyboard).
        hovering_sound (game.mixer.Sound, optional): Sound to play on hover. Defaults to None.
    Returns:
        None
    """
    for idx, button in enumerate(buttons):  # enumerate to get index
        # selected=True if this button is selected via keyboard
        button.change_state(menu_mouse_pos, selected=(idx == selected_idx))
        button.update(screen)
        button.change_cursor(button.rect.collidepoint(menu_mouse_pos), hovering_sound=hovering_sound)
