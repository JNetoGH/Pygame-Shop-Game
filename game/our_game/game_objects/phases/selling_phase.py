import random

import pygame

from JNetoProductions_pygame_game_engine.components.key_tracker.key_tracker import KeyTracker
from JNetoProductions_pygame_game_engine.components.single_sprite.single_sprite import SingleSprite
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen


class Npc(GameObject):

    TotalAvailableCompleteNpcsSpriteSet = 3
    AvailableNpcsPaths = ["our_game/game_res/graphics/npcs/npc_0/down/0.png",
                          "our_game/game_res/graphics/npcs/npc_1/down/0.png",
                          "our_game/game_res/graphics/npcs/npc_2/down/0.png"] 

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.sprite_set = random.randint(0, Npc.TotalAvailableCompleteNpcsSpriteSet-1)
        self.single_sprite = SingleSprite(Npc.AvailableNpcsPaths[self.sprite_set], self)


class SellingPhase(GameObject):

    def __init__(self, name: str, player, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        # core stuff
        self.player = player
        self.is_running = False

        # key trackers
        self.key_tracker_enter = KeyTracker(pygame.K_RETURN, self)
        self.key_tracker_k = KeyTracker(pygame.K_k, self)

        # others
        self.remove_default_rect_image()

        # npc generation: its static, a copy  of it is manipulated
        self.available_points: list[pygame.Vector2] = [pygame.Vector2(200,200), pygame.Vector2(300,300),
                                                       pygame.Vector2(400,400), pygame.Vector2(500,500),
                                                       pygame.Vector2(600,600)]

        self.amount_of_npcs_to_be_instantiated = 2

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

            created_npc = Npc(f"npc{i}", self.scene, self.rendering_layer_of_npcs)
            created_npc.transform.move_world_position(current_point)
            self.list_of_npc.append(created_npc)

            # remove the used position from the copy, in order to always use a diff position
            available_points_copy.remove(current_point)

        for npc in self.list_of_npc:
            print(f"name: {npc.name} | + posi{npc.transform.world_position}")
            print()

    def stop_phase(self):
        self.is_running = False

        # clear the generated npcs from the scene
        for npc in self.list_of_npc:
            npc.stop_rendering_this_game_object()
            self.scene.remove_game_object(npc)


    def game_object_update(self) -> None:
        if self.is_running:

            #print("runnin selling phase")
            # exit crafting phase
            if self.key_tracker_k.has_key_been_fired_at_this_frame:
                self.stop_phase()
