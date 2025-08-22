import pygame as game

CELL_SIZE = 40
CELL_NUMBER_X = 25
CELL_NUMBER_Y = 15
SCREEN_WIDTH = CELL_SIZE * CELL_NUMBER_X  # 950
SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER_Y  # 570
FPS = 9.5
MOVE_EVENT = game.USEREVENT + 1 # Event triggered for snake movement
MOVE_INTERVAL_MS = 120 # milliseconds
