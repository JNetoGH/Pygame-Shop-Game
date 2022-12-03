import pygame

from _2components.animation.animation_clip import AnimationClip
from _2components.animation.animation_controller import AnimationController
from _3gameobjs.game_obj import GameObject


class TestObj(GameObject):
    def __init__(self, pos: pygame.Vector2, level):
        super().__init__(pos, level)

    # called just once
    def start(self) -> None:
        animation_clip = AnimationClip("clip_test", "_0resources/graphics/character/down_axe")
        self.animationController = AnimationController([animation_clip], self)

    # called every frame
    def tick(self) -> None:
        #increment = pygame.Vector2(1, 1)
        #self.transform.translate(increment)
        self.animationController.animate()


















