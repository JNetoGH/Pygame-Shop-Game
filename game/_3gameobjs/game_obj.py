import pygame
from _1systems.screen.scalable_game_screen import ScalableGameScreen
from _2components.transform.transform import Transform


class GameObject(pygame.sprite.Sprite):

    def __init__(self, scene):
        super().__init__(scene.all_sprites)

        # when a component is instantiated, it is automatically stored here
        self.components_list = []
        self.scene = scene

        # sets the transform
        self.transform = Transform(self)

        # makes a default img to the object
        self.image = pygame.Surface((64, 32))
        self.image.fill((255, 255, 255))
        # - The rectangle that holds the game object's image
        # - The center pos of the rect is the same of the gm obj pos by default, but needs to be set back to the
        #   object pos at every movement, it's automatically made by the transform bia the move_position method
        self.rect = self.image.get_rect(center=self.transform.position)

        # adds itself to the scene game object list
        scene.all_game_obj.append(self)

        # calls its start() method
        self.start()

    def get_index_in_scene_all_game_objects_list(self) -> int:
        for i in range(0, len(self.scene.all_game_obj)):
            if self.scene.all_game_obj[i] == self:
                return i

    def start(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def render(self) -> None:
        pass

    def debug_late_render(self) -> None:
        # img rect
        pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, "red", self.rect, 1)
