import pygame
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _2components.component_base_class.component import Component


class Transform(Component):
    def __init__(self, game_object_owner):
        super().__init__(game_object_owner)
        self._position: pygame.Vector2 = pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, ScalableGameScreen.HalfDummyScreenHeight)

    # it's a read-only property, I am blocking moving using the _position field because it doesn't sync with the sprite
    # changing the _position only updates the logical position but not the sprite
    @property
    def position_read_only(self):
        return self._position

    def translate(self, direction: pygame.Vector2):
        new_pos = pygame.Vector2(self.position_read_only.x + direction.x, self.position_read_only.y + direction.y)
        self.move_position(new_pos)

    def move_position(self, new_position):
        self._position = new_position
        # updates the game object image's rect position, moves the image's rect together with the transform
        self._game_object_owner.rect.center = self.position_read_only

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(Transform)\n" \
               f"position: {self.position_read_only}\n"
