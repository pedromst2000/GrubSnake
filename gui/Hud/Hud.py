import pygame as game
import os
from pathlib import Path
from renderers.text import render_text
import globals.states.score as score_state


class HUD_Score:
    """
    Class to manage and display the player's score and high score.
    """

    def __init__(self, level: str):
        """
        Constructor for the Score class.

        Initializes the score, high score, font, and apple icon.

        :param level: The current game level (used for high score tracking).
        """

        self.score: int = 0
        self.level: str = level
        self.apple_icon: game.Surface = game.image.load(
            Path("assets/graphics/items/apple.png")
        )

        # --- Trim transparent padding from the icon so centering uses visible pixels
        self.apple_icon: game.Surface = self.apple_icon.convert_alpha()
        bounds: game.Rect = self.apple_icon.get_bounding_rect()
        self.apple_icon: game.Surface = self.apple_icon.subsurface(bounds).copy()
        self.icon_size: tuple[int, int] = self.apple_icon.get_size()

        # Store base apple (unscaled, only processed once)
        self.apple_icon: game.Surface = self.apple_icon

        # HUD styling
        self.padding: int = 15
        self.spacing: int = 12
        self.bg_color: tuple[int, int, int, int] = (0, 0, 0, 50)  # semi-transparent
        self.text_color: tuple[int, int, int] = (255, 255, 255)  # white

        # High score file path
        self.file_path: str = os.path.join(
            os.path.dirname(__file__), "../../data/score.txt"
        )

        # Load high score from file (or create if missing)
        self.high_score: int = self.load_high_score()

    def reset(self):
        """Reset the score when the game ends."""
        self.score: int = 0
        score_state.apples_eaten = 0

    def add_score(self, amount: int = 1):
        """Add to the current score.

        :param amount: The amount to add to the score (default is 1).
        """
        self.score += amount
        score_state.apples_eaten = self.score  # update module-level score state
        if self.score > self.high_score:
            self.high_score: int = self.score
            self.save_high_score()  # save high score immediately when updated

    def subtract_score(self, amount: int = 1):
        """Subtract from the current score.

        :param amount: The amount to subtract from the score (default is 1).
        """
        self.score -= amount
        score_state.apples_eaten = self.score  # update module-level score state
        if self.score < 0:
            self.score = 0  # prevent negative scores
            score_state.apples_eaten = 0

    def draw_score(self, screen: game.Surface, pos=(20, 20)):
        """Draw the score HUD.

        :param screen: The surface to draw the HUD on.
        :param pos: The top-left position to draw the HUD.
        """
        text: str = f"{self.score}   HI {self.high_score}"
        text_surface: game.Surface = render_text(
            text, self.text_color, type="label", return_surface=True
        )

        # Make the icon ~1.4x the text height so it feels balanced
        icon_height: int = int(text_surface.get_height() * 1.4)
        desired_icon_size: tuple[int, int] = (icon_height, icon_height)

        if self.apple_icon.get_size() != desired_icon_size:
            icon: game.Surface = game.transform.smoothscale(
                self.apple_icon, desired_icon_size
            )
        else:
            icon: game.Surface = self.apple_icon

        # Content (icon + spacing + text)
        content_w: int = desired_icon_size[0] + self.spacing + text_surface.get_width()
        content_h: int = max(desired_icon_size[1], text_surface.get_height())

        # Box (content + padding)
        box_w: int = self.padding * 2 + content_w
        box_h: int = self.padding * 2 + content_h

        box: game.Surface = game.Surface((box_w, box_h), game.SRCALPHA)
        box_rect: game.Rect = box.get_rect()
        game.draw.rect(box, self.bg_color, box_rect, border_radius=min(box_h // 2, 16))

        center_y: int = box_h // 2  # For vertical centering

        # Icon rect
        icon_rect: game.Rect = icon.get_rect()
        icon_rect.left = self.padding
        icon_rect.centery = center_y

        # Text rect
        text_rect: game.Rect = text_surface.get_rect()
        text_rect.left = icon_rect.right + self.spacing
        text_rect.centery = center_y  # aligned with icon center

        # Blit
        box.blit(icon, icon_rect)
        box.blit(text_surface, text_rect)

        screen.blit(box, pos)

    def load_high_score(self) -> int:
        """
        Load the high score for the current level from a file.

        Returns:
            int: The high score for the current level.
        """

        # If file does not exist, create it with default structure
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(
                    f"{self.level};0\n"
                )  # write default high score for current level
            return 0

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines: list[str] = f.readlines()

        # Search for the current level in the file
        for line in lines:
            parts: list[str] = line.strip().split(";")
            if len(parts) == 2 and parts[0] == self.level:  # found level
                return int(parts[1])  # return score as int of the level
        # If not found, add entry for current level
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"{self.level};0\n")
        return 0  # default high score if level not found

    def save_high_score(self):
        """
        Save the high score to a file.
        """

        scores: dict[str, int] = {}  # To store existing scores
        if os.path.exists(self.file_path):  # if the file exists
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts: list[str] = line.strip().split(";")  # Split line into parts
                    if len(parts) == 2:  # Check if line is valid
                        scores[parts[0]] = parts[
                            1
                        ].strip()  # Store score for each level => level;score

        # Updating the score for the current level
        scores[self.level] = self.high_score

        # Writing all scores back in "level;score" format
        with open(self.file_path, "w", encoding="utf-8") as f:
            for lvl, score in scores.items():
                f.write(f"{lvl};{score}\n")
