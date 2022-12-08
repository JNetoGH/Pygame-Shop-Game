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
        self.collider_balcony_horizontal = Collider(-400, -5, 550, 40, self)
        self.collider_balcony_left = Collider(-70, -80, 30, 220, self)
        # another things
        self.collider_thing1 = Collider(-620, -270, 100, 50, self)
        self.collider_thing2 = Collider(-310, -270, 120, 50, self)
        self.collider_thing3 = Collider(-150, -270, 50, 50, self)
        self.collider_thing4 = Collider(-570, -160, 110, 50, self)

        # boxes
        self.collider_boxes_lef = Collider(-670, 190, 70, 200, self)
        # boxes fruits
        self.collider_boxes_lef = Collider(560, 390, 70, 320, self)

        # bags
        self.collider_bags = Collider(450, 260, 120, 50, self)

        # wood
        self.collider_wood = Collider(-20, -100, 50, 120, self)

        # desk
        self.collider_desk = Collider(330, -80, 220, 80, self)

        # barris
        self.collider_barris1 = Collider(-300, 430, 90, 90, self)
        self.collider_barris2 = Collider(-360, 370, 90, 90, self)

        # chests
        self.collider_chests = Collider(-440, 40, 100, 80, self)

