import pygame
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _2components.component_base_class.component import Component


class Transform(Component):
    def __init__(self, game_object_owner):
        super().__init__(game_object_owner)
        self.world_position: pygame.Vector2 = pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, ScalableGameScreen.HalfDummyScreenHeight)
        self._screen_position: pygame.Vector2 = pygame.Vector2()
        self._is_center_point_appearing_on_screen = False

    @property
    def screen_position_read_only(self):
        return self._screen_position

    @property
    def is_center_point_appearing_on_screen_read_only(self):
        return self._is_center_point_appearing_on_screen

    def translate_world_position(self, direction: pygame.Vector2):
        new_pos = pygame.Vector2(self.world_position.x + direction.x, self.world_position.y + direction.y)
        self.move_world_position(new_pos)

    def move_world_position(self, new_position):
        self.world_position = new_position

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(Transform)\n" \
               f"world position:  {self.world_position}\n" \
               f"screen position: {self._screen_position}\n"

    def component_update(self):
        # updates the screen position  a.k.a. image_rect position
        self._screen_position = pygame.Vector2(self.game_object_owner.image_rect.centerx, self.game_object_owner.image_rect.centery)
        # updates _is_center_point_appearing_on_screen
        is_in_x = ScalableGameScreen.DummyScreenWidth > self._screen_position.x > 0
        is_in_y = ScalableGameScreen.DummyScreenHeight > self._screen_position.y > 0
        self._is_center_point_appearing_on_screen = is_in_x and is_in_y
