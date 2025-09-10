import pygame as game
from pathlib import Path

game.mixer.init() # Initialize the mixer for the sounds

SOUNDS = {
    "game": {
        "eat_byte": game.mixer.Sound(Path("assets/sounds/eating_byte.wav")),
        "eat_poison": game.mixer.Sound(Path("assets/sounds/eating_poison.wav")),
        "game_over": game.mixer.Sound(Path("assets/sounds/game_over.wav")),
        "move_snake": game.mixer.Sound(Path("assets/sounds/snake_rustling.wav")),
    },
    "menu": {
        "music": game.mixer.Sound(Path("assets/sounds/menu/sound_menu.mp3")),
        "select": game.mixer.Sound(Path("assets/sounds/menu/button/select.wav")),
        "click": game.mixer.Sound(Path("assets/sounds/menu/button/click.wav")),
    },
}

SOUNDS["menu"]["music"].set_volume(0.01)
SOUNDS["game"]["eat_poison"].set_volume(0.6)
SOUNDS["game"]["game_over"].set_volume(0.6)
SOUNDS["game"]["move_snake"].set_volume(0.50)
SOUNDS["menu"]["select"].set_volume(0.5)
SOUNDS["menu"]["click"].set_volume(0.5)