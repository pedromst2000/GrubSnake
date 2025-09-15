import pygame as game


def level_screen(SCREEN: game.Surface, chosen_level: str) -> None:
    """
    Displays game of the chosen level.

    Args:
        SCREEN (game.Surface): The main display surface where the game will be rendered.
        chosen_level (str): The selected difficulty level ("easy", "medium", "hard").

    Returns:
        None
    """
    while True:
        SCREEN.fill((0, 0, 0))  # Clear the screen with a black background

        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                exit()
            print(f'CHOSEN LEVEL: {chosen_level}')  # Debug print to show chosen level

        game.display.update()
