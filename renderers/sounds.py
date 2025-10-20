import pygame as game
from pathlib import Path

game.mixer.init()  # Initialize the mixer for the sounds

EAT_APPLE_SOUND = game.mixer.Sound(Path("assets/sounds/eating_apple.wav"))
EAT_POISON_SOUND = game.mixer.Sound(Path("assets/sounds/eating_poison.wav"))
GAME_OVER_SOUND = game.mixer.Sound(Path("assets/sounds/game_over.wav"))
MOVE_SNAKE_SOUND = game.mixer.Sound(Path("assets/sounds/snake_rustling.wav"))
MENU_MUSIC_SOUND = game.mixer.Sound(Path("assets/sounds/menu/sound_menu.mp3"))
SELECT_BTN_SOUND = game.mixer.Sound(Path("assets/sounds/menu/button/select.wav"))
CLICK_BTN_SOUND = game.mixer.Sound(Path("assets/sounds/menu/button/click.wav"))


MENU_MUSIC_SOUND.set_volume(0.01)
EAT_POISON_SOUND.set_volume(0.6)
GAME_OVER_SOUND.set_volume(0.6)
MOVE_SNAKE_SOUND.set_volume(0.50)
SELECT_BTN_SOUND.set_volume(0.5)
CLICK_BTN_SOUND.set_volume(0.5)
