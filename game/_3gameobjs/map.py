from _2components.collider.collider import Collider
from _2components.single_sprite.single_sprite import SingleSprite
from _3gameobjs.game_object_base_class import GameObject


class Map(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.single_sprite = SingleSprite("game_res/graphics/map/loja_nossa.png", self)
        self.single_sprite.scale_itself(4)

        # walls
        self.collider_bottom = Collider(0, 550, 2000, 20, self)
        self.collider_top = Collider(0, -300, 2000, 20, self)
        self.collider_left = Collider(-710, 0, 20, 2000, self)
        self.collider_right = Collider(590, 0, 20, 2000, self)

        # balcony
        self.collider_balcony_horizontal = Collider(-600, 0, 0, 0, self)

        # boxes
        self.collider_boxes_lef = Collider(-670, 190, 70, 200, self)
