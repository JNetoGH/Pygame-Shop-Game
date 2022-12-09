import pygame

from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject


class TrasnlucentSquare(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.stop_rendering_this_game_object()

        self.image = pygame.Surface((400, 170))
        self.image.set_alpha(200)  # alpha level
        self.image.fill((0, 0, 0))  # this fills the entire surface

        self.fix_game_object_on_screen(pygame.Vector2(230,365))
