import pygame
from _2components.component_base_class.component import Component
from settings import *

class Transform(Component):
    def __init__(self, game_object_owner):
        super().__init__(game_object_owner)
        self.position: pygame.math.Vector2 = pygame.math.Vector2(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT)

    def translate(self, direction: pygame.math.Vector2):
        new_pos = pygame.Vector2(self.position.x + direction.x, self.position.y + direction.y)
        self.move_position(new_pos)

    def move_position(self, new_position):
        self.position = new_position
        # updates the game object image's rect position, moves the image's rect together with the transform
        self.game_object_owner.rect.center = self.position
