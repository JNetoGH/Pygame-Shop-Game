import pygame
from _3gameobjs.map import Map
from _3gameobjs.player import Player
from camera import Camara
from rendering_layer import RenderingLayer
from _3gameobjs.test_obj import TestObj
from _1systems.scalable_game_screen_system import ScalableGameScreen


class Scene:

    def __init__(self, game):

        self.game = game

        """ 
        LIST USED FOR UPDATES:
            - It holds all game objects of the scene
            - When a game Obj is instantiated, it's automatically stored here using the scene passed as parameter in 
              its constructor """
        self.all_game_obj = []

        # - When a game Obj is instantiated, it's automatically stored here using the layer passed as parameter in its constructor
        self.rendering_layer_map = RenderingLayer()
        self.rendering_layer_test = RenderingLayer()
        self.rendering_layer_player = RenderingLayer()
        self.rendering_layer_tools = RenderingLayer()
        self.rendering_layers = [self.rendering_layer_map, self.rendering_layer_test, self.rendering_layer_player, self.rendering_layer_tools]

        self.scene_start()  # called once

        # game objects
        self.map = Map("map", self, self.rendering_layer_map)
        self.player = Player("game_player", self, self.rendering_layer_player)
        self.player.transform.move_world_position(pygame.Vector2(500, 500))
        self.test_obj = TestObj("test_obj_1", self, self.rendering_layer_test)

        # main camera will render the rendering layers
        self.main_camera = Camara(self.rendering_layers)
        self.main_camera.follow_game_object(self.player)

    def scene_start(self):
        pass

    def scene_update(self):
        # first updates the components then the game object itself
        for gm in self.all_game_obj:
            for component in gm.components_list:
                component.component_update()
            gm.game_object_update()

    def scene_render(self):
        # clears the screen for rendering
        ScalableGameScreen.GameScreenDummySurface.fill("darkgreen")
        # renders all rendering layers
        self.main_camera.render_layers()

    # CALLED BY THE InspectorDebuggingCanvas to show this text at the inspector
    def get_inspector_debugging_status(self) -> str:
        return f"SCENE DEBUGGING STATUS\n" \
               f"total rendering layers: {len(self.rendering_layers)}\n" \
               f"total game objects: {len(self.all_game_obj)}\n"

