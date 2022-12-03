import pygame
from _3gameobjs.game_obj import GameObject
import pygame.math as m


class TestObj(GameObject):
    def __init__(self, pos: pygame.math.Vector2, group, level):
        super().__init__(pos, group, level)

    def start(self) -> None:
        pass

    def tick(self) -> None:
        increment = pygame.math.Vector2(1, 1)
        self.transform.translate(increment)
