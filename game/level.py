import pygame

from player import Player
from settings import *


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
        player = Player(pygame.math.Vector2(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT), self.all_sprites, self)

    def tick(self):
        for gm in self.all_game_obj:
            gm.tick()

    def render(self):
        self.screen.fill((0, 0, 0)) # clears the screen
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()

        for gm in self.all_game_obj:
            gm.render()


