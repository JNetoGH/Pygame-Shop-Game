import pygame

from _1systems.screen.screen import Screen
from _2components.component_base_class.component import Component


class SingleScaledSprite(Component):

    def __init__(self, img_path, game_object_owner):
        super().__init__(game_object_owner)
        self.scaled_sprite_as_surface = SingleScaledSprite.return_scaled_sprite(pygame.image.load(img_path).convert_alpha(), Screen.SCALE_FROM_REFERENCE)
        self.game_object_owner.rect = self.game_object_owner.image.get_rect(center=self.game_object_owner.transform.position)
        self.game_object_owner.image = self.scaled_sprite_as_surface

    def scale_itself(self, scale):
        scaled_sprite_as_surface = SingleScaledSprite.return_scaled_sprite(self.scaled_sprite_as_surface, scale)
        self.game_object_owner.image = scaled_sprite_as_surface
        self.game_object_owner.rect = self.game_object_owner.image.get_rect(center=self.game_object_owner.transform.position)


    # scaled like 0.8 = 80%
    @staticmethod
    def return_scaled_sprite(surface_img, scale):
        return pygame.transform.scale(surface_img, (surface_img.get_width() * scale, surface_img.get_height() * scale))
