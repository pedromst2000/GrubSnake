import pygame as game


SCREEN_WIDTH = 950
SCREEN_HEIGHT = 600

# Snake & food size
CELL_SIZE = 30  # the size of each cell in pixels

# Auto-calculate grid
CELL_NUMBER_X = SCREEN_WIDTH // CELL_SIZE  # number of cells in the x direction
CELL_NUMBER_Y = SCREEN_HEIGHT // CELL_SIZE  # number of cells in the y direction

MOVE_EVENT = game.USEREVENT + 1

# level settings with game speed and difficulty
LEVELS = {
    "easy": {
        "fps": 12,  # game speed
        "poison_enabled": False,  # whether poison appears
        "move_interval": 120,  # snake movement interval
    },
    "medium": {"fps": 25, "poison_enabled": False, "move_interval": 100},
    "hard": {"fps": 32, "poison_enabled": True, "move_interval": 80},
}
