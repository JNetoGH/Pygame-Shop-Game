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
        self.collider_rect.centerx = self.game_object_owner.transform.world_position.x + self.offset_from_game_object_x
        self.collider_rect.centery = self.game_object_owner.transform.world_position.y + self.offset_from_game_object_y
        self.collider_rect.width = self.width
        self.collider_rect.height = self.height

        # for collision checking
        self._is_colliding = False

    def check_collision(self, another_collider):

        pass

    def component_update(self):
        self.collider_rect.centerx = self.game_object_owner.transform.world_position.x + self.offset_from_game_object_x
        self.collider_rect.centery = self.game_object_owner.transform.world_position.y + self.offset_from_game_object_y
        self.collider_rect.width = self.width
        self.collider_rect.height = self.height

    def get_inspector_debugging_status(self) -> str:
        return "Component(Collider)\n"
