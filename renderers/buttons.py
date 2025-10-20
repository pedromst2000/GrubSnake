import pygame as game
from gui.Button.Button import Button


def render_buttons(
    buttons: list[Button],
    screen: game.Surface,
    menu_mouse_pos: tuple[int, int],
    selected_idx: int,
    hovering_sound: game.mixer.Sound = None,
):
    """
    Renders a list of buttons on the screen with hover + keyboard selection.

    :param buttons: List of Button objects to render.
    :param screen: The surface to draw the buttons on.
    :param menu_mouse_pos: Current mouse position.
    :param selected_idx: Index of the currently selected button (keyboard).
    :param hovering_sound: Sound to play on hover. Defaults to None.
    """
    for idx, button in enumerate(buttons):  # enumerate to get index
        # selected=True if this button is selected via keyboard
        button.change_state(menu_mouse_pos, selected=(idx == selected_idx))
        button.update(screen)
        button.change_cursor(
            button.rect.collidepoint(menu_mouse_pos), hovering_sound=hovering_sound
        )
