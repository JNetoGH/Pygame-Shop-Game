import pygame
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _2components.component_base_class.component import Component


class Transform(Component):
    def __init__(self, game_object_owner):
        super().__init__(game_object_owner)
        self.position: pygame.Vector2 = pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, ScalableGameScreen.HalfDummyScreenHeight)

    def translate(self, direction: pygame.Vector2):
        new_pos = pygame.Vector2(self.position.x + direction.x, self.position.y + direction.y)
        self.move_position(new_pos)

    def move_position(self, new_position):
        self.position = new_position

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(Transform)\n" \
               f"position: {self.position}\n"
