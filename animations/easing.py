import pygame as game
import time


def lerp(a, b, t: float) -> float:
    """Linear interpolation between a and b by t (0.0 -> 1.0).
    
    Args:
        a (float): Start value.
        b (float): End value.
        t (float): Interpolation factor between 0.0 and 1.0.
    Returns:
    
    """
    return a + (b - a) * t


def ease_in_out_curve(t: float) -> float:
    """
    Smoothstep easing (ease-in-out curve).
    Maps t in [0,1] to eased t.

    Args:
        t (float): A value between 0.0 and 1.0 representing the interpolation factor.
    Returns:
        float: The eased interpolation factor.
    """
    return lerp(0, 1, t * t * (3 - 2 * t))


def ease_in_out(current_surf, target_surf, duration: int) -> game.Surface:
    """
    Returns an interpolated surface between current and target over the given duration.

    Args:
        current_surf (game.Surface): Current image surface.
        target_surf (game.Surface): Target image surface.
        duration (int): Transition duration in milliseconds.

    Returns:
        game.Surface: Blended/interpolated surface.
    """
    start_time = time.time()
    clock = game.time.Clock()

    # Ensure same size
    if current_surf.get_size() != target_surf.get_size():
        target_surf = game.transform.scale(target_surf, current_surf.get_size())

    while True:
        elapsed = (time.time() - start_time) * 1000  # ms
        t = min(elapsed / duration, 1.0)
        eased_t = ease_in_out_curve(t)

        # Blend images
        blended = current_surf.copy().convert_alpha()
        blended.set_alpha(int(255 * (1 - eased_t)))
        result = target_surf.copy().convert_alpha()
        result.blit(blended, (0, 0))

        yield result  # <-- Generator yields frames

        if t >= 1.0:
            break

        clock.tick(60)  # 60 FPS limit
