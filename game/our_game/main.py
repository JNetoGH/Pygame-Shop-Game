from JNetoProductions_pygame_game_engine.camera import Camara
from JNetoProductions_pygame_game_engine.game_loop import GameLoop
from JNetoProductions_pygame_game_engine.rendering_layer import RenderingLayer
from JNetoProductions_pygame_game_engine.scene import Scene
from our_game.game_objects.map import Map
from our_game.game_objects.player import Player


class Game:

    def __init__(self):

        # needs to be the first thing instantiated
        self.game_loop = GameLoop()

        # rendering layer and the main Camera
        self.rendering_layer_map = RenderingLayer()
        self.rendering_layer_test = RenderingLayer()
        self.rendering_layer_player = RenderingLayer()
        self.main_camera = Camara(self.rendering_layer_map, self.rendering_layer_test, self.rendering_layer_player)

        # the scene
        self.shop_scene = Scene(self.main_camera)

        # GameObjects
        self.game_map = Map(self, "map", self.shop_scene, self.rendering_layer_map)
        self.player = Player("game_player", self.shop_scene, self.rendering_layer_player)

        # sets the camera to follow the payer
        self.main_camera.follow_game_object(self.player)

        # GAME LOOP
        self.game_loop.set_current_scene(self.shop_scene)
        self.game_loop.run_game_loop()

Game()