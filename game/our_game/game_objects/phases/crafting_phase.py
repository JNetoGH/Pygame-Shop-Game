import pygame

from JNetoProductions_pygame_game_engine.components.key_tracker.key_tracker import KeyTracker
from JNetoProductions_pygame_game_engine.components.text_render.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.inventories.craft_inventory import Recipe
from our_game.game_objects.translucent_square import TrasnlucentSquare


mexida = 70
class CraftingTextHolder(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.stop_rendering_this_game_object()

        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth - 5, 280 - mexida))
        self.remove_default_rect_image()

        # explanatory texts
        x_axis = -405
        explain_size = 15
        mexida_y_txt = 15

        # tile
        self.text_render = TextRenderComponent("CRAFTING PHASE", 45, pygame.Color(255, 255, 255), x_axis,105 + mexida_y_txt, self)
        # 🡸🡺 change current recipe
        self.text_render_confirm = TextRenderComponent("Press ← or → to change current recipe", explain_size, pygame.Color(255, 255, 255), x_axis, 140 + mexida_y_txt, self)
        # enter confirm a crafting
        self.text_render_confirm = TextRenderComponent("Press Enter to confirm a crafting", explain_size, pygame.Color(255, 255, 255), x_axis, 160 + mexida_y_txt, self)
        # k ends the crafting phase
        self.text_render_confirm = TextRenderComponent("Press K to end the crafting phase", explain_size, pygame.Color(255, 255, 255), x_axis, 180 + mexida_y_txt, self)


class CraftingPhase(GameObject):
    def __init__(self, name: str, player, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.stop_rendering_this_game_object()

        self.player = player
        self.is_running = False
        self.current_item_index = 0
        self.remove_default_rect_image()

        self.translucent_square = TrasnlucentSquare("crafting_phase_translucent_square", self.scene,self.rendering_layer)
        self.text_holder = CraftingTextHolder("text_holder", self.scene, self.rendering_layer)

        # key trackers
        self.key_tracker_arrow_left = KeyTracker(pygame.K_LEFT, self)
        self.key_tracker_arrow_right = KeyTracker(pygame.K_RIGHT, self)
        self.key_tracker_arrow_up = KeyTracker(pygame.K_UP, self)
        self.key_tracker_arrow_down = KeyTracker(pygame.K_DOWN, self)
        self.key_tracker_enter = KeyTracker(pygame.K_RETURN, self)
        self.key_tracker_k = KeyTracker(pygame.K_k, self)

        # position on screen
        self.fixed_position_on_screen = pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth-5, 280-mexida)
        self.fix_game_object_on_screen(self.fixed_position_on_screen)

    def run_phase(self):
        self.is_running = True
        self.current_item_index = 0

        self.start_rendering_this_game_object()
        self.translucent_square.start_rendering_this_game_object()
        self.text_holder.start_rendering_this_game_object()

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
        self.translucent_square.stop_rendering_this_game_object()
        self.scene.main_camera.follow_game_object(self.player)
        self.text_holder.stop_rendering_this_game_object()

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

