import pygame as game


def instructions_screen(SCREEN: game.Surface):
    """
    Displays the instructions screen.

    :param SCREEN: The main display surface where the instructions will be rendered.
    """

    while True:

        SCREEN.fill((0, 0, 0))  # Clear the screen with a black background

        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                exit()
            print("INSTRUCTIONS SCREEN")

        game.display.update()
