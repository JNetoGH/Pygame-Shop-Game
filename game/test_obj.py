import pygame
from _2components.single_sprite.single_sprite import SingleSprite
from _3gameobjs.game_obj import GameObject


class TestObj(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        # animation_clip = AnimationClip("clip_test", "_0resources/graphics/character/down_axe")
        # self.animationController = AnimationController([animation_clip], self)
        self.single_sprite = SingleSprite("_0resources/graphics/character/down_axe/0.png", self)
        self.single_sprite.scale_itself(2)
        self.transform.move_position(pygame.Vector2(1200, 200))

    # called every frame
    def game_object_update(self) -> None:
        #increment = pygame.Vector2(1, 1)
        #self.transform.translate(increment)
        # self.animationController.animate()
        pass

    def get_inspector_debugging_status(self) -> str:
        super(TestObj, self).get_inspector_debugging_status()
        return ""


















