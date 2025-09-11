import pygame as game
from pathlib import Path
from renderers.text import render_text


class Button:
    """
    A GUI Button with hover and click states.
    """

    def __init__(
        self,
        pos: tuple[int, int],
        text: str,
        base_color: str,
        hovering_color: str,
        default_img_path: Path,
        selected_img_path: Path,
        size: tuple[int, int] = (220, 50),
    ) -> None:

        # Load button images
        self.default_image = game.image.load(default_img_path).convert_alpha()
        self.selected_image = game.image.load(selected_img_path).convert_alpha()

        if size:
            self.default_image = game.transform.scale(self.default_image, size)
            self.selected_image = game.transform.scale(self.selected_image, size)

        self.image = self.default_image
        self.rect = self.image.get_rect(center=pos)

        # Text attributes
        self.text_str = text
        self.base_color = base_color
        self.hovering_color = hovering_color

        # Render initial text surface
        self.text_surface = render_text(
            text=self.text_str,
            color=self.base_color,
            type="input",
            return_surface=True,  # Always return surface
        )
        self.text_rect = self.text_surface.get_rect(
            center=self.rect.center
        )  # Center text

        self.cursor_state = False  # To manage cursor state

    def update(self, screen: game.Surface) -> None:
        """
        Method that draws the button and its text on the screen.

        Args:
            screen (game.Surface): The surface to draw the button on.

        Returns:
            None
        """
        screen.blit(self.image, self.rect)  # Draw button image
        screen.blit(self.text_surface, self.text_rect)  # Draw button text

    def change_cursor(self, state: bool, hovering_sound: game.mixer.Sound) -> None:
        """
        Method that changes the cursor state to indicate interactivity.

        Args:
            state (bool): True to change cursor to hand, False for default.
            hovering_sound (game.mixer.Sound): Sound to play when hovering.

        Returns:
            None
        """
        if state and not self.cursor_state:  # Only change if state is different
            game.mouse.set_cursor(game.SYSTEM_CURSOR_HAND)
            hovering_sound.play()  # Play hovering sound
            self.cursor_state = True
        elif (
            not state and self.cursor_state
        ):  # not state means default cursor / not state it´s the same as !state
            game.mouse.set_cursor(game.SYSTEM_CURSOR_ARROW)
            self.cursor_state = False

    def check_for_input(
        self, position: tuple[int, int] | None = None, selected: bool = False
    ) -> bool:
        """
        Method that checks if button is activated (mouse click or keyboard selection).

        Args:
            position (tuple[int, int] | None): Mouse position (or None when using keyboard).
            selected (bool): True if triggered via keyboard (Enter/Space).
        Returns:
            bool: True if activated, False otherwise.
        """
        if position is not None and self.rect.collidepoint(position):
            return True
        if selected:  # Triggered via keyboard
            return True
        return False

    def change_state(self, position: tuple[int, int], selected: bool = False) -> None:
        """
        Method that updates button state (hover image + text color).

        Args:
            position (tuple[int, int]): The mouse position.
            selected (bool): True if selected via keyboard (Arrow Up/Down).

        Returns:
            None
        """
        hovered = self.rect.collidepoint(position)  # Check if mouse is over button

        if selected or hovered:  # If selected via keyboard or hovered via mouse
            if self.image != self.selected_image:
                self.image = self.selected_image
                self.text_surface = render_text(
                    text=self.text_str,
                    color=self.hovering_color,
                    type="input",
                    return_surface=True,
                )
        else:  # If not hovered or selected
            if self.image != self.default_image:
                self.image = self.default_image
                self.text_surface = render_text(
                    text=self.text_str,
                    color=self.base_color,
                    type="input",
                    return_surface=True,
                )

        # Keep text centered on button
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
