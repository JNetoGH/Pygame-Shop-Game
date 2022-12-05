import pygame
from player import Player
from _1systems.scalable_game_screen_system import ScalableGameScreen
from test_obj import TestObj


class Scene:
    def __init__(self, game):
        self.game = game
        self.all_sprites = pygame.sprite.Group()  # sprite group, used to draw then all
        """ 
        LIST USED FOR UPDATES:
            - It holds all game objects of the scene
            - When a game Obj is instantiated, it's automatically stored here using the scene passed as parameter in 
              its constructor
        """
        self.all_game_obj = []
        self.scene_start()  # called once

    def scene_start(self):
        Player("game_player", self)
        TestObj("test_obj_1", self)

    def scene_update(self):
        # first is called the components update of the object, and then the game object itself
        for gm in self.all_game_obj:
            for component in gm.components_list:
                component.component_update()
            gm.game_object_update()

    def scene_render(self):
        ScalableGameScreen.GameScreenDummySurface.fill("darkgreen")  # clears the screen for rendering
        self.all_sprites.draw(ScalableGameScreen.GameScreenDummySurface)
        self.all_sprites.update()
        for gm in self.all_game_obj:
            gm.game_object_render()
        # used to see lines and squares mainly
        for gm in self.all_game_obj:
            gm.game_object_debug_late_render()
