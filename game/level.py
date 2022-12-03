import pygame

from player import Player
from settings import *
from test_obj import TestObj


class Level:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen  # get the display surface for rendering
        self.all_sprites = pygame.sprite.Group()  # sprite group, used to draw then all

        """ 
        LIST USED FOR TICKS:
            - I had to call it tick() because pygame is stupid and already has a method called update, used for sprites
            - It holds all game objects of the scene
            - When a game Obj is instantiated, it's automatically stored here using the level passed as parameter in 
              its constructor
        """
        self.all_game_obj = []

        self.start()  # called once

    def start(self):
        self.player = Player(self)
        self.testObj = TestObj(self)

    def tick(self):
        for gm in self.all_game_obj:
            gm.tick()

    def render(self):
        self.screen.fill((0, 0, 0)) # clears the screen
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()

        for gm in self.all_game_obj:
            gm.render()

        for gm in self.all_game_obj:
            gm.debug_render()


