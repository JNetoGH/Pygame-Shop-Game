from JNetoProductions_pygame_game_engine.camera import Camara
from JNetoProductions_pygame_game_engine.game_loop import GameLoop
from JNetoProductions_pygame_game_engine.rendering_layer import RenderingLayer
from JNetoProductions_pygame_game_engine.scene import Scene
from our_game.game_objects.phases.phase_controller import PhaseController
from our_game.game_objects.phases.phase_loader import PhaseLoader
from our_game.game_objects.phases.buying_phase import BuyingPhase
from our_game.game_objects.phases.crafting_phase import CraftingPhase
from our_game.game_objects.map import Map
from our_game.game_objects.phases.selling_phase import SellingPhase
from our_game.game_objects.player import Player


class Game:

    def __init__(self):

        # needs to be the first thing instantiated
        self.game_loop = GameLoop()

        # rendering layer and the main Camera
        self.rendering_layer_map = RenderingLayer("rendering_layer_map")
        self.rendering_layer_test = RenderingLayer("rendering_layer_test")
        self.rendering_layer_npcs = RenderingLayer("rendering_layer_npcs")
        self.rendering_layer_player = RenderingLayer("rendering_layer_player")
        self.rendering_layer_ballons = RenderingLayer("rendering_layer_ballon")
        self.rendering_layer_inventories = RenderingLayer("rendering_layer_inventories")
        self.rendering_layer_phases = RenderingLayer("rendering_layer_phases")
        self.rendering_layer_over_all = RenderingLayer("rendering_layer_over_all")
        self.main_camera = Camara(self.rendering_layer_map, self.rendering_layer_test,
                                  self.rendering_layer_npcs, self.rendering_layer_player,
                                  self.rendering_layer_ballons, self.rendering_layer_inventories,
                                  self.rendering_layer_phases,  self.rendering_layer_over_all)

        # the scene
        self.shop_scene = Scene(self.main_camera)

        # GameObjects
        self.game_map = Map(self, "map", self.shop_scene, self.rendering_layer_map)
        self.player = Player("player", self.shop_scene, self.rendering_layer_player)
        self.buying_phase = BuyingPhase("buying_phase", self.player, self.shop_scene, self.rendering_layer_phases)
        self.crafting_phase = CraftingPhase("crafting_phase", self.player, self.shop_scene, self.rendering_layer_phases)
        self.selling_phase = SellingPhase("selling_phase", self.player, self.shop_scene, self.rendering_layer_phases)

        self.phase_loader = PhaseLoader("phase_loader",  self.shop_scene, self.rendering_layer_phases)
        self.phase_controller = PhaseController("phase_controller", self.shop_scene, self.rendering_layer_phases)

        # sets the camera to follow the payer
        self.main_camera.follow_game_object(self.player)

        # GAME LOOP
        self.game_loop.set_current_scene(self.shop_scene)
        self.game_loop.run_game_loop()


Game()
