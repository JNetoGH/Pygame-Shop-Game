import pygame
from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.inventories.recipe import Recipe
from our_game.game_objects.inventories.inventory_item import InventoryItem


class CraftablesInventory(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.single_sprite = SingleSpriteComponent("our_game/game_res/graphics/ui/inventario2.png", self)
        self.single_sprite.scale_itself(4)
        posi_res_y_in_screen = ScalableGameScreen.DummyScreenHeight - 41
        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, posi_res_y_in_screen))

        # craftables prices List
        esp_bronze_value = 10
        esp_ferro_value = 10
        esp_ouro_value = 2
        esp_rubi_value = 2
        esp_diamante_value = 15
        hammer_iron_value = 15
        bow_value = 15
        bronze_feet_value = 15
        diamante_helm_value = 15
        iron_chest_value = 15
        iron_helm_value = 15
        leather_legs_value = 15
        ouro_helm_value = 15
        ouro_legs_value = 15
        rubi_feet_value = 15

        self.craftables: list[InventoryItem] = [
            InventoryItem("esp_bronze", esp_bronze_value, 0, "our_game/game_res/graphics/craftables/espada_bronze.png", self.scene, self.rendering_layer),
            InventoryItem("esp_ferro", esp_ferro_value, 0, "our_game/game_res/graphics/craftables/espada_ferro.png", self.scene, self.rendering_layer),
            InventoryItem("esp_ouro", esp_ouro_value, 5, "our_game/game_res/graphics/craftables/espada_ouro.png", self.scene, self.rendering_layer),
            InventoryItem("esp_rubi", esp_rubi_value, 5, "our_game/game_res/graphics/craftables/espada_rubi.png", self.scene, self.rendering_layer),
            InventoryItem("esp_diamante", esp_diamante_value, 1, "our_game/game_res/graphics/craftables/espada_diamante.png", self.scene,self.rendering_layer),
            InventoryItem("hammer_iron", hammer_iron_value, 1, "our_game/game_res/graphics/craftables/hammer_iron.png", self.scene, self.rendering_layer),
            InventoryItem("bow", bow_value, 1, "our_game/game_res/graphics/craftables/bow.png", self.scene, self.rendering_layer),

            InventoryItem("bronze_feet", bronze_feet_value, 1, "our_game/game_res/graphics/craftables/bronze_feet.png", self.scene, self.rendering_layer),
            InventoryItem("diamante_helm", diamante_helm_value, 1, "our_game/game_res/graphics/craftables/diamante_helm.png", self.scene, self.rendering_layer),
            InventoryItem("iron_chest", iron_chest_value, 1, "our_game/game_res/graphics/craftables/iron_chest.png", self.scene, self.rendering_layer),
            InventoryItem("iron_helm", iron_helm_value, 1, "our_game/game_res/graphics/craftables/iron_helm.png",  self.scene, self.rendering_layer),
            InventoryItem("leather_legs", leather_legs_value, 1, "our_game/game_res/graphics/craftables/leather_legs.png", self.scene, self.rendering_layer),
            InventoryItem("ouro_helm", ouro_helm_value, 1, "our_game/game_res/graphics/craftables/ouro_helm.png", self.scene, self.rendering_layer),
            InventoryItem("ouro_legs", ouro_legs_value, 1, "our_game/game_res/graphics/craftables/ouro_legs.png", self.scene, self.rendering_layer),
            InventoryItem("rubi_feet", rubi_feet_value, 1, "our_game/game_res/graphics/craftables/rubi_feet.png", self.scene, self.rendering_layer),
                                        ]

        # MAKING RECipeS
        overall_layer = self.scene.all_rendering_layers[-1]

        # receita copper sword
        item1 = InventoryItem("stick_madeira", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item2 = InventoryItem("bronze", 0, 5, "our_game/game_res/graphics/crafting_resources/bronze.png", self.scene, overall_layer)
        item3 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("esp_bronze", esp_bronze_value, 1, "our_game/game_res/graphics/craftables/espada_bronze.png", self.scene, overall_layer)
        self.copper_sword_recipe = Recipe("copper sword", True, 20, 10, required_items, output, self.scene, self.rendering_layer)

        # receita ferro sword
        item1 = InventoryItem("stick_madeira", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item2 = InventoryItem("ouro", 0, 2, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        item3 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("esp_ferro", esp_ferro_value, 1, "our_game/game_res/graphics/craftables/espada_ferro.png", self.scene, overall_layer)
        self.iron_sword_recipe = Recipe("iron sword", True, 30, 10, required_items, output, self.scene, self.rendering_layer)

        # receita bow
        item1 = InventoryItem("stick_madeira", 0, 5, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 2, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("stick_madeira", 0, 5, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("bow", bow_value, 1, "our_game/game_res/graphics/craftables/bow.png", self.scene, overall_layer)
        self.bow_recipe = Recipe("bow", False, 5, 10, required_items, output, self.scene, self.rendering_layer)

        # receita ouro sword
        item1 = InventoryItem("stick_madeira", 0, 5, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 2, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("ouro", 0, 5, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("esp_ouro", esp_ouro_value, 1, "our_game/game_res/graphics/craftables/espada_ouro.png", self.scene, overall_layer)
        self.ouro_sword_recipe = Recipe("ouro sword", False, 20, 10, required_items, output, self.scene, self.rendering_layer)

        # receita diamante sword
        item1 = InventoryItem("stick_iron", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_iron.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("diamante", 0, 5, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("esp_diamante", esp_diamante_value, 1, "our_game/game_res/graphics/craftables/espada_diamante.png", self.scene, overall_layer)
        self.diamond_sword_recipe = Recipe("diamond sword", False, 30, 10, required_items, output, self.scene, self.rendering_layer)

        # receita rubi sword
        item1 = InventoryItem("stick_iron", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_iron.png", self.scene, overall_layer)
        item2 = InventoryItem("diamante", 0, 10, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        item3 = InventoryItem("rubi", 0, 5, "our_game/game_res/graphics/crafting_resources/rubi.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("esp_rubi", esp_rubi_value, 1, "our_game/game_res/graphics/craftables/espada_rubi.png", self.scene, overall_layer)
        self.rubi_sword_recipe = Recipe("rubi sword", False, 40, 10, required_items, output, self.scene, self.rendering_layer)

        # receita iron hammer
        item1 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("stick_madeira", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item4 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3, item4]

        output = InventoryItem("hammer_iron", hammer_iron_value, 1, "our_game/game_res/graphics/craftables/hammer_iron.png", self.scene, overall_layer)
        self.iron_hammer_recipe = Recipe("iron hammer", False, 10, 10, required_items, output, self.scene, self.rendering_layer)

        # receita iron chest
        item1 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item4 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3, item4]

        output = InventoryItem("iron_chest", iron_chest_value, 1, "our_game/game_res/graphics/craftables/iron_chest.png", self.scene, overall_layer)
        self.iron_chest_recipe = Recipe("iron chest", False, 20, 10, required_items, output, self.scene, self.rendering_layer)

        # receita iron helm
        item1 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("iron_helm", iron_helm_value, 1, "our_game/game_res/graphics/craftables/iron_helm.png", self.scene, overall_layer)
        self.iron_helm_recipe = Recipe("iron helm", False, 20, 10, required_items, output, self.scene, self.rendering_layer)

        # receita leather legs
        item1 = InventoryItem("leather", 0, 15, "our_game/game_res/graphics/crafting_resources/leather.png", self.scene, overall_layer)
        item2 = InventoryItem("iron", 0, 1, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2]

        output = InventoryItem("leather_legs", leather_legs_value, 1, "our_game/game_res/graphics/craftables/leather_legs.png", self.scene, overall_layer)
        self.leather_legs_recipe = Recipe("leather legs", False, 5, 10, required_items, output, self.scene, self.rendering_layer)

        # receita ouro helm
        item1 = InventoryItem("ouro", 0, 10, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        item2 = InventoryItem("ouro", 0, 10, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        item3 = InventoryItem("ouro", 0, 10, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("ouro_helm", ouro_helm_value, 1, "our_game/game_res/graphics/craftables/ouro_helm.png", self.scene, overall_layer)
        self.ouro_helm_recipe = Recipe("ouro helm", False, 15, 10, required_items, output, self.scene, self.rendering_layer)

        # receita ouro legs
        item1 = InventoryItem("ouro", 0, 15, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        item2 = InventoryItem("iron", 0, 1, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2]

        output = InventoryItem("ouro_legs", ouro_legs_value, 1, "our_game/game_res/graphics/craftables/ouro_legs.png", self.scene, overall_layer)
        self.ouro_legs_recipe = Recipe("ouro legs", False, 15, 10, required_items, output, self.scene, self.rendering_layer)

        # receita rubi feet
        item1 = InventoryItem("rubi", 0, 15, "our_game/game_res/graphics/crafting_resources/rubi.png", self.scene, overall_layer)
        item2 = InventoryItem("rubi", 0, 15, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        required_items = [item1, item2]

        output = InventoryItem("rubi_feet", rubi_feet_value, 1, "our_game/game_res/graphics/craftables/rubi_feet.png", self.scene, overall_layer)
        self.rubi_feet_recipe = Recipe("rubi feet", False, 45, 10, required_items, output, self.scene, self.rendering_layer)

        # receita bronze feet
        item1 = InventoryItem("bronze", 0, 15, "our_game/game_res/graphics/crafting_resources/bronze.png", self.scene, overall_layer)
        item2 = InventoryItem("bronze", 0, 15, "our_game/game_res/graphics/crafting_resources/bronze.png", self.scene, overall_layer)
        required_items = [item1, item2]

        output = InventoryItem("bronze_feet", bronze_feet_value, 1, "our_game/game_res/graphics/craftables/bronze_feet.png", self.scene, overall_layer)
        self.bronze_feet_recipe = Recipe("bronze feet", False, 10, 10, required_items, output, self.scene, self.rendering_layer)

        # receita diamante helm
        item1 = InventoryItem("diamante", 0, 10, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        item2 = InventoryItem("diamante", 0, 10, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        item3 = InventoryItem("diamante", 0, 10, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]

        output = InventoryItem("diamante_helm", diamante_helm_value, 1, "our_game/game_res/graphics/craftables/diamante_helm.png", self.scene, overall_layer)
        self.diamond_helm_recipe = Recipe("diamond helm", False, 30, 10, required_items, output, self.scene, self.rendering_layer)

        self.recipes = [self.copper_sword_recipe, self.iron_sword_recipe, self.bow_recipe, self.ouro_sword_recipe,
                        self.diamond_sword_recipe, self.rubi_sword_recipe, self.iron_hammer_recipe,
                        self.iron_chest_recipe, self.iron_helm_recipe, self.leather_legs_recipe, self.ouro_helm_recipe,
                        self.ouro_legs_recipe, self.rubi_feet_recipe, self.bronze_feet_recipe, self.diamond_helm_recipe]

        # deixa o player ter acesso a todas por padrao
        for recipe in self.recipes:
            recipe.player_has_me = True

        for recipe in self.recipes:
            recipe.stop_showing_recipe_on_screen()

    def add_amount(self, quantity, res_name):
        for res in self.craftables:
            if res.name == res_name:
                res.add_amount(quantity)

    def remove_amount(self, quantity, res_name):
        for res in self.craftables:
            if res.name == res_name:
                res.remove_amount(quantity)

    def game_object_update(self) -> None:
        # aligns the existing itens sprite with the inventory
        posi_res_y_in_screen = ScalableGameScreen.DummyScreenHeight - 42
        inital_x = ScalableGameScreen.HalfDummyScreenWidth - 392
        posi_res_x_is_screen = inital_x
        espacamento = 56

        for res in self.craftables:
            res.fix_game_object_on_screen(pygame.Vector2(posi_res_x_is_screen, posi_res_y_in_screen))
            # last step
            posi_res_x_is_screen += espacamento

    def see_status(self):
        for craftable in self.craftables:
            print(craftable.to_string())
            print()


