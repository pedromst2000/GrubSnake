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
        default_img_path: Path = "assets/menu/buttons_rect/button_default.png",
        selected_img_path: Path = "assets/menu/buttons_rect/button_selected.png",
        base_color: str = "#9DC19DCC",
        hovering_color: str = "#FFFFFF",
        size: tuple[int, int] = (270, 60),
    ):
        """
        Initializes the Button object with position, text, colors, and images.

            :param pos: The (x, y) position of the button center.
            :param text: The text to display on the button.
            :param base_color: The base color of the text.
            :param hovering_color: The color of the text when hovered.
            :param default_img_path: Path to the default button image.
            :param selected_img_path: Path to the selected button image.
            :param size: (tuple[int, int], optional): Size to scale the button images. Defaults to (220, 50).

        """

        # Load button images
        self.default_image: game.Surface = game.image.load(
            default_img_path
        ).convert_alpha()
        self.selected_image: game.Surface = game.image.load(
            selected_img_path
        ).convert_alpha()

        if size:
            self.default_image: game.Surface = game.transform.scale(
                self.default_image, size
            )
            self.selected_image: game.Surface = game.transform.scale(
                self.selected_image, size
            )

        self.image: game.Surface = self.default_image
        self.rect: game.Rect = self.image.get_rect(center=pos)

        # Text attributes
        self.text_str: str = text
        self.base_color: str = base_color
        self.hovering_color: str = hovering_color

        # Render initial text surface
        self.text_surface: game.Surface = render_text(
            text=self.text_str,
            color=self.base_color,
            type="input",
            return_surface=True,  # Always return surface
        )
        self.text_rect: game.Rect = self.text_surface.get_rect(
            center=self.rect.center
        )  # Center text

        self.cursor_state: bool = False  # To manage cursor state
        self.animator: None = None  # To hold animation generator
        self.target_image: game.Surface = self.image  # Target image for animation

    def update(self, screen: game.Surface):
        """
        Method that draws the button and its text on the screen.

            :param screen: The surface to draw the button on.
        """
        if self.animator:  # If animation is running
            try:
                self.image: game.Surface = next(self.animator)
            except StopIteration:
                self.animator: None = None

        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def change_cursor(self, state: bool, hovering_sound: game.mixer.Sound):
        """
        Method that changes the cursor state to indicate interactivity.

            :param state: True to change cursor to hand, False for default.
            :param hovering_sound: Sound to play when hovering.

        """
        if state and not self.cursor_state:  # Only change if state is different
            game.mouse.set_cursor(game.SYSTEM_CURSOR_HAND)
            hovering_sound.play()  # Play hovering sound
            self.cursor_state: bool = True
        elif (
            not state and self.cursor_state
        ):  # not state means default cursor / not state it´s the same as !state
            game.mouse.set_cursor(game.SYSTEM_CURSOR_ARROW)
            self.cursor_state: bool = False

    def check_for_input(
        self, position: tuple[int, int] | None = None, selected: bool = False
    ) -> bool:
        """
        Method that checks if button is activated (mouse click or keyboard selection).

            :param position: Mouse position (or None when using keyboard).
            :param selected: True if triggered via keyboard (Enter/Space).
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
    ):
        """
        Method that updates button state (hover image + text color) with ease-in-out animation.


            :param position: The mouse position.
            :param selected: True if selected via keyboard (Arrow Up/Down).
            :param duration: Animation duration in milliseconds.

        """
        hovered: bool = self.rect.collidepoint(position)
        target_image: game.Surface = (
            self.selected_image if (selected or hovered) else self.default_image
        )
        target_color: game.Color = (
            self.hovering_color if (selected or hovered) else self.base_color
        )

        if self.target_image != target_image:  # State change
            self.target_image = target_image
            self.animator: None = ease_in_out(self.image, self.target_image, duration)

        # Always update text color
        self.text_surface: game.Surface = render_text(
            text=self.text_str,
            color=target_color,
            type="input",
            return_surface=True,
        )
        self.text_rect: game.Rect = self.text_surface.get_rect(center=self.rect.center)
