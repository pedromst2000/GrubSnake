import pygame as game
from pathlib import Path
from renderers.text import render_text
from animations.easing import ease_in_out


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
        self.animator = None  # To hold animation generator
        self.target_image = self.image  # Target image for animation

    def update(self, screen: game.Surface) -> None:
        """
        Method that draws the button and its text on the screen.

        Args:
            screen (game.Surface): The surface to draw the button on.

        Returns:
            None
        """
        if self.animator:  # If animation is running
            try:
                self.image = next(self.animator)
            except StopIteration:
                self.animator = None

        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

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

    def change_state(
        self, position: tuple[int, int], selected: bool = False, duration: int = 550
    ) -> None:
        """
        Method that updates button state (hover image + text color) with ease-in-out animation.

        Args:
            position (tuple[int, int]): The mouse position.
            selected (bool): True if selected via keyboard (Arrow Up/Down).
            duration (int): Animation duration in milliseconds.

        Returns:
            None
        """
        hovered = self.rect.collidepoint(position)
        target_image = (
            self.selected_image if (selected or hovered) else self.default_image
        )
        target_color = self.hovering_color if (selected or hovered) else self.base_color

        if self.target_image != target_image:  # State change
            self.target_image = target_image
            self.animator = ease_in_out(self.image, self.target_image, duration)

        # Always update text color
        self.text_surface = render_text(
            text=self.text_str,
            color=target_color,
            type="input",
            return_surface=True,
        )
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
