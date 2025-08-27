import pygame as game
import os


class Score:
    """
    Class to manage the score and high score display.
    """

    def __init__(self, font: game.font.Font, byte_icon: game.Surface) -> None:
        """
        Constructor for the Score class.

        Initializes the score, high score, font, and byte icon.
        """

        self.score = 0
        self.font = font

        # --- Trim transparent padding from the icon so centering uses visible pixels
        self.byte_icon = byte_icon.convert_alpha()
        bounds = self.byte_icon.get_bounding_rect()
        self.byte_icon = self.byte_icon.subsurface(bounds).copy()
        self.icon_size = self.byte_icon.get_size()

        # HUD styling
        self.padding = 10
        self.spacing = 12
        self.bg_color = (0, 0, 0, 35)  # semi-transparent
        self.text_color = (255, 255, 255)  # white

        # High score file path
        self.file_path = os.path.join(os.path.dirname(__file__), "../../data/score.txt")

        # Load high score from file (or create if missing)
        self.high_score = self.load_high_score()

    def reset(self) -> None:
        """Reset the score when the game ends."""
        self.score = 0

    def add_score(self, amount: int = 1) -> None:
        """Add to the current score."""
        self.score += amount
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()  # save high score when beaten - beaten means surpassing the previous high score

    def draw_score(self, screen: game.Surface, pos=(20, 20)) -> None:
        """Draw the score HUD."""
        text = f"{self.score}   HI {self.high_score}"
        text_surface = self.font.render(text, True, self.text_color)

        # Scale the icon to fit the text height
        desired_icon_size = (text_surface.get_height(),) * 2
        if self.byte_icon.get_size() != desired_icon_size:
            icon = game.transform.smoothscale(self.byte_icon, desired_icon_size)
        else:
            icon = self.byte_icon

        # Content (icon + spacing + text)
        content_w = desired_icon_size[0] + self.spacing + text_surface.get_width()
        content_h = max(desired_icon_size[1], text_surface.get_height())

        # Box (content + padding)
        box_w = self.padding * 2 + content_w
        box_h = self.padding * 2 + content_h

        box = game.Surface((box_w, box_h), game.SRCALPHA)
        box_rect = box.get_rect()
        game.draw.rect(box, self.bg_color, box_rect, border_radius=min(box_h // 2, 16))

        center_y = box_h // 2  # For vertical centering

        # Icon rect
        icon_rect = icon.get_rect()  # Get the rectangle for the icon surface
        icon_rect.left = self.padding  # Set left padding
        icon_rect.centery = center_y  # Center vertically

        # Text rect
        text_rect = text_surface.get_rect()  # Get the rectangle for the text surface
        text_rect.left = (
            icon_rect.right + self.spacing
        )  # Position text to the right of the icon
        text_rect.centery = center_y + 4  # Adjust vertical position

        # Blit - means to copy the pixels from one surface to another
        box.blit(icon, icon_rect)
        box.blit(text_surface, text_rect)

        # Place HUD on screen
        screen.blit(box, pos)

    def load_high_score(self) -> int:
        """
        Load the high score from a file.
        Returns the high score as an integer.
        """

        # If file does not exist, create it with default structure
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:  # create file if not exists
                f.write("score\n0\n")  # write default high score value as 0
            return 0

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Must have at least 2 lines: "score" and value
        if len(lines) >= 2:
            try:
                return int(lines[1].strip())  # strip for whitespace
            except ValueError:
                return 0
        return 0

    def save_high_score(self) -> None:
        """
        Save the high score to a file.
        """

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("score\n")
            f.write(f"{self.high_score}")
    