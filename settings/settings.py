import pygame as game

SCREEN_WIDTH: int = 950
SCREEN_HEIGHT: int = 600

# TODO:
# THE CELL_SIZE SHOULD BE ADJUSTABLE WHILE THE SCORE INCREASES (TO A LIMIT) FOR A DECREASE VIEW OF THE MAP EFFECT TO BE POSSIBLE TO REACH HIGH SCORES VALUES
# THIS WILL REQUIRE ADJUSTMENTS IN THE SPAWNING OF ITEMS AND OBSTACLES TO AVOID IMPOSSIBLE SITUATIONS
# IT SHOULD HAVE A MINIMUM AND A MAXIMUM CELL SIZE
# IT SHOULD HAVE A MAXIMUM SCORE VALUE TO REACH (E.G., 1000 POINTS) TO WIN THE GAME


# Snake & items size of the game
CELL_SIZE: int = 23  # the size of each cell in pixels

# Auto-calculate grid
CELL_NUMBER_X: int = SCREEN_WIDTH // CELL_SIZE
CELL_NUMBER_Y: int = SCREEN_HEIGHT // CELL_SIZE

SCREEN_WIDTH: int = CELL_NUMBER_X * CELL_SIZE
SCREEN_HEIGHT: int = CELL_NUMBER_Y * CELL_SIZE

MOVE_EVENT: int = game.USEREVENT + 1

# level settings with game speed and difficulty
LEVELS: dict[str, dict[str, int]] = {
    "easy": {
        "move_interval": 75,  # ms per snake move
    },
    "medium": {
        "move_interval": 50,
    },
    "hard": {
        "move_interval": 55,
    },
}
