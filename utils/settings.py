import pygame as game

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 600

# Snake & food size
CELL_SIZE = 35 # the size of each cell in pixels 

# Auto-calculate grid
CELL_NUMBER_X = SCREEN_WIDTH // CELL_SIZE # number of cells in the x direction
CELL_NUMBER_Y = SCREEN_HEIGHT // CELL_SIZE # number of cells in the y direction

# Game speed
FPS = 15
MOVE_EVENT = game.USEREVENT + 1
MOVE_INTERVAL_MS = 120
