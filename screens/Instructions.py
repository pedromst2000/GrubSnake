import pygame as game


def instructions_screen(SCREEN: game.Surface) -> None:
    """
    Displays the instructions for the game.

    Args:
    - SCREEN (game.Surface): The main display surface where the instructions will be rendered.

    Returns:
    - None
    """

    while True:

        SCREEN.fill((0, 0, 0))  # Clear the screen with a black background

        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                exit()
            print("INSTRUCTIONS SCREEN")
                
        game.display.update() 
