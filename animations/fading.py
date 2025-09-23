import pygame as game
import time


def lerp(a: float, b: float, t: float) -> float:
    """
    Linear interpolation between a and b by t.

    Args:
        a (float): Start value.
        b (float): End value.
        t (float): Interpolation factor in [0, 1].

    Returns:
        float: Interpolated value.

    """
    return a + (b - a) * t


def ease_in_out_curve(t: float) -> float:
    """
    Smoothstep easing (ease-in-out).
    Maps t in [0,1] to eased t.

    Args:
        t (float): Input time factor in [0, 1].
    Returns:
        float: Eased time factor in [0, 1].
    """
    return lerp(0, 1, t * t * (3 - 2 * t))


def fade_in(
    SCREEN: game.Surface, draw_callback: callable, duration: int = 1000
) -> None:
    """
    Performs a fade-in animation for the given screen.

    Args:
        SCREEN (game.Surface): Main display surface.
        draw_callback (callable): Function to draw the screen content (called every frame).
        duration (int): Duration of the fade-in effect in milliseconds.
    Returns:
        None
    """
    clock = game.time.Clock()
    start_time = time.time()

    while True:
        elapsed = (time.time() - start_time) * 1000  # ms
        t = min(elapsed / duration, 1.0)
        eased_t = ease_in_out_curve(t)

        # First draw normal screen
        draw_callback()

        # Copy screen content and overlay black with decreasing opacity
        overlay = game.Surface(SCREEN.get_size()).convert_alpha()
        overlay.fill((0, 0, 0, int(255 * (1 - eased_t))))
        SCREEN.blit(overlay, (0, 0))

        game.display.update()

        if t >= 1.0:
            break

        clock.tick(60)  # Limit FPS
