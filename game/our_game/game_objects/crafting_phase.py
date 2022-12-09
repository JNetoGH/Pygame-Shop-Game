import pygame

from JNetoProductions_pygame_game_engine.components.key_tracker.key_tracker import KeyTracker
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from our_game.game_objects.craft_inventory import Recipe


class CraftingPhase(GameObject):
    def __init__(self, name: str, player, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.stop_rendering_this_game_object()

        self.player = player
        self.is_running = False
        self.current_item_index = 0

        # key trackers
        self.key_tracker_arrow_left = KeyTracker(pygame.K_LEFT, self)
        self.key_tracker_arrow_right = KeyTracker(pygame.K_RIGHT, self)
        self.key_tracker_arrow_up = KeyTracker(pygame.K_UP, self)
        self.key_tracker_arrow_down = KeyTracker(pygame.K_DOWN, self)
        self.key_tracker_enter = KeyTracker(pygame.K_RETURN, self)
        self.key_tracker_k = KeyTracker(pygame.K_k, self)

    def run_phase(self):
        self.is_running = True
        self.current_item_index = 0

        self.start_rendering_this_game_object()

        self.scene.main_camera.stop_following_current_set_game_object()
        self.scene.main_camera.focus_camera_at_world_position(pygame.Vector2(
            self.player.transform.world_position.x + 300,
            self.player.transform.world_position.y + 200
        ))

        for recipe in self.player.craft_inventory.recipes:
            recipe.stop_showing_recipe_on_screen()

    def stop_phase(self):
        self.is_running = False
        self.stop_rendering_this_game_object()
        self.scene.main_camera.follow_game_object(self.player)

    def game_object_update(self) -> None:
        if self.is_running:

            print("running crafting phase")

            current_recipe: Recipe = self.player.craft_inventory.recipes[self.current_item_index]
            current_recipe.show_recipe_recept_on_screen()

            # switch between resources
            if self.key_tracker_arrow_right.has_key_been_fired_at_this_frame:
                if not self.current_item_index == len(self.player.craft_inventory.recipes) - 1:
                    current_recipe.stop_showing_recipe_on_screen()
                    self.current_item_index += 1
            elif self.key_tracker_arrow_left.has_key_been_fired_at_this_frame:
                if not self.current_item_index <= 0:
                    self.current_item_index -= 1
                    current_recipe.stop_showing_recipe_on_screen()

            # craft
            elif self.key_tracker_enter.has_key_been_fired_at_this_frame:
                current_recipe.craft(self.player,
                                     self.player.res_inventory.resources,
                                     self.player.craft_inventory.craftables)

            # exit crafting phase
            elif self.key_tracker_k.has_key_been_fired_at_this_frame:
                current_recipe.stop_showing_recipe_on_screen()
                self.stop_phase()

