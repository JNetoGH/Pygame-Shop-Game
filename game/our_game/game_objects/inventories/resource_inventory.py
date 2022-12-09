import pygame

from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.inventories.inventory_item import InventoryItem


class ResInventory(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.single_sprite = SingleSpriteComponent("our_game/game_res/graphics/ui/inventory.png", self)
        self.single_sprite.scale_itself(4)
        posi_res_y_in_screen = ScalableGameScreen.DummyScreenHeight - 125
        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, posi_res_y_in_screen))

        # Res List
        self.resources: list[InventoryItem] = [
            InventoryItem("leather", 5, 50, "our_game/game_res/graphics/crafting_resources/leather.png", self.scene, self.rendering_layer),
            InventoryItem("stick_madeira", 10, 50, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, self.rendering_layer),
            InventoryItem("stick_iron", 10, 50, "our_game/game_res/graphics/crafting_resources/stick_iron.png", self.scene, self.rendering_layer),
            InventoryItem("bronze", 2, 50, "our_game/game_res/graphics/crafting_resources/bronze.png", self.scene, self.rendering_layer),
            InventoryItem("ferro", 2, 50, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, self.rendering_layer),
            InventoryItem("ouro", 15, 50, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, self.rendering_layer),
            InventoryItem("rubi", 10, 50, "our_game/game_res/graphics/crafting_resources/rubi.png", self.scene, self.rendering_layer),
            InventoryItem("diamante", 15, 50, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, self.rendering_layer)
                                        ]

    def add_amount(self, quantity, res_name):
        for res in self.resources:
            if res.name == res_name:
                res.add_amount(quantity)

    def remove_amount(self, quantity, res_name):
        for res in self.resources:
            if res.name == res_name:
                res.remove_amount(quantity)

    def game_object_update(self) -> None:
        # aligns the existing itens sprite with the inventory
        posi_res_y_in_screen = ScalableGameScreen.DummyScreenHeight - 119
        inital_x = ScalableGameScreen.HalfDummyScreenWidth - 196
        posi_res_x_is_screen = inital_x
        espacamento = 56

        for res in self.resources:
            res.fix_game_object_on_screen(pygame.Vector2(posi_res_x_is_screen, posi_res_y_in_screen))
            # last step
            posi_res_x_is_screen += espacamento

    def see_status(self):
        for res in self.resources:
            print(res.to_string())
            print()



