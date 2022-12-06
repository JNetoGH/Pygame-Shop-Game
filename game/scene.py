import pygame

from _3gameobjs.map import Map
from _3gameobjs.player import Player
from rendering_layer import RenderingLayer
from _3gameobjs.test_obj import TestObj
from _1systems.scalable_game_screen_system import ScalableGameScreen


class Camara:

    def __init__(self, rendering_layers_to_render: list[RenderingLayer], followed_game_object = None):
        self._rendering_layers_to_render = rendering_layers_to_render
        self._followed_game_object = followed_game_object

        # the movement off-set base on the followed game object
        self.followed_object_offset = pygame.Vector2()

    def follow_game_object(self, game_object):
        self._followed_game_object = game_object

    def render_layers(self):

        self.followed_object_offset.x = self._followed_game_object.transform.world_position.x - ScalableGameScreen.HalfDummyScreenWidth
        self.followed_object_offset.y = self._followed_game_object.transform.world_position.y - ScalableGameScreen.HalfDummyScreenHeight

        print(f"self.followed_object_offset.x: {self.followed_object_offset.x}")
        print(f"self.followed_object_offset.y: {self.followed_object_offset.y}\n")

        for r_layer in self._rendering_layers_to_render:
            for game_obj in r_layer.game_objects_to_render_read_only:

                # the final result of the render takes in consideration the game object world position
                # that's why I pre-update the image_rect
                game_obj.image_rect = game_obj.image.get_rect(center=game_obj.transform.world_position)

                # the followed game object must be treated in a different way
                if game_obj != self._followed_game_object:

                    # updates the sprite image_rect
                    offset_rect = game_obj.image_rect.copy()
                    offset_rect.center -= self.followed_object_offset
                    game_obj.image_rect = offset_rect

                    # render
                    if game_obj.should__be_rendered:
                        ScalableGameScreen.GameScreenDummySurface.blit(game_obj.image, game_obj.image_rect)
                else:

                    # updates the sprite image_rect position the followed game object image rect ,
                    # it's different from the orders because it's always n the center
                    screen_center = (ScalableGameScreen.HalfDummyScreenWidth, ScalableGameScreen.HalfDummyScreenHeight)
                    self._followed_game_object.image_rect = game_obj.image.get_rect(center=screen_center)

                    # render
                    if self._followed_game_object.should__be_rendered:
                        ScalableGameScreen.GameScreenDummySurface.blit(game_obj.image, game_obj.image_rect)


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
        self.rendering_layer_map = RenderingLayer(False)
        self.rendering_layer_test = RenderingLayer(False)
        self.rendering_layer_player = RenderingLayer(True)
        self.rendering_layer_tools = RenderingLayer(True)
        self.rendering_layers = [self.rendering_layer_map, self.rendering_layer_test, self.rendering_layer_player, self.rendering_layer_tools]

        self.scene_start()  # called once

        # game objects
        self.map = Map("map", self, self.rendering_layer_map)
        self.player = Player("game_player", self, self.rendering_layer_player)
        self.player.transform.move_world_position(pygame.Vector2(500, 500))
        self.test_obj = TestObj("test_obj_1", self, self.rendering_layer_test)
        # main camera will render the rendering layers
        self.main_camera = Camara(self.rendering_layers, self.player)

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

