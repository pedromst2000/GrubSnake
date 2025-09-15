import pygame as game
import sys
from pathlib import Path
from renderers.background import render_background
from renderers.text import render_text
from renderers.sounds import SOUNDS
from renderers.buttons import render_buttons
from gui.Button.Button import Button
from events.keyboard import handle_keydown_navigation
from events.mouse import handle_mouse_navigation
from screens.gameplay import gameplay_screen


def level_opt_screen(SCREEN: game.Surface) -> None:
    """
    Displays the level options screen where the player can choose the difficulty level.
    """

    # TODO: TO CHANGE THE BACKGROUND IMAGE TO SOMETHING MORE CREATIVE

    BG = render_background(Path("assets/menu/background_menu.png"))

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

    SOUNDS["menu"]["music"].play(loops=-1)

    while True:
        SCREEN.blit(BG, (0, 0))
        LEVEL_OPT_MOUSE_POS = game.mouse.get_pos()

        render_text(
            text="Choose the Level to Play",
            color="#6FC96A",
            SCREEN=SCREEN,
            type="label",
            effect="none",
        )

        # Render buttons
        render_buttons(
            buttons=BUTTONS,
            screen=SCREEN,
            menu_mouse_pos=LEVEL_OPT_MOUSE_POS,
            selected_idx=level_opt_screen.selected_idx,
            hovering_sound=SOUNDS["menu"]["select"],
        )

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
                    mouse_pos=LEVEL_OPT_MOUSE_POS,
                    SCREEN=SCREEN,
                )

        game.display.update()
