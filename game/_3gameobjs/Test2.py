import pygame

from _2components.collider.collider import Collider
from _2components.single_sprite.single_sprite import SingleSprite
from _3gameobjs.game_object_base_class import GameObject


class Test2Obj(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.transform.move_world_position(pygame.Vector2(700,700))
        self.sprite = SingleSprite("game_res/graphics/seeds/corn.png", self)
        self.collider = Collider(0, 0, 100, 100,self)

    def game_object_update(self) -> None:
        direction = pygame.Vector2(0, 5)
        new_posix = self.transform.world_position.x + direction.x
        new_posiy = self.transform.world_position.y + direction.y
        new_posi = pygame.Vector2(new_posix, new_posiy)

        self.transform.move_world_position_with_collisions_calculations(new_posi)
