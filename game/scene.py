import pygame
from player import Player
from _1systems.screen.scalable_game_screen import ScalableGameScreen
from test_obj import TestObj


class Scene:
    def __init__(self, game):
        self.game = game
        self.all_sprites = pygame.sprite.Group()  # sprite group, used to draw then all
        """ 
        LIST USED FOR TICKS:
            - I had to call it tick() because pygame is stupid and already has a method called update, used for sprites
            - It holds all game objects of the scene
            - When a game Obj is instantiated, it's automatically stored here using the scene passed as parameter in 
              its constructor
        """
        self.all_game_obj = []
        self.start()  # called once

    def start(self):
        Player(self)
        TestObj(self)

    def tick(self):
        for gm in self.all_game_obj:
            gm.tick()

    def render(self):
        ScalableGameScreen.GameScreenDummySurface.fill("darkgreen")  # clears the screen for rendering
        self.all_sprites.draw(ScalableGameScreen.GameScreenDummySurface)
        self.all_sprites.update()
        for gm in self.all_game_obj:
            gm.render()
        for gm in self.all_game_obj:
            gm.debug_late_render()
