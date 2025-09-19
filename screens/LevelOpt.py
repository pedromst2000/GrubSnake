import pygame as game
import sys
from pathlib import Path
from renderers.sounds import SOUNDS
from renderers.background import render_background
from renderers.text import render_text
from renderers.buttons import render_buttons
from gui.Button.Button import Button
from events.keyboard import handle_keydown_navigation
from events.mouse import handle_mouse_navigation
from screens.gameplay import gameplay_screen
from animations.fading import fade_in


def level_opt_screen(SCREEN: game.Surface) -> None:
    """
    Displays the level options screen where the player can choose the difficulty level.
    """

    BG = render_background(Path("assets/backgrounds/level_opt_bg.png"))

    BUTTONS = [
        Button(
            pos=(SCREEN.get_width() / 2, 250),
            text="EASY",
            base_color="#D3E2D2",
            hovering_color="White",
            default_img_path=Path("assets/menu/buttons_rect/button_default.png"),
            selected_img_path=Path("assets/menu/buttons_rect/button_selected.png"),
        ),
        Button(
            pos=(SCREEN.get_width() / 2, 350),
            text="MEDIUM",
            base_color="#D3E2D2",
            hovering_color="White",
            default_img_path=Path("assets/menu/buttons_rect/button_default.png"),
            selected_img_path=Path("assets/menu/buttons_rect/button_selected.png"),
        ),
        Button(
            pos=(SCREEN.get_width() / 2, 450),
            text="HARD",
            base_color="#D3E2D2",
            hovering_color="White",
            default_img_path=Path("assets/menu/buttons_rect/button_default.png"),
            selected_img_path=Path("assets/menu/buttons_rect/button_selected.png"),
        ),
    ]

    # Initialize selected index if it doesn't exist
    if not hasattr(level_opt_screen, "selected_idx"):
        level_opt_screen.selected_idx = 0  # Default to the first button / To manage the state of the selected button

        # TODO : REFACTOR THIS CODE TO INCLUDE THE RENDER UI ELEMENTS WITH A FUNCTION HELPER

        def render_level_options() -> None:
            """Helper function to draw the entire level options screen."""
            SCREEN.blit(BG, (0, 0))

            render_text(
                text="Choose the Level to Play",
                color="#6FC96A",
                SCREEN=SCREEN,
                type="label",
                effect="none",
            )

            render_buttons(
                buttons=BUTTONS,
                screen=SCREEN,
                menu_mouse_pos=game.mouse.get_pos(),
                selected_idx=level_opt_screen.selected_idx,
                hovering_sound=SOUNDS["menu"]["select"],
            )

        fade_in(SCREEN, render_level_options, duration=550)

    while True:
        render_level_options()

        # Event handling
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()

            # Keyboard navigation
            if event.type == game.KEYDOWN:  # key press handling from keyboard
                level_opt_screen.selected_idx = handle_keydown_navigation(
                    event=event,
                    selected_idx=level_opt_screen.selected_idx,
                    num_buttons=len(BUTTONS),
                    buttons=BUTTONS,
                    screens=[gameplay_screen],
                    SCREEN=SCREEN,
                )

            # Mouse navigation
            if event.type == game.MOUSEBUTTONDOWN:
                level_opt_screen.selected_idx = handle_mouse_navigation(
                    event=event,
                    selected_idx=level_opt_screen.selected_idx,
                    buttons=BUTTONS,
                    screens=[gameplay_screen],
                    mouse_pos=game.mouse.get_pos(),
                    SCREEN=SCREEN,
                )

        game.display.update()
