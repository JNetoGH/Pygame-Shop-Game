from _2components.animation.animation_clip import AnimationClip
from _2components.animation.animation_controller import AnimationController
from _2components.single_sprite.single_sprite import SingleScaledSprite
from _3gameobjs.game_obj import GameObject


class TestObj(GameObject):
    def __init__(self, level):
        super().__init__(level)

    # called just once
    def start(self) -> None:
        # animation_clip = AnimationClip("clip_test", "_0resources/graphics/character/down_axe")
        # self.animationController = AnimationController([animation_clip], self)
        self.single_sprite = SingleScaledSprite("_0resources/graphics/character/down_axe/0.png", self)
        self.single_sprite.scale_itself(2)

    # called every frame
    def tick(self) -> None:
        #increment = pygame.Vector2(1, 1)
        #self.transform.translate(increment)
        # self.animationController.animate()
        pass


















