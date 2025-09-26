import pygame as game

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 600

# Snake & items size of the game
CELL_SIZE = 30  # the size of each cell in pixels

# Auto-calculate grid
CELL_NUMBER_X = SCREEN_WIDTH // CELL_SIZE
CELL_NUMBER_Y = SCREEN_HEIGHT // CELL_SIZE

MOVE_EVENT = game.USEREVENT + 1

# level settings with game speed and difficulty
LEVELS = {
    "easy": {
        "poison_enabled": False,
        "move_interval": 80,  # ms per snake move
    },
    "medium": {
        "poison_enabled": False,
        "move_interval": 100,
    },
    "hard": {
        "poison_enabled": True,
        "move_interval": 50,
    },
}
