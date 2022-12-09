import enum
import random
import pygame
from JNetoProductions_pygame_game_engine.components.key_tracker_component import KeyTrackerComponent
from JNetoProductions_pygame_game_engine.components.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.npc import Npc
from our_game.game_objects.phases.demand_enum import Demand
from our_game.game_objects.phases.phase_controller import PhaseController
from our_game.game_objects.phases.phase_loader import PhaseLoader
from our_game.game_objects.translucent_square import TrasnlucentSquare


class SellingPhaseTextHolder(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.remove_default_rect_image()

        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth,
                                                      ScalableGameScreen.HalfDummyScreenHeight))

        # explanatory texts
        explain_size = 15
        x_axis = -400
        mexida_y_txt = -150

        # tile
        self.text_render = TextRenderComponent("SELLING PHASE", 45, pygame.Color(255, 255, 255), x_axis, 120 + mexida_y_txt, self)
        self.text_render_confirm = TextRenderComponent("Talk to NPCS and sell your items", explain_size,  pygame.Color(255, 255, 255), x_axis, 160 + mexida_y_txt, self)
        # enter confirm a crafting
        self.text_render_confirm = TextRenderComponent("Press E to confirm a sale", explain_size, pygame.Color(255, 255, 255), x_axis, 180 + mexida_y_txt, self)
        # k ends the crafting phase
        self.text_render_confirm = TextRenderComponent("Press K to end the selling phase", explain_size, pygame.Color(255, 255, 255), x_axis, 200 + mexida_y_txt, self)



class SellingPhase(GameObject):

    def __init__(self, name: str, player, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        # core stuff
        self.player = player
        self.is_running = False
        self.stop_rendering_this_game_object()

        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth,
                                                      ScalableGameScreen.HalfDummyScreenHeight))

        # key trackers
        self.key_tracker_k = KeyTrackerComponent(pygame.K_k, self)

        self.translucent_square = TrasnlucentSquare("selling_phase_translucent_square", self.scene, self.rendering_layer)
        self.selling_phase_text_holder = SellingPhaseTextHolder("selling_phase_text_holder", self.scene, self.rendering_layer)
        self.translucent_square.stop_rendering_this_game_object()
        self.selling_phase_text_holder.stop_rendering_this_game_object()
        
        # others
        self.remove_default_rect_image()

        # stores the demand for each product
        self.demand_per_craftable_list: list[Demand] = []

        # NPC
        # npc generation: its static, a copy  of it is manipulated
        #  points = (400, 400)(600,800)(500, 600)(800, 300)(700, 700)(200, 500)(100, 850)
        #  (900, 300)(850, 650)(650, 550)(700, 200)(890, 100)(1000, 500)(1020, 700)(1050, 800)
        self.available_points: list[pygame.Vector2] = [pygame.Vector2(400,400), pygame.Vector2(600,800), pygame.Vector2(500,600),
                                                       pygame.Vector2(800,300), pygame.Vector2(700,700), pygame.Vector2(200,500),
                                                       pygame.Vector2(100,850), pygame.Vector2(900,300), pygame.Vector2(850,650),
                                                       pygame.Vector2(650,550), pygame.Vector2(700,200), pygame.Vector2(890,100),
                                                       pygame.Vector2(100,500), pygame.Vector2(1020,700), pygame.Vector2(1050,800)]
        self.amount_of_npcs_to_be_instantiated = 7
        self.rendering_layer_of_npcs = self.scene.get_rendering_layer_by_name("rendering_layer_npcs")
        # holds the npcs instantiated for this run of the phase, its cleaned when the phase stops
        self.list_of_npc = []

    def generate_demand(self):
        self.demand_per_craftable_list = []
        for product in self.player.craft_inventory.craftables:
            demand = random.randint(1, 3)
            if demand == 1:
                self.demand_per_craftable_list.append(Demand.Low)
            elif demand == 2:
                self.demand_per_craftable_list.append(Demand.Normal)
            elif demand == 3:
                self.demand_per_craftable_list.append(Demand.High)

    def run_phase(self):

        self.is_running = True
        self.start_rendering_this_game_object()
        self.translucent_square.start_rendering_this_game_object()
        self.selling_phase_text_holder.start_rendering_this_game_object()

        # DEMAND
        # generates the demand
        self.generate_demand()
        # prints the demand for each craftable on screes
        print("\nDemands for each craftable item:")
        for demand in self.demand_per_craftable_list:
            print(demand)

        # NPCS
        # the amount of npcs for selling phase can variate from 5 to 0
        self.amount_of_npcs_to_be_instantiated = random.randint(5, 8)
        # resets the list of npcs
        self.list_of_npc = []
        # available point for npcs being instantiated, it is manipulated having positions removed in order to do
        # not have 2 NPCS at the same position
        available_points_copy: list[pygame.Vector2] = self.available_points.copy()
        # generates npcs in random and different available positions
        for i in range(self.amount_of_npcs_to_be_instantiated):

            rand_index = random.randint(0, len(available_points_copy)-1)
            current_point = available_points_copy[rand_index]

            created_npc = Npc(f"npc{i}", self.player, self.scene, self.rendering_layer_of_npcs)
            created_npc.transform.move_world_position(current_point)
            self.list_of_npc.append(created_npc)

            # remove the used position from the copy, in order to always use a diff position
            available_points_copy.remove(current_point)

        print("\nNPCS")
        print(f"total of NPCS for this SellingPhase: {len(self.list_of_npc)}")
        for npc in self.list_of_npc:
            print(f"name: {npc.name} | + posi: {npc.transform.world_position} |"
                  f" price willing to pay: {npc.price_willing_to_pay} |"
                  f" demand status of requested craftable: {npc.demand_status_of_craftable}")
        print()


    def stop_phase(self):
        self.is_running = False
        self.stop_rendering_this_game_object()
        self.translucent_square.stop_rendering_this_game_object()
        self.selling_phase_text_holder.stop_rendering_this_game_object()

        # clear the generated npcs from the scene and their ballons
        for npc in self.list_of_npc:
            self.scene.remove_game_object(npc.purchase_balloon)
            self.scene.remove_game_object(npc.purchase_balloon.item_image_holder)
            self.scene.remove_game_object(npc)

        # runs the BuyingPhase
        # PhaseController.CurrentPhase = PhaseController.PhaseCode.BuyingPhase
        self.scene.get_game_object_by_name("phase_loader").load_phase(PhaseController.PhaseCode.BuyingPhase)


    def game_object_update(self) -> None:
        if self.is_running:

            # DEBUGGING INFO
            # print("running selling phase")

            # exit crafting phase
            if self.key_tracker_k.has_key_been_fired_at_this_frame:
                self.stop_phase()
