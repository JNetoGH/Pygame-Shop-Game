import pygame


class Screen:

    # CANVAS SURFACE
    GameScreenSurface: pygame.Surface = None

    # SCREEN ITSELF
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
    HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2

    _REFERENCE_RESOLUTION_WIDTH = 1280
    _REFERENCE_RESOLUTION_HEIGHT = 720
    SCALE_FROM_REFERENCE = ((SCREEN_HEIGHT * 100) / _REFERENCE_RESOLUTION_HEIGHT / 100)

    TILE_SIZE = 64