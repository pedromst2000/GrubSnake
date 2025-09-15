import pygame as game
import sys
from pathlib import Path
from renderers.background import render_background
from renderers.text import render_text
from renderers.sounds import SOUNDS
from renderers.buttons import render_buttons
from gui.Button.Button import Button
from screens.Instructions import instructions_screen
from screens.LevelOpt import level_options_screen
from events.keyboard import handle_keydown_navigation
from events.mouse import handle_mouse_navigation


def main_menu_screen(SCREEN: game.Surface) -> None:
    """
    Displays the main menu screen of the game.
    """
    BG = render_background(Path("assets/menu/background_menu.png"))

    BUTTONS = [
        Button(
            pos=(SCREEN.get_width() / 2, 250),
            text="PLAY",
            base_color="#D3E2D2",
            hovering_color="White",
            default_img_path=Path("assets/menu/buttons_rect/button_default.png"),
            selected_img_path=Path("assets/menu/buttons_rect/button_selected.png"),
        ),
        Button(
            pos=(SCREEN.get_width() / 2, 350),
            text="INSTRUCTIONS",
            base_color="#D3E2D2",
            hovering_color="White",
            default_img_path=Path("assets/menu/buttons_rect/button_default.png"),
            selected_img_path=Path("assets/menu/buttons_rect/button_selected.png"),
        ),
        Button(
            pos=(SCREEN.get_width() / 2, 450),
            text="EXIT",
            base_color="#D3E2D2",
            hovering_color="White",
            default_img_path=Path("assets/menu/buttons_rect/button_default.png"),
            selected_img_path=Path("assets/menu/buttons_rect/button_selected.png"),
        ),
    ]

    # Initialize selected index if it doesn't exist
    if not hasattr(main_menu_screen, "selected_idx"):
        main_menu_screen.selected_idx = 0  # Default to the first button / To manage the state of the selected button

    SOUNDS["menu"]["music"].play(loops=-1)

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = game.mouse.get_pos()

        # Render title with shadow
        render_text(
            text="BITSNAKE",
            color="#285f25",
            SCREEN=SCREEN,
            type="title",
            effect="shadow",
            offset=(7, 6.7),
        )
        render_text(
            text="BITSNAKE",
            color="#6FC96A",
            SCREEN=SCREEN,
            type="title",
            effect="none",
        )

        # Render buttons
        render_buttons(
            buttons=BUTTONS,
            screen=SCREEN,
            menu_mouse_pos=MENU_MOUSE_POS,
            selected_idx=main_menu_screen.selected_idx,
            hovering_sound=SOUNDS["menu"]["select"],
        )

        # Event handling
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()

            # Keyboard navigation
            if event.type == game.KEYDOWN:  # key press handling from keyboard
                main_menu_screen.selected_idx = handle_keydown_navigation(
                    event=event,
                    selected_idx=main_menu_screen.selected_idx,
                    num_buttons=len(BUTTONS),
                    buttons=BUTTONS,
                    screens=[level_options_screen, instructions_screen],
                    SCREEN=SCREEN,
                )

            # Mouse navigation
            if event.type == game.MOUSEBUTTONDOWN:
                main_menu_screen.selected_idx = handle_mouse_navigation(
                    event=event,
                    selected_idx=main_menu_screen.selected_idx,
                    buttons=BUTTONS,
                    screens=[level_options_screen, instructions_screen],
                    mouse_pos=MENU_MOUSE_POS,
                    SCREEN=SCREEN,
                )

        game.display.update()
