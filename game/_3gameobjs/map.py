from _2components.collider.collider import Collider
from _2components.single_sprite.single_sprite import SingleSprite
from _3gameobjs.game_object import GameObject


class Map(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.single_sprite = SingleSprite("_0resources/graphics/map/base_map.png", self)
        self.collider1 = Collider(0, 700, 1000, 30, self)
        self.collider1 = Collider(400, 0, 30, 2000, self)