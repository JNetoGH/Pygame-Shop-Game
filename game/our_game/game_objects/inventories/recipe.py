import random
import pygame
from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.components.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.inventories.inventory_item import InventoryItem


class Recipe(GameObject):

    def __init__(self, name:str, player_has_me: bool, success_rating, buying_price,
                 list_of_resources_for_crafting: list[InventoryItem], craftable_out_put, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.buying_price = buying_price
        self.success_rating = success_rating

        self.player_has_me: bool = player_has_me

        self.list_of_resources_for_crafting = list_of_resources_for_crafting
        self.craftable_output = craftable_out_put

        self.fix_game_object_on_screen(pygame.Vector2(
            ScalableGameScreen.HalfDummyScreenWidth,
            ScalableGameScreen.HalfDummyScreenHeight-50)
        )
        self.single_sprite = SingleSpriteComponent("our_game/game_res/graphics/ui/receitas_layout.png", self)
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
