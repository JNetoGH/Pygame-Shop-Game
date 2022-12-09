import random

import pygame
from JNetoProductions_pygame_game_engine.components.single_sprite.single_sprite import SingleSprite
from JNetoProductions_pygame_game_engine.components.text_render.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.inventories.inventory_item import InventoryItem


class Recipe(GameObject):
    def __init__(self, name:str, success_rating, buying_price,
                 list_of_resources_for_crafting: list[InventoryItem], craftable_out_put, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.buying_price = buying_price
        self.success_rating = success_rating

        self.list_of_resources_for_crafting = list_of_resources_for_crafting
        self.craftable_output = craftable_out_put

        self.fix_game_object_on_screen(pygame.Vector2(
            ScalableGameScreen.HalfDummyScreenWidth,
            ScalableGameScreen.HalfDummyScreenHeight-50)
        )
        self.single_sprite = SingleSprite("our_game/game_res/graphics/ui/receitas_layout.png", self)
        self.single_sprite.scale_itself(4)

        self.name_text_render = TextRenderComponent(self.name, 20, pygame.Color(0, 0, 0), 10, 65, self)
        self.success_rating_text_render = TextRenderComponent(f"success rating: {self.success_rating}",
                                                              15, pygame.Color(0, 0, 0), 10, 85, self)
        self.last_craft_attempt_status_text_render = TextRenderComponent(f"last attempt: none",
                                                              15, pygame.Color(0, 0, 0), 10, 105, self)

    def game_object_update(self) -> None:
        # align required res at their pos on the squares
        counter = 0
        espacamento = 56
        posi_res_y_in_screen = 238
        inital_x = 567
        posi_res_x_is_screen = inital_x
        for res in self.list_of_resources_for_crafting:
            counter += 1
            if counter == 3:
                posi_res_x_is_screen = inital_x
                posi_res_y_in_screen += 55
            new_pos_on_screen = pygame.Vector2()
            new_pos_on_screen.x = posi_res_x_is_screen
            new_pos_on_screen.y = posi_res_y_in_screen
            res.fix_game_object_on_screen(new_pos_on_screen)
            posi_res_x_is_screen += espacamento

        # aligns the output craft
        output_in_screen_x = 740
        output_in_screen_y = 270
        self.craftable_output.fix_game_object_on_screen(pygame.Vector2(output_in_screen_x, output_in_screen_y))

    def show_recipe_recept_on_screen(self):
        self.start_rendering_this_game_object()
        self.craftable_output.start_rendering_this_game_object()
        for res in self.list_of_resources_for_crafting:
            res.start_rendering_this_game_object()

    def stop_showing_recipe_on_screen(self):
        self.stop_rendering_this_game_object()
        self.craftable_output.stop_rendering_this_game_object()
        for res in self.list_of_resources_for_crafting:
            res.stop_rendering_this_game_object()

    def craft(self, player, list_of_given_res: list[InventoryItem], output_craftables_list: list[InventoryItem]):

        # check if there is enough of all the required resources in case not, just returns
        for given_res in list_of_given_res:
            for req_res in self.list_of_resources_for_crafting:
                if given_res.name == req_res.name:
                    if given_res.amount < req_res.amount:
                        return

        # reduce the amount subtracting the cost of the recipe
        for given_res in list_of_given_res:
            for req_res in self.list_of_resources_for_crafting:
                if given_res.name == req_res.name:
                    given_res.remove_amount(req_res.amount)

        # if success rates fails, the resources are consumed, but the output crafting item is not generated
        failed = True
        PlayerCraftAttempt = player.exp * random.randint(1, 10)
        if PlayerCraftAttempt >= self.success_rating:
            failed = False
        if failed:
            self.last_craft_attempt_status_text_render.change_text("last attempt: failed")
            self.last_craft_attempt_status_text_render.change_color(pygame.Color(255, 0, 0))
            return
        else:
            self.last_craft_attempt_status_text_render.change_text("last attempt: success")
            self.last_craft_attempt_status_text_render.change_color(pygame.Color(0, 128, 0))
            player.exp += player.exp_enhancement_per_success_in_craft

        # adds up the amount of the recipe to the inventory
        for craft in output_craftables_list:
            if craft.name == self.craftable_output.name:
                craft.add_amount(self.craftable_output.amount)


class CraftablesInventory(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.single_sprite = SingleSprite("our_game/game_res/graphics/ui/inventario2.png", self)
        self.single_sprite.scale_itself(4)
        posi_res_y_in_screen = ScalableGameScreen.DummyScreenHeight - 41
        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, posi_res_y_in_screen))

        # craftables List
        self.craftables: list[InventoryItem] = [
            InventoryItem("esp_bronze", 10, 0, "our_game/game_res/graphics/craftables/espada_bronze.png", self.scene, self.rendering_layer),
            InventoryItem("esp_ferro", 10, 0, "our_game/game_res/graphics/craftables/espada_ferro.png", self.scene, self.rendering_layer),
            InventoryItem("esp_ouro", 2, 5, "our_game/game_res/graphics/craftables/espada_ouro.png", self.scene, self.rendering_layer),
            InventoryItem("esp_rubi", 2, 5, "our_game/game_res/graphics/craftables/espada_rubi.png", self.scene, self.rendering_layer),
            InventoryItem("esp_diamante", 15, 1, "our_game/game_res/graphics/craftables/espada_diamante.png", self.scene,self.rendering_layer),
            InventoryItem("hammer_iron", 15, 1, "our_game/game_res/graphics/craftables/hammer_iron.png", self.scene, self.rendering_layer),
            InventoryItem("bow", 15, 1, "our_game/game_res/graphics/craftables/bow.png", self.scene, self.rendering_layer),

            InventoryItem("bronze_feet", 15, 1, "our_game/game_res/graphics/craftables/bronze_feet.png", self.scene, self.rendering_layer),
            InventoryItem("diamante_helm", 15, 1, "our_game/game_res/graphics/craftables/diamante_helm.png", self.scene, self.rendering_layer),
            InventoryItem("iron_chest", 15, 1, "our_game/game_res/graphics/craftables/iron_chest.png", self.scene, self.rendering_layer),
            InventoryItem("iron_hem", 15, 1, "our_game/game_res/graphics/craftables/iron_helm.png",  self.scene, self.rendering_layer),
            InventoryItem("leather_legs", 15, 1, "our_game/game_res/graphics/craftables/leather_legs.png", self.scene, self.rendering_layer),
            InventoryItem("ouro_helm", 15, 1, "our_game/game_res/graphics/craftables/ouro_helm.png", self.scene, self.rendering_layer),
            InventoryItem("ouro_legs", 15, 1, "our_game/game_res/graphics/craftables/ouro_legs.png", self.scene, self.rendering_layer),
            InventoryItem("rubi_feet", 15, 1, "our_game/game_res/graphics/craftables/rubi_feet.png", self.scene, self.rendering_layer),
                                        ]

        # MAKING RECEPTS
        overall_layer = self.scene.all_rendering_layers[-1]

        # receita copper sword
        item1 = InventoryItem("stick_madeira", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item2 = InventoryItem("bronze", 0, 5, "our_game/game_res/graphics/crafting_resources/bronze.png", self.scene, overall_layer)
        item3 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("esp_bronze", 0, 1, "our_game/game_res/graphics/craftables/espada_bronze.png", self.scene, overall_layer)
        self.copper_sword_recept = Recipe("copper sword", 20, 10, required_items, output, self.scene, self.rendering_layer)

        # receita ferro sword
        item1 = InventoryItem("stick_madeira", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item2 = InventoryItem("ouro", 0, 2, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        item3 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("esp_ferro", 0, 1, "our_game/game_res/graphics/craftables/espada_ferro.png", self.scene, overall_layer)
        self.iron_sword_recept = Recipe("iron sword", 30, 10, required_items, output, self.scene, self.rendering_layer)

        # receita bow
        item1 = InventoryItem("stick_madeira", 0, 5, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 2, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("stick_madeira", 0, 5, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("bow", 0, 1, "our_game/game_res/graphics/craftables/bow.png", self.scene, overall_layer)
        self.bow_recept = Recipe("bow", 5, 10, required_items, output, self.scene, self.rendering_layer)

        # receita ouro sword
        item1 = InventoryItem("stick_madeira", 0, 5, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 2, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("ouro", 0, 5, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("esp_ouro", 0, 1, "our_game/game_res/graphics/craftables/espada_ouro.png", self.scene, overall_layer)
        self.ouro_sword_recept = Recipe("ouro sword", 20, 10, required_items, output, self.scene, self.rendering_layer)

        # receita diamante sword
        item1 = InventoryItem("stick_iron", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_iron.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("diamante", 0, 5, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("esp_diamante", 0, 1, "our_game/game_res/graphics/craftables/espada_diamante.png", self.scene, overall_layer)
        self.diamond_sword_recept = Recipe("diamond sword", 30, 10, required_items, output, self.scene, self.rendering_layer)

        # receita rubi sword
        item1 = InventoryItem("stick_iron", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_iron.png", self.scene, overall_layer)
        item2 = InventoryItem("diamante", 0, 10, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        item3 = InventoryItem("rubi", 0, 5, "our_game/game_res/graphics/crafting_resources/rubi.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("esp_rubi", 0, 1, "our_game/game_res/graphics/craftables/espada_rubi.png", self.scene, overall_layer)
        self.rubi_sword_recept = Recipe("rubi sword", 40, 10, required_items, output, self.scene, self.rendering_layer)

        # receita iron hammer
        item1 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("stick_madeira", 0, 10, "our_game/game_res/graphics/crafting_resources/stick_madeira.png", self.scene, overall_layer)
        item4 = InventoryItem("ferro", 0, 5, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3, item4]
        output = InventoryItem("hammer_iron", 0, 1, "our_game/game_res/graphics/craftables/hammer_iron.png", self.scene, overall_layer)
        self.iron_hammer_recept = Recipe("iron hammer", 10, 10, required_items, output, self.scene, self.rendering_layer)

        # receita iron chest
        item1 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item4 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3, item4]
        output = InventoryItem("iron_chest", 0, 1, "our_game/game_res/graphics/craftables/iron_chest.png", self.scene, overall_layer)
        self.iron_chest_recept = Recipe("iron chest", 20, 10, required_items, output, self.scene, self.rendering_layer)

        # receita iron helm
        item1 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item2 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        item3 = InventoryItem("ferro", 0, 10, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("iron_helm", 0, 1, "our_game/game_res/graphics/craftables/iron_helm.png", self.scene, overall_layer)
        self.iron_helm_recept = Recipe("iron helm", 20, 10, required_items, output, self.scene, self.rendering_layer)

        # receita leather legs
        item1 = InventoryItem("leather", 0, 15, "our_game/game_res/graphics/crafting_resources/leather.png", self.scene, overall_layer)
        item2 = InventoryItem("iron", 0, 1, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2]
        output = InventoryItem("leather_legs", 0, 1, "our_game/game_res/graphics/craftables/leather_legs.png", self.scene, overall_layer)
        self.leather_legs_recept = Recipe("leather legs", 5, 10, required_items, output, self.scene, self.rendering_layer)

        # receita ouro helm
        item1 = InventoryItem("ouro", 0, 10, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        item2 = InventoryItem("ouro", 0, 10, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        item3 = InventoryItem("ouro", 0, 10, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("ouro_helm", 0, 1, "our_game/game_res/graphics/craftables/ouro_helm.png", self.scene, overall_layer)
        self.ouro_helm_recept = Recipe("ouro helm", 15, 10, required_items, output, self.scene, self.rendering_layer)

        # receita ouro legs
        item1 = InventoryItem("ouro", 0, 15, "our_game/game_res/graphics/crafting_resources/ouro.png", self.scene, overall_layer)
        item2 = InventoryItem("iron", 0, 1, "our_game/game_res/graphics/crafting_resources/ferro.png", self.scene, overall_layer)
        required_items = [item1, item2]
        output = InventoryItem("ouro_legs", 0, 1, "our_game/game_res/graphics/craftables/ouro_legs.png", self.scene, overall_layer)
        self.ouro_legs_recept = Recipe("ouro legs", 15, 10, required_items, output, self.scene, self.rendering_layer)

        # receita rubi feet
        item1 = InventoryItem("rubi", 0, 15, "our_game/game_res/graphics/crafting_resources/rubi.png", self.scene, overall_layer)
        item2 = InventoryItem("rubi", 0, 15, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        required_items = [item1, item2]
        output = InventoryItem("rubi_feet", 0, 1, "our_game/game_res/graphics/craftables/rubi_feet.png", self.scene, overall_layer)
        self.rubi_feet_recept = Recipe("rubi feet", 45, 10, required_items, output, self.scene, self.rendering_layer)

        # receita bronze feet
        item1 = InventoryItem("bronze", 0, 15, "our_game/game_res/graphics/crafting_resources/bronze.png", self.scene, overall_layer)
        item2 = InventoryItem("bronze", 0, 15, "our_game/game_res/graphics/crafting_resources/bronze.png", self.scene, overall_layer)
        required_items = [item1, item2]
        output = InventoryItem("bronze_feet", 0, 1, "our_game/game_res/graphics/craftables/bronze_feet.png", self.scene, overall_layer)
        self.bronze_feet_recept = Recipe("bronze feet", 10, 10, required_items, output, self.scene, self.rendering_layer)

        # receita diamante helm
        item1 = InventoryItem("diamante", 0, 10, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        item2 = InventoryItem("diamante", 0, 10, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        item3 = InventoryItem("diamante", 0, 10, "our_game/game_res/graphics/crafting_resources/diamante.png", self.scene, overall_layer)
        required_items = [item1, item2, item3]
        output = InventoryItem("diamond_helm", 0, 1, "our_game/game_res/graphics/craftables/diamante_helm.png", self.scene, overall_layer)
        self.diamond_helm_recept = Recipe("diamond helm", 30, 10, required_items, output, self.scene, self.rendering_layer)

        self.recipes = [self.copper_sword_recept, self.iron_sword_recept, self.bow_recept, self.ouro_sword_recept,
                        self.diamond_sword_recept, self.rubi_sword_recept, self.iron_hammer_recept,
                        self.iron_chest_recept, self.iron_helm_recept, self.leather_legs_recept, self.ouro_helm_recept,
                        self.ouro_legs_recept, self.rubi_feet_recept, self.bronze_feet_recept, self.diamond_helm_recept]

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


