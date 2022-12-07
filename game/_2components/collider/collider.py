import pygame.rect

from _2components.component_base_class.component import Component


class Collider(Component):

    def __init__(self, offset_from_game_object_x, offset_from_game_object_y, width, height, game_object_owner):
        super().__init__(game_object_owner)

        self.game_object_owner.has_collider = True

        # initing field
        self.width = width
        self.height = height
        self.offset_from_game_object_x = offset_from_game_object_x
        self.offset_from_game_object_y = offset_from_game_object_y

        # making the collider rect
        self.collider_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        # sets the collider_rect default shape and position
        # pygame is stupid, it only uses ints to represent rectanclge what truncates the float from 1.9 to 1 for example
        # making pretty bad collision, so i am rounding what makes 1.9 => 2 and 1.2 => 1, what is a bit better
        self.collider_rect.width = self.width
        self.collider_rect.height = self.height
        self.collider_rect.centerx = round(self.game_object_owner.transform.world_position.x + self.offset_from_game_object_x)
        self.collider_rect.centery = round(self.game_object_owner.transform.world_position.y + self.offset_from_game_object_y)

        # for collision checking
        self._is_colliding = False

    def check_collision(self, another_collider):
        pass

    def component_update(self):
        self.collider_rect.width = self.width
        self.collider_rect.height = self.height
        self.collider_rect.centerx = self.game_object_owner.transform.world_position.x + self.offset_from_game_object_x
        self.collider_rect.centery = self.game_object_owner.transform.world_position.y + self.offset_from_game_object_y

    def get_inspector_debugging_status(self) -> str:
        return "Component(Collider)\n"
