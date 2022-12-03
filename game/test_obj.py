import pygame

from _3gameobjs.game_obj import GameObject


class TestObj(GameObject):
    def __init__(self, pos: pygame.math.Vector2, group, level):
        super().__init__(pos, group, level)
