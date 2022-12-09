import random
import pygame
from JNetoProductions_pygame_game_engine.components.collider_component import ColliderComponent
from JNetoProductions_pygame_game_engine.components.key_tracker_component import KeyTrackerComponent
from JNetoProductions_pygame_game_engine.components.rect_trigger_component import RectTriggerComponent
from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.components.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.game_time_system import GameTime
from our_game.game_objects.inventories.craftable_recipe import CraftableRecipe
from our_game.game_objects.inventories.inventory_item import InventoryItem


class ItemImgHolder(GameObject):

    def __init__(self, name: str, path_to_image, purchase_balloon, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.single_sprite = SingleSpriteComponent(path_to_image, self)
        self.single_sprite.scale_itself(3)
        self.purchase_balloon = purchase_balloon

    def game_object_update(self) -> None:
        position = pygame.Vector2()
        position.x = self.purchase_balloon.transform.world_position.x
        position.y =  self.purchase_balloon.transform.world_position.y
        self.transform.move_world_position(position)


class PurchaseBalloon(GameObject):

    def __init__(self, name: str, path_to_image, price_willing_to_pay,npc_owner, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.single_sprite = SingleSpriteComponent("our_game/game_res/graphics/ui/balao.png", self)
        self.price_willing_to_pay = price_willing_to_pay

        self.text_render_of_price_willing_to_pay = TextRenderComponent(f"{self.price_willing_to_pay}", 15, pygame.Color(0, 128, 0), 12, -27, self)
        self.item_image_holder = ItemImgHolder("image placer", path_to_image, self, self.scene, self.rendering_layer)
        self.status_text_renderer = TextRenderComponent(f"none", 15, pygame.Color(255, 255, 255), 0, -80, self)
        self.npc_owner = npc_owner

    def game_object_update(self) -> None:
        y_off_set = -60
        x_off_set = -20
        position = pygame.Vector2(self.npc_owner.transform.world_position.x, self.npc_owner.transform.world_position.y)
        position.y = position.y + y_off_set
        position.x = position.x + x_off_set
        self.transform.move_world_position(position)


class Npc(GameObject):

    TotalAvailableCompleteNpcsSpriteSet = 3
    AvailableNpcsPaths = ["our_game/game_res/graphics/npcs/npc_0/down/0.png",
                          "our_game/game_res/graphics/npcs/npc_1/down/0.png",
                          "our_game/game_res/graphics/npcs/npc_2/down/0.png"]

    def __init__(self, name: str, player, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        # sets the object in world
        self.sprite_set = random.randint(0, Npc.TotalAvailableCompleteNpcsSpriteSet-1)
        self.single_sprite = SingleSpriteComponent(Npc.AvailableNpcsPaths[self.sprite_set], self)
        self.collider = ColliderComponent(0, 0, 55, 70, self)

        # generates a recipe
        self.player = player
        self.recipes: list[CraftableRecipe] = player.craft_inventory.recipes
        self.chosen_recipe: CraftableRecipe = self.recipes[random.randint(0, len(self.recipes) - 1)]
        self.chosen_recipe_output: InventoryItem = self.chosen_recipe.craftable_output

        # can variate
        self.price_willing_to_pay = self.chosen_recipe_output.price

        # used to get when the player can interact with the NPC
        self.trigger_rect = RectTriggerComponent(0, 30, 150, 80, self)

        # key trackers, confirms the purchase
        self.key_tracker_enter = KeyTrackerComponent(pygame.K_RETURN, self)

        # status of purchase
        self.status_0 = "Hello!"
        self.status_1 = "wanna sell?"
        self.status_2 = "you don't have the item"
        self.status_3 = "done"
        self.status_index = 0


        # controlling
        self.has_bought_the_item = False

        # makes the purchase balloon
        balloon_img_path = self.chosen_recipe_output.single_sprite.get_img_path()
        self.purchase_balloon = PurchaseBalloon(f"purchase balloon {self.name}", balloon_img_path,
                                                self.price_willing_to_pay, self, self.scene,
                                                self.scene.get_rendering_layer_by_name("rendering_layer_ballon"))

        # animation related: has to be the last thing called
        self.max_alpha_level = 255
        self.current_alpha_level = 1
        self.appearing_speed = 200
        self.is_in_appearing_animation = False
        self.appear_animation()

    def appear_animation(self):
        self.image.set_alpha(1)
        self.purchase_balloon.image.set_alpha(1)
        self.purchase_balloon.item_image_holder.image.set_alpha(1)
        self.is_in_appearing_animation = True

    def check_purchase(self):
        # Rect Trigger usage, if player is in trigger rect, and not has bought the item yet
        player_collider: ColliderComponent = self.player.collider
        if self.trigger_rect.is_there_a_point_inside(player_collider.world_position_get_only) and not self.has_bought_the_item:
            print("player is inside me")

            player_craftable = None
            for craftable in self.player.craft_inventory.craftables:
                if craftable.name == self.chosen_recipe_output.name:
                    player_craftable = craftable

            # if the item was found at the players items
            if isinstance(player_craftable, InventoryItem):

                # has the item
                if player_craftable.amount >= 1:
                   self.purchase_balloon.status_text_renderer.change_text(self.status_1)
                   self.purchase_balloon.status_text_renderer.change_color(pygame.Color(50, 205, 50))

                   # purchase made
                   if self.key_tracker_enter.has_key_been_fired_at_this_frame:
                       player_craftable.amount -= 1
                       self.player.money += self.price_willing_to_pay
                       self.purchase_balloon.status_text_renderer.change_text(self.status_3)
                       self.has_bought_the_item = True

                # doesn't have the item
                else:
                    self.purchase_balloon.status_text_renderer.change_text(self.status_2)
                    self.purchase_balloon.status_text_renderer.change_color(pygame.Color(255,105,97))

        # got out of the trigger
        else:

            # only change back to hello! if hasn't bought the item
            if not self.has_bought_the_item:
                self.purchase_balloon.status_text_renderer.change_text(self.status_0)
                self.purchase_balloon.status_text_renderer.change_color(pygame.Color(255, 255, 255))

    def game_object_update(self) -> None:
        if self.is_in_appearing_animation:
            self.current_alpha_level = self.current_alpha_level + self.appearing_speed * GameTime.DeltaTime
            if self.current_alpha_level <= self.max_alpha_level:
                self.image.set_alpha(self.current_alpha_level)
                self.purchase_balloon.image.set_alpha(self.current_alpha_level)
                self.purchase_balloon.item_image_holder.image.set_alpha(self.current_alpha_level)
            else:
                self.image.set_alpha(self.max_alpha_level)
                self.purchase_balloon.image.set_alpha(self.max_alpha_level)
                self.purchase_balloon.item_image_holder.image.set_alpha(self.max_alpha_level)
                self.is_in_appearing_animation = False

        self.check_purchase()


class SellingPhase(GameObject):

    def __init__(self, name: str, player, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        # core stuff
        self.player = player
        self.is_running = False

        # key trackers
        self.key_tracker_k = KeyTrackerComponent(pygame.K_k, self)

        # others
        self.remove_default_rect_image()

        # npc generation: its static, a copy  of it is manipulated
        #  points = (400, 400)(600,800)(500, 600)(800, 300)(700, 700)(200, 500)(100, 850)(900, 300)(850, 650)(650, 550)
        # (700, 200)(890, 100)(1000, 500)(1020, 700)(1050, 800)
        self.available_points: list[pygame.Vector2] = [pygame.Vector2(400,400), pygame.Vector2(600,800), pygame.Vector2(500,600),
                                                       pygame.Vector2(800,300), pygame.Vector2(700,700), pygame.Vector2(200,500),
                                                       pygame.Vector2(100,850), pygame.Vector2(900,300), pygame.Vector2(850,650),
                                                       pygame.Vector2(650,550), pygame.Vector2(700,200), pygame.Vector2(890,100),
                                                       pygame.Vector2(100,500), pygame.Vector2(1020,700), pygame.Vector2(1050,800)]

        self.amount_of_npcs_to_be_instantiated = 7

        self.rendering_layer_of_npcs = self.scene.get_rendering_layer_by_name("rendering_layer_npcs")
        # holds the npcs instantiated for this run of the phase, its cleaned when the phase stops
        self.list_of_npc = []

    def run_phase(self):
        self.is_running = True
        available_points_copy: list[pygame.Vector2] = self.available_points.copy()

        # generates npcs in random and different available positions
        for i in range(self.amount_of_npcs_to_be_instantiated):
            print(f"list: {available_points_copy}")

            rand_index = random.randint(0, len(available_points_copy)-1)
            current_point = available_points_copy[rand_index]

            created_npc = Npc(f"npc{i}", self.player, self.scene, self.rendering_layer_of_npcs)
            created_npc.transform.move_world_position(current_point)
            self.list_of_npc.append(created_npc)

            # remove the used position from the copy, in order to always use a diff position
            available_points_copy.remove(current_point)

        for npc in self.list_of_npc:
            print(f"name: {npc.name} | + posi{npc.transform.world_position}")
            print()

    def stop_phase(self):
        self.is_running = False

        # clear the generated npcs from the scene and their ballons
        for npc in self.list_of_npc:
            self.scene.remove_game_object(npc.purchase_balloon)
            self.scene.remove_game_object(npc.purchase_balloon.item_image_holder)
            self.scene.remove_game_object(npc)

    def game_object_update(self) -> None:
        if self.is_running:

            # DEBUGGING INFO
            # print("running selling phase")

            # exit crafting phase
            if self.key_tracker_k.has_key_been_fired_at_this_frame:
                self.stop_phase()
