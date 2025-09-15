import pygame as game


def gameplay_screen(SCREEN: game.Surface, chosen_level: str) -> None:
    """
    Renders the gameplay screen for the selected difficulty level.

    Args:
        SCREEN (game.Surface): The main display surface for rendering game elements.
        chosen_level (str): The difficulty level selected by the player ("easy", "medium", "hard").

    Returns:
        None
    """
    while True:
        SCREEN.fill((0, 0, 0))  # Clear the screen with a black background

        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                exit()
            print(f"CHOSEN LEVEL: {chosen_level}")  # Debug print to show chosen level

        game.display.update()
