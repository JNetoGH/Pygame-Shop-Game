import pygame
from player import Player
from rendering_layer import RenderingLayer
from test_obj import TestObj
from _1systems.scalable_game_screen_system import ScalableGameScreen



class Scene:
    def __init__(self, game):
        self.game = game

        """ 
        LIST USED FOR UPDATES:
            - It holds all game objects of the scene
            - When a game Obj is instantiated, it's automatically stored here using the scene passed as parameter in 
              its constructor
        """
        self.all_game_obj = []

        # - When a game Obj is instantiated, it's automatically stored here using the layer passed as parameter in its constructor
        rendering_layer_0 = RenderingLayer()
        rendering_layer_1 = RenderingLayer()
        self.rendering_layers = [rendering_layer_0, rendering_layer_1]

        self.scene_start()  # called once

    def scene_start(self):
        Player("game_player", self, self.rendering_layers[0])
        TestObj("test_obj_1", self, self.rendering_layers[1])

    def scene_update(self):
        # first is called the components update of the object, and then the game object itself
        for gm in self.all_game_obj:
            for component in gm.components_list:
                component.component_update()
            gm.game_object_update()

    def scene_render(self):

        # clears the screen for rendering
        ScalableGameScreen.GameScreenDummySurface.fill("darkgreen")

        # renders all rendering layers
        for r_layer in self.rendering_layers:
            r_layer.render_all_game_objects()


        """      
        OLD WAY WHEN SCENE WOULD RENDER EVERYTHING 
        WITH THIS FIELD AT THE CONSTRUCTOR: self.all_sprites = pygame.sprite.Group()  # sprite group, used to draw then all
        
        self.all_sprites.draw(ScalableGameScreen.GameScreenDummySurface)
        self.all_sprites.update()
        # used to see lines and squares mainly
        for gm in self.all_game_obj:
            gm.game_object_debug_late_render()
        """

    # CALLED BY THE InspectorDebuggingCanvas to show this text at the inpector
    def get_inspector_debugging_status(self) -> str:
        return f"SCENE DEBUGGING STATUS\n" \
               f"total rendering layers: {len(self.rendering_layers)}\n" \
               f"total game objects: {len(self.all_game_obj)}\n"

