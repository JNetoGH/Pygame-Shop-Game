from JNetoProductions_pygame_game_engine.components.collider_component import ColliderComponent
from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject



class Map(GameObject):

    def __init__(self, game, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.game = game

        self.single_sprite = SingleSpriteComponent("our_game/game_res/graphics/map/loja_nossa.png", self)
        self.single_sprite.scale_itself(4)

        # walls
        self.collider_bottom = ColliderComponent(0, 550, 2000, 20, self)
        self.collider_top = ColliderComponent(0, -300, 2000, 20, self)
        self.collider_left = ColliderComponent(-710, 0, 20, 2000, self)
        self.collider_right = ColliderComponent(590, 0, 20, 2000, self)

        # balcony
        self.collider_balcony_horizontal = ColliderComponent(-400, -5, 620, 60, self)
        self.collider_balcony_vertical = ColliderComponent(-75, -80, 40, 220, self)

        # another things
        self.collider_thing1 = ColliderComponent(-620, -270, 100, 50, self)
        self.collider_thing2 = ColliderComponent(-310, -270, 120, 50, self)
        self.collider_thing3 = ColliderComponent(-150, -270, 50, 50, self)
        self.collider_thing4 = ColliderComponent(-570, -160, 110, 50, self)

        # boxes
        self.collider_boxes_lef = ColliderComponent(-670, 190, 70, 200, self)
        # boxes fruits
        self.collider_boxes_lef = ColliderComponent(560, 390, 70, 320, self)

        # bags
        self.collider_bags = ColliderComponent(450, 260, 120, 50, self)

        # wood
        self.collider_wood = ColliderComponent(-20, -100, 50, 120, self)

        # desk
        self.collider_desk = ColliderComponent(330, -80, 220, 80, self)

        # barris
        self.collider_barris1 = ColliderComponent(-300, 430, 90, 90, self)
        self.collider_barris2 = ColliderComponent(-360, 370, 90, 90, self)

        # chests
        self.collider_chests = ColliderComponent(-440, 40, 100, 80, self)

    def game_object_update(self) -> None:
        pass
